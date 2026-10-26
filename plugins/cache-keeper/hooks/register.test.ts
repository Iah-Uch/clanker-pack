import { expect, mock, test } from 'claude-code/testing'

const HOUR = 60 * 60 * 1000
const USAGE = { input_tokens: 10, output_tokens: 5, cache_read_input_tokens: 200000, cache_creation_input_tokens: 0 }

async function warmSession($: any, on: any, clock: ReturnType<typeof mock.clock>, logs: string[] = [], liveTokens: () => number = () => 200000) {
  on('ui.status', () => ({ value: undefined }))
  on('ui.log', (_: any, e: any) => {
    logs.push(String(e.text ?? e.message ?? JSON.stringify(e)))
    return { value: undefined }
  })
  on('turn.step', async function* (_: any, e: any) {
    return { turnId: e.turnId, index: e.index, answer: '', toolUses: [], stopReason: 'end_turn', usage: null }
  })
  on('turn.complete', () => ({ text: '' }))
  on('session.model', () => ({ value: 'claude-sonnet-5-5' }))
  on('session.usage', () => ({ value: { context: { tokens: liveTokens(), window: 1000000, percent: 20 }, startedAt: 0 } }))
  on('command.register', () => ({ value: { command: 'keepwarm' } }))
  on('session.start', (_: any, e: any) => ({ cwd: e.cwd }))
  await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
  // One main turn at time 0 puts a 200k-token context in the cache.
  await $.turn.step({ turnId: 't1', index: 0, model: 'claude-sonnet-5-5', messageCount: 10 })
  await $.turn.complete({ turnId: 't1', answer: '', reason: 'answer', isAborted: false, durationMs: 1000, usage: { ...USAGE, model: 'claude-sonnet-5-5' } })
  await clock.settle()
}

test('a cold send is refused once with its price, the resend goes through', async ($, on) => {
  const clock = mock.clock(on, { now: 10_000_000 })
  on('prompt.submit', (_, e) => ({ text: e.text }))
  await warmSession($, on, clock)

  await clock.advance(HOUR + 60_000)
  const first = await $.prompt.submit({ text: 'recap', origin: { kind: 'composer' } })
  expect(String(first.drop)).toContain('$0.80')

  const second = await $.prompt.submit({ text: 'recap', origin: { kind: 'composer' } })
  expect(second.drop).toBeUndefined()
})

test('a warm send goes through untouched', async ($, on) => {
  const clock = mock.clock(on, { now: 10_000_000 })
  on('prompt.submit', (_, e) => ({ text: e.text }))
  await warmSession($, on, clock)

  await clock.advance(10 * 60_000)
  const sent = await $.prompt.submit({ text: 'recap', origin: { kind: 'composer' } })
  expect(sent.drop).toBeUndefined()
})

test('auto mode pings after 50 idle minutes with no command, and off stops it', async ($, on) => {
  const clock = mock.clock(on, { now: 10_000_000 })
  let forks = 0
  on('model.fork', () => {
    forks++
    return { value: { isAnswered: true, text: 'warm', usage: USAGE } }
  })
  on('command.run', () => ({ text: '' }))
  on('prompt.submit', (_, e) => ({ text: e.text }))
  await warmSession($, on, clock)

  await clock.advance(51 * 60_000)
  expect(forks).toBe(1)

  // The ping refreshed the cache, so a send 70 minutes after the turn is still warm.
  await clock.advance(19 * 60_000)
  const sent = await $.prompt.submit({ text: 'recap', origin: { kind: 'composer' } })
  expect(sent.drop).toBeUndefined()
})

test('off stops the pings and keeps auto from re-arming', async ($, on) => {
  const clock = mock.clock(on, { now: 10_000_000 })
  let forks = 0
  on('model.fork', () => {
    forks++
    return { value: { isAnswered: true, text: 'warm', usage: USAGE } }
  })
  on('command.run', () => ({ text: '' }))
  on('prompt.submit', (_, e) => ({ text: e.text }))
  await warmSession($, on, clock)

  await $.command.run({ command: 'keepwarm', args: 'off' })
  await clock.advance(3 * 60 * 60_000)
  expect(forks).toBe(0)
})

const BREAK_USAGE = { input_tokens: 10, output_tokens: 5, cache_read_input_tokens: 31000, cache_creation_input_tokens: 110000, model: 'claude-sonnet-5-5' }

async function turnWith($: any, clock: ReturnType<typeof mock.clock>, usage: typeof BREAK_USAGE) {
  for await (const c of $.turn.step({ turnId: 't2', index: 0, model: 'claude-sonnet-5-5', messageCount: 12 })) void c
  await $.turn.complete({ turnId: 't2', answer: '', reason: 'answer', isAborted: false, durationMs: 1000, usage })
  await clock.settle()
}

test('a large write minutes after the last request is a cache break, not a cold write', async ($, on) => {
  const clock = mock.clock(on, { now: 10_000_000 })
  const logs: string[] = []
  on('prompt.submit', (_, e) => ({ text: e.text }))
  await warmSession($, on, clock, logs)

  await clock.advance(5 * 60_000)
  await turnWith($, clock, BREAK_USAGE)
  expect(logs.some(l => l.includes('cache break: 110'))).toBe(true)
  expect(logs.some(l => l.includes('Keeping the cache warm'))).toBe(false)
})

test('a large write after the cache expired is still a cold write', async ($, on) => {
  const clock = mock.clock(on, { now: 10_000_000 })
  const logs: string[] = []
  on('prompt.submit', (_, e) => ({ text: e.text }))
  on('model.fork', () => ({ value: { isAnswered: false, text: '', usage: null } }))
  await warmSession($, on, clock, logs)
  await $.command.run({ command: 'keepwarm', args: 'off' })

  await clock.advance(HOUR + 60_000)
  await turnWith($, clock, BREAK_USAGE)
  expect(logs.some(l => l.includes('cold write of'))).toBe(true)
})

test('a rewrite under half the context is still a break when the read fell away', async ($, on) => {
  const clock = mock.clock(on, { now: 10_000_000 })
  const logs: string[] = []
  on('prompt.submit', (_, e) => ({ text: e.text }))
  await warmSession($, on, clock, logs)

  await clock.advance(5 * 60_000)
  await turnWith($, clock, { ...BREAK_USAGE, cache_read_input_tokens: 31000, cache_creation_input_tokens: 89000 })
  expect(logs.some(l => l.includes('cache break: 89'))).toBe(true)
})

test('new content on a warm cache is not a break', async ($, on) => {
  const clock = mock.clock(on, { now: 10_000_000 })
  const logs: string[] = []
  on('prompt.submit', (_, e) => ({ text: e.text }))
  await warmSession($, on, clock, logs)

  await clock.advance(5 * 60_000)
  await turnWith($, clock, { ...BREAK_USAGE, cache_read_input_tokens: 190000, cache_creation_input_tokens: 40000 })
  expect(logs.some(l => l.includes('cache break') || l.includes('cold write'))).toBe(false)
})

test('a compaction no hook reported stops the pings: the live context shrank', async ($, on) => {
  const clock = mock.clock(on, { now: 10_000_000 })
  let forks = 0
  let live = 200000
  on('model.fork', () => {
    forks++
    return { value: { isAnswered: true, text: 'warm', usage: USAGE } }
  })
  on('command.run', () => ({ text: '' }))
  on('prompt.submit', (_, e) => ({ text: e.text }))
  await warmSession($, on, clock, [], () => live)

  // The summary replaced the conversation while the mod saw no session.compact.
  live = 8000
  await clock.advance(55 * 60_000)
  expect(forks).toBe(0)
})
