# Benchmarks

Two tests live here. Both need the `codex` CLI, logged in. They cost plan allowance, not cash.

## Skill benchmark

An agent works in a seeded project folder in a clean `HOME`. Three arms:

- `bare`: the skill is absent.
- `natural`: the skill is installed and the agent decides whether to use it.
- `forced`: the skill is installed and the prompt names it.

A grader inspects the project state and the planted facts, never the skill's own wording. The `generative-pack` cases give a problem with no technique named and check that the answer names the right project or one on the same topic.

```
python3 benchmarks/run.py --only <text> --runs 2
python3 benchmarks/report.py benchmarks/results/skills
BENCH_TEXT_ONLY=1 python3 benchmarks/run.py ...   # read-only, short answers, cheap
```

| File | Job |
|---|---|
| `fixtures.py` | Seeded project folders with planted traps |
| `cases.py` | One case per skill: prompt and grader |
| `catalog.py` | Reads the generative skills' catalogs, builds problems and checks licenses |
| `run.py` | Runs the cases through `codex exec`, saves answer, project diff, events, record |
| `report.py` | Writes `REPORT.md` from `records.json` |

Report: [results/skills/REPORT.md](results/skills/REPORT.md).

## Hook benchmark

`hooks_bench.py` feeds labelled commands, file contents and transcripts to the `safety-pack` hooks. Free. Results: `results/hooks/hooks_results.json`.

## What is and is not here

- The report lists only skills whose `forced` runs all passed (19 of 28). The other skills were tested, and their cases, fixtures and results were removed. The list shows what worked, not everything tested.
- Several listed skills also pass `bare`. The model already does that task alone, so the skill adds little there.

## Limits

- Codex is not Claude Code. Skill triggering may differ.
- 1 to 3 runs per cell. A one-run gap is noise.
- The author wrote the prompts and the graders. Some skills were edited after seeing results, so those cases are not held out.
- The `generative-pack` cases ran text-only, 1 run per arm, with no `natural` arm.
- `reread-guard` is not covered: its tests need the Claude Code mod runtime.
- Every output is text, so the saved answers are the proof. There are no screenshots.
