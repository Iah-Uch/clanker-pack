// Pure data for the prompt-cache keeper: prices, timing, text. Nothing here touches `$`; the hooks that do live in
// register.tsx, because the engine reads `$` only where a module spells it out.
export const TTL_MS = 60 * 60 * 1000
export const PING_EVERY_MS = 50 * 60 * 1000
export const MIN_PING_MS = 60 * 1000
export const MAX_RETRIES = 3
export const AUTO_WARM_MS = 3 * 60 * 60 * 1000
// Auto mode renews the window to this far past each turn. Past roughly 40 idle pings
// (the write/read price ratio) one cold rewrite costs less than the pings.
export const AUTO_WINDOW_MS = 24 * 60 * 60 * 1000
export const BIG_TOKENS = 50000
// A rewrite below this costs cents; a turn's ordinary new content writes about this much.
export const MIN_BREAK_TOKENS = 20000
export const PING_PROMPT = 'Reply with the single word: warm'

// Prompts no person sent. Nobody could resend them after a refusal, so the guard lets them through.
export const UNATTENDED = new Set(['task-notification', 'scheduled-trigger', 'peer', 'peer-send-message', 'projects-relay', 'coordinator', 'observer', 'observer-activity'])

// $ per million tokens: [cache read, 1h cache write, output]. A model id takes the first row it matches.
export const PRICES: Array<[string, number, number, number]> = [
  ['fable-5-1', 0.25, 20, 50],
  ['opus-5-5', 0.2, 8, 20],
  ['sonnet-5-5', 0.1, 4, 10],
]

export type GuardMode = 'refuse' | 'warn'
export type CachePing = { read: number; write: number; usd: number | null }
export type ApiUsage = { input_tokens: number; output_tokens: number; cache_read_input_tokens: number; cache_creation_input_tokens: number }

