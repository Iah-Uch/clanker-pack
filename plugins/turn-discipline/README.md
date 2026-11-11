# turn-discipline

A setup skill that keeps Claude Code sessions short, cheap and on target.

## What it does

`speed-setup` does three things:

1. Checks `effortLevel` and the auto-compact window in `~/.claude/settings.json`, and changes them after you agree.
2. Adds a short "Turn discipline" rules block to your `CLAUDE.md` (read intent first, size the job, batch calls).
3. Runs a plan one slice at a time, each slice in a fresh `claude -p` context, with `scripts/run-slices.sh`.

## Why slices

Research on coding agents finds that pipelines of small steps cost less than one open-ended loop. Sources: [The Complexity Trap](https://arxiv.org/abs/2508.21433), [Agentless](https://huggingface.co/papers/2407.01489).

## Limits

- The skill sets defaults. It does not enforce them. For output that floods the context, install `context-mode` from `recommended-pack`.
- `run-slices.sh` runs one slice at a time and stops at the first slice that fails.

## Install

```
/plugin marketplace add Iah-Uch/clanker-pack
/plugin install turn-discipline@clanker-pack
```

## License

MIT. See `LICENSE`.
