---
name: ship-checklist
description: Use before you say a feature is done, before a commit or push, before a deploy, or when the user says "ship it", "is this ready", "can I publish this" or "check my work". Checks the diff for leaked secrets, missing auth, unvalidated input, unsafe dependencies and missing tests. Reports each result in plain language.
---

# Ship checklist

Run this before you call work done. The reader may not read code, so report in plain words.

## Steps

1. Run `git status` and `git diff` (staged and unstaged). Work from the real diff. Do not work from memory.
2. Check each item below against the diff. Mark each one PASS, FAIL or NOT APPLICABLE.
3. Fix every FAIL that is inside the scope of the task. Report every FAIL that is outside it.
4. Run the project's test, lint and type-check commands once. Report the real output.
5. Give the report in the format at the end.

## Items

| # | Check | FAIL when |
|---|-------|-----------|
| 1 | Secrets | A key, token, password or private URL is in a changed file or in the history of this change. |
| 2 | Env files | `.env` or a key file is not in `.gitignore`, or it is staged. |
| 3 | Auth | A new route, API handler or server action has no check of who is calling. |
| 4 | Ownership | A handler reads or writes a record by id without checking that the caller owns it. |
| 5 | Input | User input reaches a database query, a shell command, a file path or HTML without validation or escaping. |
| 6 | Errors | An error message shows a stack trace, a query or a secret to the user. |
| 7 | Dependencies | A new package is unknown, unmaintained or has a known advisory. Run the project's audit command if one exists. |
| 8 | Tests | New behavior has no test, or a test was deleted or weakened to pass. |
| 9 | Debug leftovers | `console.log`, `print`, `debugger`, a test bypass or a hard-coded test user is in the diff. |
| 10 | Rollback | The change cannot be undone with one `git revert`. If a migration is involved, use the `rollback-plan` skill. |

## Report format

- One line first: "Ready to ship", "Ready after the fixes below" or "Not ready".
- Then a short list of FAIL items. For each one, say what is wrong, where, and what it could cause. Use no jargon.
- Then one line on what you ran and what you could not run.

Do not say "ready" if you skipped an item. Name the skipped item instead.
