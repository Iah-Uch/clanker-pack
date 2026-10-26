import type { EngineInterface, Register } from 'claude-code'

const TTL_MS = 60 * 60 * 1000
const PING_EVERY_MS = 50 * 60 * 1000
const MIN_PING_MS = 60 * 1000
const MAX_RETRIES = 3
const AUTO_WARM_MS = 3 * 60 * 60 * 1000
// Auto mode renews the window to this far past each turn. Past roughly 40 idle pings
// (the write/read price ratio) one cold rewrite costs less than the pings.
const AUTO_WINDOW_MS = 24 * 60 * 60 * 1000
const BIG_TOKENS = 50000
// A rewrite below this costs cents; a turn's ordinary new content writes about this much.
const MIN_BREAK_TOKENS = 20000
const PING_PROMPT = 'Reply with the single word: warm'

// Prompts no person sent. Nobody could resend them after a refusal, so the guard lets them through.
const UNATTENDED = new Set(['task-notification', 'scheduled-trigger', 'peer', 'peer-send-message', 'projects-relay', 'coordinator', 'observer', 'observer-activity'])

// $ per million tokens: [cache read, 1h cache write, output]. A model id takes the first row it matches.
const PRICES: Array<[string, number, number, number]> = [
  ['fable-5-1', 0.25, 20, 50],
  ['opus-5-5', 0.2, 8, 20],
  ['sonnet-5-5', 0.1, 4, 10],
]

type GuardMode = 'refuse' | 'warn'
type Ping = { read: number; write: number; usd: number | null }
type Usage = { input_tokens: number; output_tokens: number; cache_read_input_tokens: number; cache_creation_input_tokens: number }

type State = {
  auto: boolean
  deadline: number
  lastRequestAt: number
  model: string | null
  ctx: number
  compacted: boolean
  messages: number
  guard: GuardMode
  ackedAt: number
  coldWritePending: boolean
  pending: { cancel: () => void } | null
  last: Ping | null
  stopped: string | null
  waitForTurn: boolean
  retries: number
  retryReason: string
  gen: number
  tick: number
  inFlight: boolean
  coldWrites: number
  coldUsd: number
  breaks: number
  breakUsd: number
  /** Idle time before the current turn's first request; 0 when there was none. */
  idleBeforeTurn: number
}

function freshState(): State {
  return {
    auto: true, deadline: 0, lastRequestAt: 0, model: null, ctx: 0, compacted: false, messages: 0, guard: 'refuse', ackedAt: 0,
    coldWritePending: false, pending: null, last: null, stopped: null, waitForTurn: false, retries: 0, retryReason: '',
    gen: 0, tick: 0, inFlight: false, coldWrites: 0, coldUsd: 0,
    breaks: 0, breakUsd: 0, idleBeforeTurn: 0,
  }
}

function priceOf(model: string | null): [number, number, number] | null {
  const id = (model ?? '').toLowerCase().replace(/[\s.]+/g, '-')
  const row = PRICES.find(([family]) => id.includes(family))
  return row ? [row[1], row[2], row[3]] : null
}

function parseDuration(text: string): number | null {
  const m = /^(?:(\d+)h)?(?:(\d+)m)?$/.exec(text.trim())
  if (!m || (m[1] === undefined && m[2] === undefined)) return null
  return (Number(m[1] ?? 0) * 60 + Number(m[2] ?? 0)) * 60 * 1000
}

function fmtDuration(ms: number): string {
  const total = Math.max(0, Math.round(ms / 60000))
  const h = Math.floor(total / 60)
  const m = total % 60
  return h > 0 ? `${h}h${String(m).padStart(2, '0')}m` : `${m}m`
}

function fmtUsd(usd: number | null): string {
  return usd == null ? 'n/a' : '$' + usd.toFixed(2)
}

function fmtTok(n: number): string {
  return n >= 1e6 ? (n / 1e6).toFixed(1) + 'M' : n >= 1000 ? Math.round(n / 1000) + 'k' : String(n)
}

function coldUsd(s: State): number | null {
  const price = priceOf(s.model)
  return price ? s.ctx * price[1] / 1e6 : null
}

function warmUsd(s: State): number | null {
  const price = priceOf(s.model)
  return price ? s.ctx * price[0] / 1e6 : null
}

