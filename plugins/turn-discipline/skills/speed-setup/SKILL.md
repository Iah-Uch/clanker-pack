---
name: speed-setup
description: "Use when Claude Code sessions are slow or expensive, when the user asks to set up turn budgets, effort or compaction defaults, or a plan runner that works one slice at a time, or when a big job needs to be split into small fresh-context runs. Checks the settings the turn-discipline mod relies on, applies them with consent, and runs a plan slice by slice."
---

# Speed setup

The turn-discipline mod enforces a budget of tool calls and time per prompt and cuts huge Bash output. This skill sets the rest of the stack to match and runs big jobs as small ones.

## 1. Check the settings

Read `~/.claude/settings.json` and report these three values:

| Key | Fast default | Why |
|---|---|---|
| `effortLevel` | `low` | Adaptive thinking is the largest hidden output cost. Use `/effort high` only to plan. |
| `modelSettings.<model>.autoCompactWindow` | `200000` | Quality drops in long contexts, and a smaller window caps cost. Set it with `/autocompact 200k`. |
| `hooks` | no duplicate budget hook | The mod already counts calls. Remove any older hand-made guard hook. |

Ask before changing a value. Apply with Edit on the file, or tell the user which slash command to run.

## 2. Turn a big job into slices

1. Write a plan file, for example `docs/PLAN.md`. One slice per line, each small enough for under 15 tool calls: `- [ ] what to change, in which files, done when`.
2. Run `scripts/run-slices.sh docs/PLAN.md --dry-run` to see the first slice.
3. Run `scripts/run-slices.sh docs/PLAN.md`. Each slice runs in a fresh `claude -p` with low effort, a 15-minute timeout and a dollar cap. It stops at the first slice that fails or does not tick its own box.
4. Set `GATE_CMD` to the project's lint and test command. It runs once, after the last slice.

Env: `SLICE_MODEL` (default `sonnet`), `SLICE_EFFORT` (`low`), `SLICE_TIMEOUT` (`900`), `SLICE_BUDGET_USD` (`2`), `GATE_CMD`.

Run slices one at a time. Do not run them in parallel: cost rises with every extra run.

## 3. Check it works

Run `/budget` in the session. It shows calls and seconds used this turn, and how much Bash output was kept out of context. If the command is missing, the mod is not installed: `/plugin install turn-discipline@clanker-pack`.
