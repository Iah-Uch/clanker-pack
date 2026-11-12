---
name: git-safety-net
description: Use before a large edit, refactor, rename across many files, bulk change, multi-file change or risky experiment in a git repository, especially when uncommitted edits exist, or when the user says "don't break anything", "I'm scared of losing my work" or "undo that". Sets a checkpoint so any change can be undone, and keeps work off the main branch.
---

# Git safety net

Make the work undoable before you start. Use git. Add no other tool.

## Before a large change

1. Run `git status`. If the working tree has changes the user did not ask you to touch, tell them. Do not mix them into your work.
2. Check the branch with `git branch --show-current`. If it is the default branch (`main` or `master`), create a branch first: `git switch -c <type>/<short-name>`.
3. Make a checkpoint of the starting point so you can return to it. Prefer a branch or tag: `git tag checkpoint/<short-name>`. A tag changes nothing in the history and costs nothing.
4. Tell the user the checkpoint name and the one command that returns to it.

## During the change

- Work in small steps. After each working step, tell the user it is a good point to commit. Commit only when the user approves.
- Do not run `git reset --hard`, `git checkout -- .`, `git clean -fd` or `git push --force` unless the user asks. They destroy work that has no copy.
- Do not rewrite history that has been pushed.

## To undo

| Goal | Command |
|------|---------|
| See what changed since the checkpoint | `git diff checkpoint/<short-name>` |
| Undo one commit, keep history | `git revert <hash>` |
| Throw away the branch and go back | `git switch main`, then `git branch -D <branch>` (confirm with the user first) |
| Recover a lost commit | `git reflog`, then `git switch -c rescue <hash>` |

Before any command that deletes work, say what it deletes and ask.

For the wider plan, use the `rollback-plan` skill.