/** What a fork bills: the cache read, any write, uncached input at half the 1h write rate, and the output. */
function pingUsd(u: Usage, price: [number, number, number]): number {
  return (u.cache_read_input_tokens * price[0] + u.cache_creation_input_tokens * price[1] + u.input_tokens * price[1] / 2 + u.output_tokens * price[2]) / 1e6
}

function isCold(s: State, now: number): boolean {
  return s.lastRequestAt > 0 && !s.compacted && now - s.lastRequestAt >= TTL_MS
}

function guardText(s: State, now: number): string {
  const price = priceOf(s.model)
  const rate = price ? `$${price[1]}/MTok` : 'the cache-write rate'
  const warm = warmUsd(s)
  return `the prompt cache went cold ${fmtDuration(now - s.lastRequestAt - TTL_MS)} ago. Sending this re-writes ` +
    `up to ${s.ctx.toLocaleString('en-US')} tokens at ${rate} = ${fmtUsd(coldUsd(s))}` +
    (warm == null ? '' : ` (a warm turn would cost ${fmtUsd(warm)})`) + '.'
}

function statusText(s: State, now: number): string | undefined {
  if (s.stopped) return `keepwarm stopped: ${s.stopped}`
  if (!s.deadline) return undefined
  const ping = s.last ? ` · last ping read ${fmtTok(s.last.read)} ${fmtUsd(s.last.usd)}` : ''
  const next = !s.lastRequestAt ? ' · waiting for the first turn'
    : s.compacted ? ' · waiting for the first turn after compaction'
    : isCold(s, now) ? ' · cold now, pings resume after the next turn'
    : s.waitForTurn ? ' · nothing to fork yet, first ping after the next turn'
    : s.retries ? ` · API busy, ping retry ${s.retries} of ${MAX_RETRIES}`
    : ` · ping in ${fmtDuration(s.lastRequestAt + PING_EVERY_MS - now)}`
  return `keepwarm ${fmtDuration(s.deadline - now)} left${next}${ping}`
}

function updateStatus($: EngineInterface, s: State, now: number) {
  $.ui.status(statusText(s, now))
}

/** Cancels the timer. Every new timer is set right after this, so the tick also says the schedule changed. */
function disarm(s: State) {
  if (s.pending) s.pending.cancel()
  s.pending = null
  s.tick++
}

/** Outdates any ping in flight: stop, /clear or compaction replaced the state it was sent for. */
function outdate(s: State) {
  s.gen++
}

async function stop($: EngineInterface, s: State, why: string | null) {
  s.deadline = 0
  s.stopped = why
  s.retries = 0
  outdate(s)
  disarm(s)
  updateStatus($, s, await $.clock.now())
}

async function arm($: EngineInterface, s: State) {
  disarm(s)
  s.retries = 0
  if (!s.deadline) return
  const now = await $.clock.now()
  // A timer set while the clock was read replaces this one; nothing awaits from here to the assignment.
  disarm(s)
  s.retries = 0
  if (now >= s.deadline) return stop($, s, null)
  // A cold cache is never pinged: that would pay the rewrite for nobody.
  if (s.lastRequestAt && !s.compacted && !isCold(s, now)) {
    const untilCold = s.lastRequestAt + TTL_MS - now
    if (s.waitForTurn) s.pending = $.clock.after(Math.min(s.deadline - now, untilCold), () => { void arm($, s) })
    else {
      const delay = Math.min(s.deadline - now, untilCold, Math.max(1000, s.lastRequestAt + PING_EVERY_MS - now))
      s.pending = $.clock.after(delay, () => { void ping($, s) })
    }
  } else {
    s.pending = $.clock.after(s.deadline - now, () => { void arm($, s) })
  }
  updateStatus($, s, now)
}

function afterRetries(n: number): string {
  return n ? ` after ${n} ${n === 1 ? 'retry' : 'retries'}` : ''
}

