import type { Register } from 'claude-code'

// Below this a repeat read costs less than the refused call and the retry.
const MIN_BYTES = 8000
// About four bytes per token for source text.
const BYTES_PER_TOKEN = 4

type Seen = { mtimeMs: number; size: number; refused: boolean }

function keyOf(agentId: string | undefined, path: string, offset?: number, limit?: number): string {
  return `${agentId ?? ''}\u0000${path}\u0000${offset ?? ''}\u0000${limit ?? ''}`
}

function refusal(path: string): string {
  return `reread-guard: ${path} has not changed since you read it, with the same range, earlier in this session, so its text is already in your context. ` +
    'Use that text. If you no longer have it, repeat the same Read once and it goes through.'
}

export const register: Register = on => {
  // What each agent has read, keyed by agent, path and range. A subagent has its own context.
  const seen = new Map<string, Seen>()
  let refused = 0
  let savedBytes = 0
  let mainMessages = 0

  /** An edit changes the file under every range and every agent. */
  function forget(path: string) {
    for (const key of seen.keys()) if (key.split('\u0000')[1] === path) seen.delete(key)
  }

  on('session.start', async ($, e, next) => {
    const r = await next(e)
    await $.command.register({
      name: 'reread',
      description: 'Re-reads refused this session and the tokens they kept out of context (reread-guard)',
      immediate: true,
    })
    return r
  })

  on('command.run', { command: 'reread' }, () => ({
    text: `reread-guard: ${refused} repeat read${refused === 1 ? '' : 's'} refused, about ${Math.round(savedBytes / BYTES_PER_TOKEN / 1000)}k tokens kept out of context`,
  }))

  on('tool.call', { tool: 'Read' }, async ($, e, next) => {
    if (e.pages !== undefined) return next(e)
    const stat = await $.fs.stat(e.file_path).catch(() => null)
    if (!stat || stat.kind !== 'file' || stat.size < MIN_BYTES) return next(e)
    const key = keyOf(e.agentId, e.file_path, e.offset, e.limit)
    const prev = seen.get(key)
    if (prev && prev.mtimeMs === stat.mtimeMs && prev.size === stat.size && !prev.refused) {
      // One refusal per read. A second try means the text left the context, so it goes through.
      prev.refused = true
      refused++
      savedBytes += stat.size
      return { deny: refusal(e.file_path) }
    }
    const result = await next(e)
    if (result.deny === undefined && !result.isError) seen.set(key, { mtimeMs: stat.mtimeMs, size: stat.size, refused: false })
    return result
  })

  on('tool.call', { tool: 'Edit' }, async (_, e, next) => {
    forget(e.file_path)
    return next(e)
  })

  on('tool.call', { tool: 'Write' }, async (_, e, next) => {
    forget(e.file_path)
    return next(e)
  })

  on('tool.call', { tool: 'NotebookEdit' }, async (_, e, next) => {
    forget(e.notebook_path)
    return next(e)
  })

  // A managed plugin can end session.compact before it reaches this mod. A request over fewer than half
  // the last one's messages is a compaction summary, not a rewind.
  on('turn.step', async function* (_, e, next) {
    if (e.agentId === undefined) {
      if (e.messageCount * 2 < mainMessages) seen.clear()
      mainMessages = e.messageCount
    }
    return yield* next(e)
  })

  // A summary replaces the text the reads put in context.
  on('session.compact', async (_, e, next) => {
    const r = await next(e)
    if (!e.agentId) {
      seen.clear()
      mainMessages = 0
    }
    return r
  })

  on('session.end', async (_, e, next) => {
    if (e.reason === 'clear' || e.reason === 'resume') seen.clear()
    return next(e)
  })
}
