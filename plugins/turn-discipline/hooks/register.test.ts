import { expect, test } from 'claude-code/testing'

const BIG = 'x'.repeat(20000)

async function start($: any, on: any, answer: () => unknown = () => ({})) {
  on('command.register', () => ({ value: { command: 'budget' } }))
  on('session.start', (_: any, e: any) => ({ cwd: e.cwd }))
  on('fs.write', () => ({ value: undefined }))
  on('tool.call', () => ({ result: answer() }))
  await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
}

test('the 41st tool call in a turn is denied with an instruction to stop', async ($, on) => {
  await start($, on)
  for (let i = 0; i < 40; i++) {
    const r = await $.tool.call({ tool: 'Read', file_path: '/a' })
    expect(r.deny).toBeUndefined()
  }
  const over = await $.tool.call({ tool: 'Read', file_path: '/a' })
  expect(String(over.deny)).toContain('turn budget used up')
})

test('a new prompt from the person resets the count, and #long raises the limit', async ($, on) => {
  on('prompt.submit', (_: any, e: any) => ({ text: e.text }))
  await start($, on)
  for (let i = 0; i < 41; i++) await $.tool.call({ tool: 'Read', file_path: '/a' })

  await $.prompt.submit({ text: 'go on', origin: { kind: 'composer' } })
  expect((await $.tool.call({ tool: 'Read', file_path: '/a' })).deny).toBeUndefined()

  await $.prompt.submit({ text: 'big job #long', origin: { kind: 'composer' } })
  for (let i = 0; i < 100; i++) expect((await $.tool.call({ tool: 'Read', file_path: '/a' })).deny).toBeUndefined()
})

test('a task notification does not reset the count', async ($, on) => {
  on('prompt.submit', (_: any, e: any) => ({ text: e.text }))
  await start($, on)
  for (let i = 0; i < 41; i++) await $.tool.call({ tool: 'Read', file_path: '/a' })

  await $.prompt.submit({ text: 'notice', origin: { kind: 'task-notification' } })
  expect(String((await $.tool.call({ tool: 'Read', file_path: '/a' })).deny)).toContain('turn budget')
})

test('huge Bash output is cut to a head and a tail and points at the saved file', async ($, on) => {
  await start($, on, () => ({ stdout: BIG, stderr: '', interrupted: false }))
  const r = await $.tool.call({ tool: 'Bash', command: 'cat big' })
  const text = (r.result as { stdout: string }).stdout
  expect(text.length).toBeLessThan(5000)
  expect(text).toContain('/tmp/turn-discipline/')
  expect(text).toContain('16000 characters cut')
})

test('small Bash output passes through untouched', async ($, on) => {
  await start($, on, () => ({ stdout: 'ok', stderr: '', interrupted: false }))
  const r = await $.tool.call({ tool: 'Bash', command: 'echo ok' })
  expect((r.result as { stdout: string }).stdout).toBe('ok')
})
