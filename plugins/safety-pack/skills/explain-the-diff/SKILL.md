---
name: explain-the-diff
description: Use when the user asks "what did you change", "what did you just do", "explain this diff", "is this safe to accept" or "what could break", or when a change touches many files and the user does not read code. Explains the real diff in plain language, with the risk of each change.
---

# Explain the diff

The reader decides whether to accept your changes. They may not read code. Give them enough to decide.

## Steps

1. Run `git status --short`, `git diff` and `git diff --staged`. New files do not show in `git diff`, so read each untracked file too. Read the real changes. Do not describe them from memory.
2. Group the changes by purpose, not by file. One group is one reason for change.
3. For each group, write the three parts below.
4. Finish with the verdict.

## Each group

- **What changed:** one sentence in plain words. Name the feature, not the function.
- **Why:** one sentence that links it to the request.
- **Risk:** what could break, who would notice, and how to undo it. Write "low" only when you checked.

## Verdict

- List anything you changed that the user did not ask for. Offer to revert it.
- List anything that deletes data, changes a permission, changes a dependency or touches money, login or personal data. Put these first.
- Say what you tested and what you did not.

## Rules

- No jargon without a one-line meaning in brackets.
- Short sentences. One idea each.
- Do not praise the change. Do not hide a doubt.