export type CacheState = {
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
  last: CachePing | null
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

export function freshCache(): CacheState {
  return {
    auto: true, deadline: 0, lastRequestAt: 0, model: null, ctx: 0, compacted: false, messages: 0, guard: 'refuse', ackedAt: 0,
    coldWritePending: false, pending: null, last: null, stopped: null, waitForTurn: false, retries: 0, retryReason: '',
    gen: 0, tick: 0, inFlight: false, coldWrites: 0, coldUsd: 0,
    breaks: 0, breakUsd: 0, idleBeforeTurn: 0,
  }
}

export function priceOf(model: string | null): [number, number, number] | null {
  const id = (model ?? '').toLowerCase().replace(/[\s.]+/g, '-')
  const row = PRICES.find(([family]) => id.includes(family))
  return row ? [row[1], row[2], row[3]] : null
}

export function parseDuration(text: string): number | null {
  const m = /^(?:(\d+)h)?(?:(\d+)m)?$/.exec(text.trim())
  if (!m || (m[1] === undefined && m[2] === undefined)) return null
  return (Number(m[1] ?? 0) * 60 + Number(m[2] ?? 0)) * 60 * 1000
}

export function fmtSpan(ms: number): string {
  const total = Math.max(0, Math.round(ms / 60000))
  const h = Math.floor(total / 60)
  const m = total % 60
  return h > 0 ? `${h}h${String(m).padStart(2, '0')}m` : `${m}m`
}

export function fmtDollars(usd: number | null): string {
  return usd == null ? 'n/a' : '$' + usd.toFixed(2)
}

export function fmtTok(n: number): string {
  return n >= 1e6 ? (n / 1e6).toFixed(1) + 'M' : n >= 1000 ? Math.round(n / 1000) + 'k' : String(n)
}

export function coldUsd(s: CacheState): number | null {
  const price = priceOf(s.model)
  return price ? s.ctx * price[1] / 1e6 : null
}

export function warmUsd(s: CacheState): number | null {
  const price = priceOf(s.model)
  return price ? s.ctx * price[0] / 1e6 : null
}

/** What a fork bills: the cache read, any write, uncached input at half the 1h write rate, and the output. */
export function pingUsd(u: ApiUsage, price: [number, number, number]): number {
  return (u.cache_read_input_tokens * price[0] + u.cache_creation_input_tokens * price[1] + u.input_tokens * price[1] / 2 + u.output_tokens * price[2]) / 1e6
}

export function isCold(s: CacheState, now: number): boolean {
  return s.lastRequestAt > 0 && !s.compacted && now - s.lastRequestAt >= TTL_MS
}

export function guardText(s: CacheState, now: number): string {
  const price = priceOf(s.model)
  const rate = price ? `$${price[1]}/MTok` : 'the cache-write rate'
  const warm = warmUsd(s)
  return `the prompt cache went cold ${fmtSpan(now - s.lastRequestAt - TTL_MS)} ago. Sending this re-writes ` +
    `up to ${s.ctx.toLocaleString('en-US')} tokens at ${rate} = ${fmtDollars(coldUsd(s))}` +
    (warm == null ? '' : ` (a warm turn would cost ${fmtDollars(warm)})`) + '.'
}

export function statusText(s: CacheState, now: number): string | undefined {
  if (s.stopped) return `keepwarm stopped: ${s.stopped}`
  if (!s.deadline) return undefined
  const ping = s.last ? ` · last ping read ${fmtTok(s.last.read)} ${fmtDollars(s.last.usd)}` : ''
  const next = !s.lastRequestAt ? ' · waiting for the first turn'
    : s.compacted ? ' · waiting for the first turn after compaction'
    : isCold(s, now) ? ' · cold now, pings resume after the next turn'
    : s.waitForTurn ? ' · nothing to fork yet, first ping after the next turn'
    : s.retries ? ` · API busy, ping retry ${s.retries} of ${MAX_RETRIES}`
    : ` · ping in ${fmtSpan(s.lastRequestAt + PING_EVERY_MS - now)}`
  return `keepwarm ${fmtSpan(s.deadline - now)} left${next}${ping}`
}

/** Cancels the timer. Every new timer is set right after this, so the tick also says the schedule changed. */
export function disarm(s: CacheState) {
  if (s.pending) s.pending.cancel()
  s.pending = null
  s.tick++
}

/** Outdates any ping in flight: stop, /clear or compaction replaced the state it was sent for. */
export function outdate(s: CacheState) {
  s.gen++
}

export function afterRetries(n: number): string {
  return n ? ` after ${n} ${n === 1 ? 'retry' : 'retries'}` : ''
}

export function cacheCard(s: CacheState, now: number): string {
  const lines = [s.model ?? 'model not seen yet']
  if (s.compacted) lines.push('state       reset by compaction, waiting for the first turn')
  else if (!s.lastRequestAt) lines.push('state       no request yet this session')
  else if (isCold(s, now)) lines.push(`state       COLD, last request ${fmtSpan(now - s.lastRequestAt)} ago`)
  else lines.push(`state       warm, ${fmtSpan(s.lastRequestAt + TTL_MS - now)} left`)
  lines.push(`context     ${s.ctx.toLocaleString('en-US')} tokens`)
  lines.push(`cold cost   ${fmtDollars(coldUsd(s))} to re-write it (warm turn ${fmtDollars(warmUsd(s))})`)
  const mode = s.auto ? ' (auto: renewed to 24h after every turn)' : ''
  lines.push(`keepwarm    ${s.deadline ? (statusText(s, now) ?? '').replace(/^keepwarm /, 'on, ') + mode : s.stopped ? `stopped, ${s.stopped}` : s.auto ? 'auto, arms after the next turn' : 'off (/keepwarm on turns auto back on)'}`)
  lines.push(`guard       ${s.guard === 'refuse' ? 'refuse once (/keepwarm guard warn to only show the price)' : 'warn only (/keepwarm guard refuse to be stopped once)'}`)
  lines.push(`session     ${s.coldWrites} cold write${s.coldWrites === 1 ? '' : 's'} paid, ${fmtDollars(s.coldUsd)}`)
  if (s.breaks) lines.push(`            ${s.breaks} cache break${s.breaks === 1 ? '' : 's'} while warm, ${fmtDollars(s.breakUsd)}`)
  return lines.join('\n')
}

/** /clear or a resume starts a new conversation: nothing priced before it still exists. */
export function resetCache(s: CacheState) {
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



/** The status line piece: how long the cache stays warm, or that it went cold. Null while there is nothing to say. */
export function statusPart(s: CacheState, now: number): string | null {
  if (s.stopped) return 'keepwarm stopped'
  if (!s.lastRequestAt || s.compacted) return null
  return isCold(s, now) ? 'cache cold' : `cache ${fmtSpan(s.lastRequestAt + TTL_MS - now)}`
}

/** One line for the pane; `isCold` marks it as a warning. Null before the first request. */
export function paneLine(s: CacheState, now: number): { text: string; isCold: boolean } | null {
  if (s.compacted) return { text: 'cache reset by compaction', isCold: false }
  if (!s.lastRequestAt) return null
  if (isCold(s, now)) return { text: `cache COLD ${fmtSpan(now - s.lastRequestAt - TTL_MS)} ago · a send re-writes ${fmtDollars(coldUsd(s))}`, isCold: true }
  const keep = s.stopped ? `keepwarm stopped: ${s.stopped}` : s.deadline ? `ping in ${fmtSpan(s.lastRequestAt + PING_EVERY_MS - now)}` : 'keepwarm off'
  return { text: `cache warm ${fmtSpan(s.lastRequestAt + TTL_MS - now)} · ${keep}`, isCold: false }
}
