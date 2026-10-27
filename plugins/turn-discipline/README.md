# turn-discipline

A Claude Code mod and a setup skill that keep sessions short, cheap and on target.

## What it does

- **Turn budget.** A turn is one prompt from you and everything Claude does before it answers. Past 40 tool calls or 10 minutes, every tool call is denied, and Claude has to stop and report what is done and what is left. Put `#long` in a prompt to raise both limits four times for that turn. A subagent has its own limits.
- **Output cap.** Bash output over 8,000 characters is cut to its first and last 2,000 characters. The full text goes to a file under `/tmp/turn-discipline/`, and the cut text names it, so Claude can read a range instead of repeating the command. Files older than 24 hours are deleted when a session starts, and `/tmp` clears on reboot.
- **Rules section.** Adds a short block to the system prompt: read the intent behind a broad request and state it as a sharp spec before acting, size the job, batch independent calls, edit instead of rewriting, and stop when the budget is gone.
- **Setup skill.** `speed-setup` checks effort and compaction settings and runs a plan one slice at a time, each slice in a fresh context.

## Commands

| Command | Effect |
|---|---|
| `/budget` | Show calls and seconds used this turn, and the Bash output kept out of context. |

## Why these three

Research on coding agents finds that tool output is most of the context, that old output can be dropped with little loss when the agent can get it back, and that fewer model calls cut latency most. Pipelines of small steps cost less than one open-ended loop. Sources: [The Complexity Trap](https://arxiv.org/abs/2508.21433), [AgentDiet](https://arxiv.org/abs/2509.23586), [Hidden Costs of Forgetting](https://arxiv.org/abs/2610.35496), [LLMCompiler](https://arxiv.org/abs/2312.04511), [Agentless](https://huggingface.co/papers/2407.01489).

## Limits

- The output cap applies to new Bash output. It does not shrink old turns.
- The budget counts the main thread only.
- The 40-call and 10-minute limits are fixed in `hooks/register.ts`.

## Reach

A mod runs unsandboxed and sees the whole session. This one calls `$.command`, `$.fs.write` and `$.process.run`. The only file it writes is the spilled Bash output under `/tmp/turn-discipline/`. The only process it runs is `find /tmp/turn-discipline -type f -mmin +1440 -delete`. Read `hooks/register.ts` before you install it.

## Install

```
/plugin marketplace add Iah-Uch/clanker-pack
/plugin install turn-discipline@clanker-pack
```

## License

MIT. See `LICENSE`.