async function ping($: EngineInterface, s: State) {
  s.pending = null
  if (!s.deadline) return
  const tick = s.tick
  const now = await $.clock.now()
  const live = (await $.session.usage()).context.tokens ?? 0
  // A timer set or cancelled while the clock and the context were read owns the window now.
  if (s.tick !== tick) return s.pending || s.inFlight ? undefined : arm($, s)
  // One fork at a time; set below with no await in between.
  if (s.inFlight) return
  if (now >= s.deadline || isCold(s, now) || s.compacted || s.waitForTurn || !s.lastRequestAt) return arm($, s)
  // A compaction no hook reported leaves a far smaller context: the cache this ping would refresh is gone.
  if (s.ctx > 0 && live > 0 && live < 0.5 * s.ctx) {
    s.compacted = true
    outdate(s)
    return arm($, s)
  }
  // A request since this timer was set moved the clock.
  if (now - s.lastRequestAt < PING_EVERY_MS - 1000) return arm($, s)
  if (s.retries && now >= s.lastRequestAt + TTL_MS - MIN_PING_MS) return stop($, s, s.retryReason + afterRetries(s.retries))
  const gen = s.gen
  const sentAt = s.lastRequestAt
  s.inFlight = true
  const sent = await $.model.fork({ prompt: PING_PROMPT }).then(reply => ({ reply }), (err: unknown) => ({ err }))
  const at = await $.clock.now()
  s.inFlight = false
  // A stop, /clear, compaction or main request replaced what this fork was sent for: drop its reply.
  if (gen !== s.gen || s.lastRequestAt !== sentAt) return s.pending ? undefined : arm($, s)
  if ('err' in sent) return stop($, s, `the ping failed, ${sent.err instanceof Error ? sent.err.message : String(sent.err)}`)
  const reply = sent.reply
  if (reply === null) return stop($, s, 'the engine did not send the ping')
  if (reply.isAnswered === false) {
    // A restarted process has no conversation to fork until its first turn.
    if (reply.reason === 'nothing-to-fork') {
      s.waitForTurn = true
      return arm($, s)
    }
    const reason = reply.reason === 'api-error' ? `the API call failed${reply.status === null ? '' : ` (${reply.status})`}`
      : reply.reason === 'aborted' ? 'the ping was interrupted'
      : 'the ping returned no text'
    // A busy API is usually brief: retry while a ping can still land a minute before the cache goes cold.
    if (reply.reason === 'api-error' && (reply.status === null || reply.status === 429 || reply.status >= 500)) {
      const wait = MIN_PING_MS * 2 ** s.retries
      if (s.retries < MAX_RETRIES && at + wait < Math.min(s.deadline, s.lastRequestAt + TTL_MS - MIN_PING_MS)) {
        s.retries++
        s.retryReason = reason
        disarm(s)
        s.pending = $.clock.after(wait, () => { void ping($, s) })
        updateStatus($, s, at)
        return
      }
    }
    return stop($, s, reason + afterRetries(s.retries))
  }
  const u = reply.usage
  const price = priceOf(s.model)
  // A warm ping reads the prefix and writes only its own message; a write of a tenth of the read means the prefix broke.
  const warm = u.cache_read_input_tokens > 0 && u.cache_creation_input_tokens < 0.1 * u.cache_read_input_tokens
  const usd = price ? pingUsd(u, price) : null
  s.last = { read: u.cache_read_input_tokens, write: u.cache_creation_input_tokens, usd }
  if (!warm) return stop($, s, `the ping read ${fmtTok(u.cache_read_input_tokens)} and wrote ${fmtTok(u.cache_creation_input_tokens)} tokens (${fmtUsd(usd)}), the cache was already gone`)
  s.lastRequestAt = at
  await arm($, s)
}

/** Opens or renews the keepwarm window. */
async function startWindow($: EngineInterface, s: State, windowMs: number) {
  s.deadline = (await $.clock.now()) + windowMs
  s.stopped = null
  await arm($, s)
}

