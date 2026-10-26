# reread-guard

A Claude Code mod that refuses a repeat `Read` of a large file that has not changed, so its text is not added to the context twice.

Some builds of Claude Code return the full text on every `Read`, even when the same range was read a moment ago.

## What it does

- Refuses a `Read` of an unchanged file of 8 KB or more, with the same range, that this agent already read.
- Lets a second identical `Read` through, in case the text has left the context.
- Forgets a file when it is edited or written, and forgets everything after a compaction.
- Keeps each subagent's reads separate, because a subagent has its own context.

A different range, a changed modification time, a changed size and a small file are never refused.

## Commands

| Command | Effect |
|---|---|
| `/reread` | Show how many reads were refused and about how many tokens they kept out of context. |

## Limits

- It detects a compaction from `session.compact`, and from a drop in the message count when another plugin hides that event.
- The token figure is an estimate of four bytes per token.

## Reach

A mod runs unsandboxed and sees the whole session. This one calls only `$.fs.stat` and `$.command`. It reads no file content. Read `hooks/register.ts` before you install it.

## Install

```
/plugin marketplace add Iah-Uch/clanker-pack
/plugin install reread-guard@clanker-pack
```

## License

MIT. See `LICENSE`.
