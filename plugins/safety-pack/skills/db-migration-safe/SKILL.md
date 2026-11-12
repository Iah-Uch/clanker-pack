---
name: db-migration-safe
description: "Use when changing a database schema or data - adding, renaming or dropping a table or column, changing a column type, writing a migration file, running a backfill, or resetting a database. Makes the change safe: backup first, small reversible steps, a dry run, and a way back."
---

# Safe database change

Data loss is the one mistake that a `git revert` does not fix. Slow down here.

## Before you write anything

1. Find out which database the command will hit. Read the connection setting. Say it out loud: "This targets <name> on <host>."
2. If it is a production or shared database, stop. Ask the user to confirm in words. Do not run migrations against it yourself unless they say so.
3. Make a backup or a snapshot first. Say where it is and how to restore it. If you cannot make one, say so and ask.

## Write the change

- Prefer additive steps: add a column, then fill it, then switch the code, then drop the old one in a later change.
- Never rename or drop in one step. A rename is: add new, copy, switch reads and writes, drop old later.
- A new `NOT NULL` column needs a default or a backfill first.
- Write the reverse migration in the same change. If it cannot reverse (a drop), say so and name the backup.
- Keep one logical change per migration file.
- Use the project's own migration tool. Do not hand-edit the database.

## Check before you run

1. Run it on a copy or a local database first. Show the result.
2. Count the rows it will touch. Report the number.
3. Run the project's tests against the migrated copy.

## Never, without explicit approval

- `DROP TABLE`, `DROP COLUMN`, `TRUNCATE`, or `DELETE` with no `WHERE`.
- A `reset`, `push --force` or `migrate reset` command of a database tool.
- A migration on a database whose backup you did not confirm.

For the wider plan, use the `rollback-plan` skill.
