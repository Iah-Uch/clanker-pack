# Changelog

## Unreleased

### Added
- `safety-pack` 0.1.0: six skills (`ship-checklist`, `explain-the-diff`, `db-migration-safe`, `rollback-plan`, `git-safety-net`, `deploy-recipes`) and three hooks (destructive-command guard, secret scan, context watchdog), with unit tests.
- `recommended-core` 0.1.0 (5 plugins, no extra binary), `recommended-extras` 0.1.0 (9 optional plugins) and `recommended-memory` 0.1.0 (`ai-memory`, needs its binary). `recommended-pack` is unchanged and still installs all 15.
- Eval cases for `safety-pack`, `stack-pack`, `ui-pack` and `tools-pack`, run with `claude plugin eval`.
- `scripts/cost.py`, which measures the skill-listing text each plugin adds to a session.
- Quick-start section and a cost table in the README.
- `benchmarks/`: runs an agent in seeded project folders with the skill absent, installed and named, and reports the 19 skills whose named-skill runs all passed. It also has a hook benchmark.

### Changed
- `ui-pack` 1.4.0: `tailwind-patterns` loads on matching files only. `improve-animations` is manual only (`/improve-animations`).
- `stack-pack` 1.2.0: `docker-expert` loads on matching files only.
- `scripts/check.py` counts `when_to_use` toward the 1,536-character cap and validates `paths`.
