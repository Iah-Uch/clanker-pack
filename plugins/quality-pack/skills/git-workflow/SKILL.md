---
name: git-workflow
description: Use when committing, branching, merging, or opening a PR — any git write operation. Covers atomic commits, conventional commit messages, the human-approval gate before committing, feature-branch flow, no-fast-forward merges, and human-only authorship. Do NOT use for read-only git inspection (log, diff, status).
metadata:
  author: Iah-Uch
  version: '1.0.0'
---

# Git Workflow

## Overview

A git discipline for humans who want a legible history. Every commit is one reviewable idea, every message says **why**, every merge preserves branch structure, and the human — not the tool — owns and approves the work.

**Core principle: the human is the author and the gatekeeper.** The agent stages and proposes; the human approves and owns. Never the other way around.

## The Non-Negotiables

1. **Never commit without explicit human approval.** Stage the changes, show the diff, then stop and wait. "Approval to make the change" is not "approval to commit it."
2. **Never attribute work to the agent.** No `Co-Authored-By: Claude`, no "Generated with" footer, no AI as commit author or PR assignee. All work is attributed to the human.
3. **Never commit directly to `main`.** Work on a `feat/` or `fix/` branch; integrate via PR.
4. **Never fast-forward a merge.** Use `git merge --no-ff` so the graph shows branch structure and the order work happened.

Violating the letter of these rules is violating the spirit of them. There is no "close enough."

## Atomic Commits

One logical change per commit. If a task touches several concerns, split it — one commit each.

- A commit should build and pass tests on its own.
- If the subject needs the word "and", it's probably two commits.
- Staging is a tool: use `git add -p` to peel one logical change out of a messy working tree.
- Reordering/squashing before a PR is fine; rewriting shared history is not.

## Conventional Commits

Format: `type: subject`

**Types:** `feat` · `fix` · `refactor` · `docs` · `chore` · `perf` · `test` · `build` · `ci` · `style`

**Subject = one sentence on _why_, not _what_.** The diff already shows what changed; the message explains the reason it changed.

**Body** only when context is genuinely needed (a non-obvious tradeoff, a subtle bug's root cause, a link to an issue). Skip it otherwise — an empty body beats a body that restates the diff.

```
# ✅ says why
fix: prevent double-charge when the payment webhook retries

# ❌ restates the diff (what, not why)
fix: add idempotency key check in webhook handler

# ✅ two concerns → two commits
feat: expose glucose-file attachment on the analysis endpoint
test: cover cross-user access denial on attachment upload

# ❌ one commit doing two things
feat: add attachment endpoint and fix unrelated pagination bug
```

## Branch & Merge Flow

1. Branch off `main`: `git switch -c feat/<slug>` (or `fix/<slug>`).
2. Commit atomically as you go.
3. Open a PR — short summary bullets + a test plan. No essays.
4. Merge with `git merge --no-ff` (or the platform's merge-commit option — never squash-to-main if it erases the atomic history, never fast-forward).

The resulting graph should read like a table of contents: each branch a feature, each merge a milestone.

## The Commit Handshake

The one interaction that matters most. Follow it every time:

```
1. Make the change.
2. git add -p   (stage exactly one logical change)
3. Show the diff + the proposed commit message.
4. STOP. Wait for explicit "yes, commit."
5. Only then: git commit.
```

## Rationalizations — STOP if you catch yourself here

| Excuse | Reality |
|--------|---------|
| "They approved the change, so committing is implied." | Approving code ≠ approving a commit. Show the diff and wait. |
| "It's a tiny one-line fix, no need to ask." | Size is irrelevant. The gate is on the action, not the diff size. |
| "A `Co-Authored-By` trailer is just being honest." | The human owns the work. No AI authorship, ever. |
| "Fast-forward is cleaner, no ugly merge bubble." | The bubble IS the information — it shows branch structure. `--no-ff`. |
| "These changes are related enough for one commit." | If the subject needs "and", split it. |
| "Committing straight to main saves a PR round-trip." | Never. Branch + PR, no exceptions. |
| "I'll write a detailed body to be thorough." | A body that restates the diff is noise. Why-only, or nothing. |

## Red Flags — you're about to break the discipline

- About to run `git commit` without having shown the diff and gotten a "yes."
- Typing `Co-Authored-By`, `Generated with`, or adding an AI as assignee.
- On `main` and about to commit.
- Reaching for `git merge` without `--no-ff`, or letting a fast-forward happen.
- A commit subject containing "and", or describing _what_ changed instead of _why_.

**All of these mean: stop and go back to the rule.**