function card(s: State, now: number): string {
  const lines = [s.model ?? 'model not seen yet']
  if (s.compacted) lines.push('state       reset by compaction, waiting for the first turn')
  else if (!s.lastRequestAt) lines.push('state       no request yet this session')
  else if (isCold(s, now)) lines.push(`state       COLD, last request ${fmtDuration(now - s.lastRequestAt)} ago`)
  else lines.push(`state       warm, ${fmtDuration(s.lastRequestAt + TTL_MS - now)} left`)
  lines.push(`context     ${s.ctx.toLocaleString('en-US')} tokens`)
  lines.push(`cold cost   ${fmtUsd(coldUsd(s))} to re-write it (warm turn ${fmtUsd(warmUsd(s))})`)
  const mode = s.auto ? ' (auto: renewed to 24h after every turn)' : ''
  lines.push(`keepwarm    ${s.deadline ? (statusText(s, now) ?? '').replace(/^keepwarm /, 'on, ') + mode : s.stopped ? `stopped, ${s.stopped}` : s.auto ? 'auto, arms after the next turn' : 'off (/keepwarm on turns auto back on)'}`)
  lines.push(`guard       ${s.guard === 'refuse' ? 'refuse once (/keepwarm guard warn to only show the price)' : 'warn only (/keepwarm guard refuse to be stopped once)'}`)
  lines.push(`session     ${s.coldWrites} cold write${s.coldWrites === 1 ? '' : 's'} paid, ${fmtUsd(s.coldUsd)}`)
  if (s.breaks) lines.push(`            ${s.breaks} cache break${s.breaks === 1 ? '' : 's'} while warm, ${fmtUsd(s.breakUsd)}`)
  return lines.join('\n')
}

/** /clear or a resume starts a new conversation: nothing priced before it still exists. */
function reset(s: State) {
  s.ctx = 0
  s.lastRequestAt = 0
  s.compacted = false
  s.messages = 0
  s.idleBeforeTurn = 0
  s.ackedAt = 0
  s.coldWritePending = false
  s.waitForTurn = false
  s.deadline = 0
  s.stopped = null
  s.retries = 0
  outdate(s)
  disarm(s)
}

