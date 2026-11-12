---
name: rollback-plan
description: Use before a risky or hard-to-undo change - a deploy, a migration, a dependency upgrade, a large refactor, a config or environment change - or when the user asks "how do I undo this", "what if it breaks" or "is there a way back". Writes a short rollback plan and checks that the way back works.
---

# Rollback plan

Write the way back before you take the step forward.

## Steps

1. Name the change in one sentence.
2. Find what the change touches. Mark each as code, data, config, an external service or a dependency.
3. For each one, write how to undo it. Use the table below.
4. State the point of no return, if there is one. Name the step after which the undo no longer works.
5. Check that the undo is real: the branch exists, the backup file exists, the previous version tag exists.
6. Give the plan to the user as a short numbered list.

## Undo by type

| Touches | Way back | Check |
|---------|----------|-------|
| Code | `git revert` of the merge or commit. Work on a branch. | The branch or commit hash exists. |
| Dependencies | Restore the lockfile from git. Reinstall. | The old lockfile is in git history. |
| Data | Restore from a backup taken before the change. | The backup file exists and has a size. |
| Config or env | Keep the old value in the plan. Restore it. | The old value is written down. |
| Deploy | Redeploy the previous version or use the host's rollback. | The previous version is still available. |
| External service | Note the manual undo, or say that none exists. | The user knows. |

## Rules

- If a change has no undo, say so before you start. Let the user decide.
- Take the smallest step that gives a useful result. Check it. Then take the next one.
- Do not mix a risky change with an unrelated one. Keep each one separate so each can be undone alone.
- After the change, run the checks that prove it works. Then say whether to keep the undo plan ready or drop it.

For database changes, also use the `db-migration-safe` skill.
