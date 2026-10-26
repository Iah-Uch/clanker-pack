import { expect, test } from 'claude-code/testing'

const FILE = '/repo/big.ts'

async function start($: any, on: any, stat: () => { size: number; mtimeMs: number }) {
  on('command.register', () => ({ value: { command: 'reread' } }))
  on('session.start', (_: any, e: any) => ({ cwd: e.cwd }))
  on('fs.stat', () => ({ value: { kind: 'file', isLink: false, ...stat() } }))
  on('tool.call', () => ({ result: {} }))
  await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
}

test('a repeat read of an unchanged large file is refused once, the retry goes through', async ($, on) => {
  await start($, on, () => ({ size: 40000, mtimeMs: 1 }))

  const first = await $.tool.call({ tool: 'Read', file_path: FILE })
  expect(first.deny).toBeUndefined()

  const second = await $.tool.call({ tool: 'Read', file_path: FILE })
  expect(String(second.deny)).toContain('already in your context')

  const third = await $.tool.call({ tool: 'Read', file_path: FILE })
  expect(third.deny).toBeUndefined()
})

test('a changed file, another range or an edit in between is read again', async ($, on) => {
  let mtimeMs = 1
  await start($, on, () => ({ size: 40000, mtimeMs }))

  await $.tool.call({ tool: 'Read', file_path: FILE })
  const otherRange = await $.tool.call({ tool: 'Read', file_path: FILE, offset: 100, limit: 50 })
  expect(otherRange.deny).toBeUndefined()

  mtimeMs = 2
  const changed = await $.tool.call({ tool: 'Read', file_path: FILE })
  expect(changed.deny).toBeUndefined()

  await $.tool.call({ tool: 'Edit', file_path: FILE, old_string: 'a', new_string: 'b' })
  const afterEdit = await $.tool.call({ tool: 'Read', file_path: FILE })
  expect(afterEdit.deny).toBeUndefined()
})

test('a request over far fewer messages is read as a compaction and the file is read again', async ($, on) => {
  on('turn.step', async function* (_: any, e: any) {
    return { turnId: e.turnId, index: e.index, answer: '', toolUses: [], stopReason: 'end_turn', usage: null }
  })
  await start($, on, () => ({ size: 40000, mtimeMs: 1 }))
  const step = async (turnId: string, messageCount: number) => {
    for await (const c of $.turn.step({ turnId, index: 0, model: 'claude-sonnet-5-5', messageCount })) void c
  }

  await step('t1', 60)
  await $.tool.call({ tool: 'Read', file_path: FILE })
  await step('t2', 62)
  const refused = await $.tool.call({ tool: 'Read', file_path: FILE })
  expect(String(refused.deny)).toContain('already in your context')

  await $.tool.call({ tool: 'Read', file_path: FILE })
  await step('t3', 3)
  const afterSummary = await $.tool.call({ tool: 'Read', file_path: FILE })
  expect(afterSummary.deny).toBeUndefined()
})

test('a small file is never refused',async ($, on) => {
  await start($, on, () => ({ size: 500, mtimeMs: 1 }))

  await $.tool.call({ tool: 'Read', file_path: FILE })
  const again = await $.tool.call({ tool: 'Read', file_path: FILE })
  expect(again.deny).toBeUndefined()
})
