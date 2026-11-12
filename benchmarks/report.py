#!/usr/bin/env python3
"""Write REPORT.md for a results folder from records.json and the saved per-run files.

Usage (repo root):  python3 benchmarks/report.py DIR
"""

import collections
import json
import os
import re
import sys

ARMS = ("bare", "natural", "forced")
GENERATIVE = re.compile(r"^(?P<skill>[a-z-]+)-(?P<n>\d)$")
PACKS = {"safety-pack": "Safety", "ui-pack": "UI", "stack-pack": "Stack", "turn-discipline": "Turn discipline",
         "tools-pack": "Tools", "generative-pack": "Generative"}


def skill_of(case_id):
    match = GENERATIVE.match(case_id)
    return match.group("skill") if match else case_id


def rate(runs, key="passed"):
    return f"{sum(bool(r[key]) for r in runs)}/{len(runs)}" if runs else "n/a"


def mean_tokens(runs):
    return f"{round(sum(r['tokens'] for r in runs) / len(runs) / 1000):,}k" if runs else "n/a"


def excerpt(path, size=700):
    text = open(path, encoding="utf-8").read().strip().replace("```", "'''")
    return text[:size] + (" ..." if len(text) > size else "")


def main() -> int:
    out = sys.argv[1]
    records = json.load(open(os.path.join(out, "records.json")))
    cases = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in records:
        cases[r["id"]][r["arm"]].append(r)
    skills = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in records:
        skills[skill_of(r["id"])][r["arm"]].append(r)
    plugin_of = {}
    for r in records:
        plugin_of[skill_of(r["id"])] = r.get("plugin", "")

    agent = [s for s in skills if not any(GENERATIVE.match(r["id"]) for runs in skills[s].values() for r in runs)]
    generative = [s for s in skills if s not in agent]
    total_tokens = sum(r["tokens"] for r in records)

    lines = ["# Skill benchmark report", "",
             f"{len(skills)} skills, {len(records)} agent runs, {total_tokens / 1e6:.1f}M tokens (plan allowance, no cash). "
             "Token counts are the totals Codex reports, and most of them are cached input that the agent re-reads each turn.", "",
             "Only skills whose `forced` runs all passed appear here. Other skills were tested and removed from this report, "
             "so read it as a list of what worked, not of everything tested.", "",
             "## Summary", ""]

    def pooled(names, arm):
        runs = [r for s in names for r in skills[s][arm]]
        return rate(runs)
    lines += ["| Group | Skills | bare | natural | forced |", "|---|---:|---:|---:|---:|",
              f"| Agent tasks | {len(agent)} | {pooled(agent, 'bare')} | {pooled(agent, 'natural')} | {pooled(agent, 'forced')} |",
              f"| Generative | {len(generative)} | {pooled(generative, 'bare')} | n/a | {pooled(generative, 'forced')} |", "",
              "Cells are passed runs over total runs. `natural` minus `bare` is what installing the skill does in everyday use. "
              "`forced` minus `bare` is what the skill adds when the agent uses it.", "",
              "## Method", "",
              "Each run gets a fresh seeded project folder and a throwaway `HOME` and `CODEX_HOME`, so nothing from the author's setup is present. "
              "A grader inspects the project state and planted facts. It never looks for the skill's own wording.", "",
              "| Arm | Meaning |", "|---|---|",
              "| `bare` | No skill installed |",
              "| `natural` | Skill installed in the project. The agent decides whether to use it |",
              "| `forced` | Skill installed and the prompt starts \"Use the `<skill>` skill.\" |", "",
              "`fired` means the agent opened the skill's `SKILL.md`. Prompts, fixtures and graders are in `cases.py` and `fixtures.py`.", "",
              "## Agent-task skills", "",
              "| Skill | bare | natural | forced | Fired (natural) | Tokens bare | Tokens natural | Tokens forced |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for s in agent:
        a = skills[s]
        lines.append(f"| `{s}` | {rate(a['bare'])} | {rate(a['natural'])} | {rate(a['forced'])} | {rate(a['natural'], 'fired')} | "
                     f"{mean_tokens(a['bare'])} | {mean_tokens(a['natural'])} | {mean_tokens(a['forced'])} |")
    lines += ["", "## Generative skills", "",
              "Each skill has three cases. A case states a problem with no technique named and asks what to use under a commercial license. "
              "It passes when the answer names the target project or another project on the same topic. "
              "These ran text-only (read-only sandbox, short answers), 1 run per case, with no `natural` arm.", "",
              "| Skill | bare | forced | Fired (forced) | Names exact target (bare) | Names exact target (forced) |", "|---|---:|---:|---:|---:|---:|"]
    for s in generative:
        a = skills[s]
        lines.append(f"| `{s}` | {rate(a['bare'])} | {rate(a['forced'])} | {rate(a['forced'], 'fired')} | "
                     f"{sum(bool(r['checks'].get('names_target')) for r in a['bare'])}/{len(a['bare'])} | "
                     f"{sum(bool(r['checks'].get('names_target')) for r in a['forced'])}/{len(a['forced'])} |")

    lines += ["", "## Reading the results", "",
              "- Skills where `bare` already passes every run add little on these tasks: the model does the job alone.",
              "- A low `natural` fire rate with a high `forced` pass rate means the skill works but its description does not trigger it on a plain prompt.",
              "- Installed skills can raise cost. Compare the token columns before you keep a skill that does not raise the pass rate.", "",
              "## Checks per case", "", "Share of runs where each check was true.", ""]
    for case_id, arms in cases.items():
        sample = next(iter(arms.values()))[0]
        names = [k for k in sample["checks"] if k != "pass"]
        present = [a for a in ARMS if arms.get(a)]
        lines += [f"### `{case_id}`", "", "| Check | " + " | ".join(present) + " |", "|---|" + "---:|" * len(present)]
        for name in names:
            lines.append(f"| {name} | " + " | ".join(f"{sum(bool(r['checks'].get(name)) for r in arms[a])}/{len(arms[a])}" for a in present) + " |")
        lines.append("")

    lines += ["## Saved answers", "",
              "The first run of the `bare` and `forced` arms for each agent-task skill. Every run is saved under `<case>/<arm>-<run>/` "
              "(`answer.md`, `project.diff`, `events.jsonl`, `record.json`).", ""]
    for s in agent:
        lines += [f"### `{s}`", ""]
        for arm in ("bare", "forced"):
            path = os.path.join(out, s, f"{arm}-1", "answer.md")
            if os.path.exists(path):
                rec = skills[s][arm][0]
                lines += [f"<details><summary><b>{arm}</b>: passed={rec['passed']}, fired={rec['fired']}</summary>", "", "```text", excerpt(path), "```", "", "</details>", ""]

    lines += ["## Limits", "",
              "- Codex is not Claude Code, so skill triggering may differ.",
              "- Each cell has 1 to 3 runs. A one-run gap is noise.",
              "- The author wrote the prompts and graders. Some skills were edited after seeing results, so those cases are not held out.",
              "- Several agent tasks have a small number of planted traps, so a pass shows the agent caught those traps, not that its work is complete.",
              "- `reread-guard` and `technique-finder` are not covered.", ""]
    with open(os.path.join(out, "REPORT.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print("wrote", os.path.join(out, "REPORT.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