export const register: Register = on => {
  const s = freshState()

  on('session.start', async ($, e, next) => {
    const r = await next(e)
    $.ui.status(undefined)
    s.model = await $.session.model()
    const usage = await $.session.usage()
    if (usage.context.tokens) s.ctx = usage.context.tokens
    await $.command.register({
      name: 'keepwarm',
      description: 'Prompt cache keeper, auto by default: on, off, a fixed window such as 90m, status, or guard warn|refuse (cache-keeper)',
      argumentHint: '[on | off | 90m | status | guard warn | guard refuse]',
      immediate: true,
    })
    return r
  })

  on('session.end', async ($, e, next) => {
    if (e.reason === 'clear' || e.reason === 'resume') {
      reset(s)
      updateStatus($, s, await $.clock.now())
    }
    return next(e)
  })

  on('command.run', { command: 'keepwarm' }, async ($, e) => {
    const words = String(e.args ?? '').trim().split(/\s+/).filter(Boolean)
    const now = await $.clock.now()
    if (words[0] === 'off') {
      s.auto = false
      await stop($, s, null)
      return { text: 'keepwarm is off, auto is off too; /keepwarm on turns auto back on' }
    }
    if (!words.length || words[0] === 'on') {
      s.auto = true
      await startWindow($, s, AUTO_WINDOW_MS)
      return { text: 'keepwarm auto is on: every turn renews the window to 24h, a ping every 50 idle minutes keeps the cache read, not re-written' }
    }
    if (words[0] === 'status') return { text: card(s, now) }
    if (words[0] === 'guard') {
      if (words[1] !== 'warn' && words[1] !== 'refuse') return { text: '/keepwarm guard takes warn or refuse' }
      s.guard = words[1]
      return { text: s.guard === 'refuse' ? 'guard set to refuse once: a cold send is dropped with its price, the resend goes through' : 'guard set to warn: a cold send goes through with its price shown' }
    }
    const window = parseDuration(words[0])
    if (!window) return { text: 'keepwarm takes on, off, a window such as 6h or 90m, status, or guard warn|refuse' }
    // A fixed window ends on its own; auto mode would renew it at the next turn.
    s.auto = false
    await startWindow($, s, window)
    return { text: isCold(s, now)
      ? `keepwarm on for ${fmtDuration(window)}. The cache is cold now, so pings resume after the next turn`
      : `keepwarm on for ${fmtDuration(window)}, a ping every ${fmtDuration(PING_EVERY_MS)} of idle keeps the cache read, not re-written` }
  })

  // The message that pays for a cold cache. Only its first character is read.
  on('prompt.submit', async ($, e, next) => {
    if (e.origin.kind === 'plugin') return next(e)
    if (typeof e.text !== 'string' || e.text.trimStart().startsWith('/')) return next(e)
    const now = await $.clock.now()
    if (!isCold(s, now) || s.ctx < BIG_TOKENS) return next(e)
    const unattended = UNATTENDED.has(e.origin.kind)
    if (s.guard === 'warn' || unattended) {
      $.ui.log(`${guardText(s, now)} Sending anyway${unattended ? `, since this ${e.origin.kind} prompt cannot be sent again` : ''}.`)
      s.coldWritePending = true
      return next(e)
    }
    // The resend after a refusal is the user's yes.
    if (s.ackedAt === s.lastRequestAt) {
      s.ackedAt = 0
      s.coldWritePending = true
      return next(e)
    }
    s.ackedAt = s.lastRequestAt
    return { drop: `cache-keeper: ${guardText(s, now)} Send it again to pay it, or /clear and start from a note.` }
  })

  on('turn.step', async function* ($, e, next) {
    if (!e.agentId) {
      // A request over fewer than half the last one's messages is a compaction summary, not a rewind.
      if (e.messageCount * 2 < s.messages) {
        s.compacted = true
        outdate(s)
      }
      s.messages = e.messageCount
      const now = await $.clock.now()
      if (e.index === 0) s.idleBeforeTurn = s.lastRequestAt > 0 ? now - s.lastRequestAt : 0
      s.lastRequestAt = now
    }
    return yield* next(e)
  })

  on('turn.complete', async ($, e, next) => {
    const r = await next(e)
    if (e.agentId) return r
    const now = await $.clock.now()
    if (s.deadline && now >= s.deadline) await stop($, s, null)
    // An aborted turn that sent nothing touched no cache.
    if ((e.usage || !e.isAborted) && now - s.lastRequestAt > e.durationMs) s.lastRequestAt = now
    const compacted = s.compacted
    s.compacted = false
    s.waitForTurn = false
    s.ackedAt = 0
    const u = e.usage
    if (u) {
      if (u.model) s.model = u.model
      const prev = s.ctx
      const live = (await $.session.usage()).context.tokens ?? 0
      s.ctx = live && live > 0 ? live : u.input_tokens + u.cache_read_input_tokens + u.cache_creation_input_tokens
      // A write after compaction is the summary, not a cold write.
      const written = u.cache_creation_input_tokens
      // A cache read that fell under half the last context, inside the TTL, means the prefix broke whatever was written.
      const readDropped = s.idleBeforeTurn < TTL_MS && u.cache_read_input_tokens < 0.5 * prev && written >= MIN_BREAK_TOKENS
      if (!compacted && (s.coldWritePending ? written > 0 : prev > 20000 && (written >= 0.5 * prev || readDropped))) {
        const price = priceOf(s.model)
        const usd = price ? written * price[1] / 1e6 : null
        // A write while the cache was still inside its TTL is a broken prefix, not an expiry: keeping it warm cannot help.
        if (!s.coldWritePending && s.idleBeforeTurn < TTL_MS) {
          s.breaks++
          s.breakUsd += usd ?? 0
          $.ui.log(`cache break: ${fmtTok(written)} tokens re-written (${fmtUsd(usd)}) only ${fmtDuration(s.idleBeforeTurn)} after the last request. ` +
            'Something early in the conversation changed, such as a mod reload or a tool list change.')
        } else {
          s.coldWrites++
          s.coldUsd += usd ?? 0
          const extend = s.deadline < now + AUTO_WARM_MS
          if (extend) await startWindow($, s, AUTO_WARM_MS)
          $.ui.log(`cold write of ${fmtTok(written)} tokens paid (${fmtUsd(usd)}).` +
            (extend ? ` Keeping the cache warm for ${fmtDuration(AUTO_WARM_MS)} so it is not paid again today; /keepwarm off to stop.` : ''))
        }
      }
    }
    s.coldWritePending = false
    // A turn that reached the cache renews the window, and brings back one that stopped.
    if (s.auto && e.usage) await startWindow($, s, AUTO_WINDOW_MS)
    await arm($, s)
    return r
  })

  on('session.compact', async ($, e, next) => {
    const r = await next(e)
    if (!e.agentId) {
      s.compacted = true
      s.messages = 0
      s.ctx = 0
      outdate(s)
      disarm(s)
      await arm($, s)
    }
    return r
  })
}
