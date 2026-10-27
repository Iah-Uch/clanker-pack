import type { Register } from 'claude-code'

// A turn is one user prompt and everything Claude does before it answers.
const MAX_CALLS = 40
const MAX_SECONDS = 600
// "#long" in a prompt raises both limits by this factor for that turn.
const LONG_FACTOR = 4
// Bash output past this many characters is cut to a head and a tail. The full text goes to a file.
const CAP_CHARS = 8000
const KEEP_CHARS = 2000
const SPILL_DIR = '/tmp/turn-discipline'
// Spilled files older than this are deleted when a session starts. /tmp also clears on reboot.
const SPILL_MAX_AGE_MINUTES = 1440
// These prompt origins are the person speaking. A task notification or a trigger is not a new turn.
const HUMAN = new Set(['composer', 'bridge', 'sdk'])

type Turn = { startedMs: number; calls: number; factor: number }

function spillPath(id: string | undefined): string {
  const safe = (id ?? String(Date.now())).replace(/[^\w-]/g, '')
  return `${SPILL_DIR}/${safe}.txt`
}

/** Cuts text to its head and tail around a marker that names the file with the whole text. */
export function cut(text: string, path: string): string {
  const omitted = text.length - 2 * KEEP_CHARS
  return (
    `${text.slice(0, KEEP_CHARS)}\n[turn-discipline: ${omitted} characters cut. ` +
    `Full output (${text.length} characters) is in ${path}. Read a range of it or grep it.]\n` +
    text.slice(-KEEP_CHARS)
  )
}

export const register: Register = on => {
  let turn: Turn = { startedMs: Date.now(), calls: 0, factor: 1 }
  let capped = 0
  let keptChars = 0

  on('session.start', async ($, e, next) => {
    const r = await next(e)
    try {
      await $.process.run(['find', SPILL_DIR, '-type', 'f', '-mmin', `+${SPILL_MAX_AGE_MINUTES}`, '-delete'])
    } catch {
      // Nothing to clean, or find is missing: a leftover file is harmless.
    }
    await $.command.register({
      name: 'budget',
      description: 'Tool calls and time used this turn, and the Bash output kept out of context (turn-discipline)',
      immediate: true,
    })
    return r
  })

  on('command.run', { command: 'budget' }, () => ({
    text:
      `${turn.calls}/${MAX_CALLS * turn.factor} calls, ` +
      `${Math.round((Date.now() - turn.startedMs) / 1000)}/${MAX_SECONDS * turn.factor}s this turn. ` +
      `${capped} Bash output${capped === 1 ? '' : 's'} cut, about ${Math.round(keptChars / 4 / 1000)}k tokens kept out of context.`,
  }))

  on('prompt.submit', ($, e, next) => {
    if (HUMAN.has(e.origin.kind) && !e.isMeta && !e.command) {
      turn = { startedMs: Date.now(), calls: 0, factor: e.text.includes('#long') ? LONG_FACTOR : 1 }
    }
    return next(e)
  }).catch(($, e, next) => next(e))

  on('tool.call', async ($, e, next) => {
    // A subagent runs its own loop under its own limits.
    if (e.agentId !== undefined) return next(e)
    turn.calls++
    const elapsed = (Date.now() - turn.startedMs) / 1000
    if (turn.calls > MAX_CALLS * turn.factor || elapsed > MAX_SECONDS * turn.factor) {
      return {
        deny:
          `turn-discipline: turn budget used up (${turn.calls} tool calls, ${Math.round(elapsed)}s; ` +
          `limit ${MAX_CALLS * turn.factor} calls or ${MAX_SECONDS * turn.factor}s). Stop now and call no more tools. ` +
          'Tell the user in 5 lines or fewer what is done, what is left, and the next slice. ' +
          'The user can reply with #long to raise the budget.',
      }
    }
    if (e.tool !== 'Bash') return next(e)

    const ran = await next(e)
    if (ran.deny !== undefined) return ran
    const out = ran.result as { stdout?: unknown; isImage?: boolean; rawOutputPath?: string } | undefined
    if (!out || typeof out.stdout !== 'string' || out.isImage || out.rawOutputPath) return ran
    if (out.stdout.length <= CAP_CHARS) return ran

    const path = spillPath(e.tool_use_id)
    try {
      await $.fs.write(path, out.stdout)
    } catch {
      return ran // Without the file the cut text would be lost, so the output stays whole.
    }
    capped++
    keptChars += out.stdout.length - 2 * KEEP_CHARS
    // A hook's own { result } carries no `ref`, so core maps this result and not the messages it made itself.
    return {
      result: { ...ran.result, stdout: cut(out.stdout, path) },
      ...(ran.context ? { context: ran.context } : {}),
      ...(ran.isError ? { isError: true as const } : {}),
    } as typeof ran
  }).catch(($, e, next) => next(e)) // Fail open: a broken guard must never block work.
}
