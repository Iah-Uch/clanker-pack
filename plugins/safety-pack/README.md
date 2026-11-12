# safety-pack

Guardrails for work you cannot fully review. It has six skills that Claude loads by itself and three hooks that run on their own. It needs `python3` on your `PATH`. It needs no other install.

```
/plugin install safety-pack@clanker-pack
```

## Skills

| Skill | Claude uses it when |
|---|---|
| `ship-checklist` | You say "ship it" or "is this ready", or Claude is about to say work is done. Checks the diff for secrets, auth, input, dependencies and tests. |
| `explain-the-diff` | You ask what Claude changed. Explains the real diff in plain words, with the risk of each change. |
| `db-migration-safe` | A schema or data change is in play. Backup first, small reversible steps, a dry run. |
| `rollback-plan` | A change is risky or hard to undo. Writes the way back and checks that it exists. |
| `git-safety-net` | A large edit is about to start. Branch and checkpoint tag first. |
| `deploy-recipes` | You want to put an app online. Pre-deploy gate, secret rules, post-deploy check. It does not hold provider commands, so Claude reads the host's current docs. |

## Hooks

| Hook | Event | What it does |
|---|---|---|
| `guard_bash.py` | `PreToolUse` on `Bash` | Denies commands that wipe a system or disk, and a force push to `main`, `master`, `production`, `prod` or `release`. Asks you before `rm -rf` of real directories, `git reset --hard`, `git clean -f`, other force pushes, SQL `DROP`, `TRUNCATE` and `DELETE` with no `WHERE`, and database reset commands. |
| `secret_scan.py` | `PreToolUse` on `Write`, `Edit`, `MultiEdit` | Denies content that holds a known key shape or a hard-coded credential. The message gives the kind and the line number, never the secret. Files that end in `.example`, `.sample`, `.template` or `.dist` are skipped. Add `secret-scan: allow` to the content to skip a known fake. |
| `context_watchdog.py` | `UserPromptSubmit` | At 250k tokens of context, and again at each 100k above, tells Claude to warn you and suggest a fresh session. Set `CLANKER_WATCHDOG_TOKENS` to change the threshold. |

## Limits

- `guard_bash.py` matches the command text. It is a seat belt, not a sandbox. A command built from variables or a script can pass it.
- `secret_scan.py` checks what Claude writes through the file tools. It does not check a file that a shell command writes.
- The watchdog reads the last assistant usage in the transcript. It can lag one turn behind.

## Tests

```
python3 -m unittest plugins/safety-pack/hooks/test_hooks.py
```
