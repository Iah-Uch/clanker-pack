#!/usr/bin/env python3
"""Skill benchmark: does an installed skill change what an agent does to a real project folder?

Usage (repo root):  python3 benchmarks/run.py [--only text] [--runs 3] [--arms bare,natural,forced] [--out DIR]

Arms, each in a throwaway HOME and CODEX_HOME so nothing from the user's own setup leaks in:
  bare     no skill present
  natural  the skill sits in <project>/.agents/skills. The agent must decide to use it, as in real use
  forced   same, and the prompt names the skill. Separates "did not fire" from "content does not help"

The agent works in a seeded project (fixtures.py) with the workspace-write sandbox. Graders in cases.py
check the project state and planted facts, never the skill's own wording.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cases import CASES, git_out  # noqa: E402

TOKENS = re.compile(r"tokens used\s*\n\s*([\d,]+)")
CONFIG = 'model = "gpt-6-luna"\nmodel_reasoning_effort = "low"\n'


def run_job(job):
    case, arm, n, out_dir = job
    base = tempfile.mkdtemp(prefix="bench2-")
    home = os.path.join(base, "home")
    repo = os.path.join(base, "repo")
    os.makedirs(os.path.join(home, ".codex"))
    shutil.copy(os.path.expanduser("~/.codex/auth.json"), os.path.join(home, ".codex", "auth.json"))
    with open(os.path.join(home, ".codex", "config.toml"), "w") as handle:
        handle.write(CONFIG)
    case["build"](repo)
    ctx = {"main_sha": git_out(repo, "rev-parse", "main").strip()}
    if arm != "bare":
        shutil.copytree(os.path.join(ROOT, "plugins", case["plugin"], "skills", case["skill"]),
                        os.path.join(repo, ".agents", "skills", case["skill"]))
        with open(os.path.join(repo, ".git", "info", "exclude"), "a") as handle:
            handle.write(".agents/\n")
    prompt = case["prompt"] if arm != "forced" else f"Use the {case['skill']} skill. {case['prompt']}"
    if os.environ.get("BENCH_TEXT_ONLY"):
        prompt += "\n\nReply in plain text, under 200 words. Do not write files, run commands or search the web."
    answer_file = os.path.join(base, "answer.md")
    started = time.time()
    result = subprocess.run(
        ["codex", "exec", "--json", "-s", "read-only" if os.environ.get("BENCH_TEXT_ONLY") else "workspace-write", "-c", f'sandbox_workspace_write.writable_roots=["{repo}/.git"]', "--skip-git-repo-check", "--ephemeral", "-C", repo, "-o", answer_file, "-"],
        input=prompt, capture_output=True, text=True, timeout=900, env={**os.environ, "HOME": home, "CODEX_HOME": os.path.join(home, ".codex")})
    msg = open(answer_file, encoding="utf-8").read() if os.path.exists(answer_file) else ""
    seconds = round(time.time() - started, 1)
    events = result.stdout
    tokens = TOKENS.findall(result.stderr + result.stdout)
    if not tokens:
        tokens = [str(sum(int(x) for x in re.findall(r'"(?:input|output)_tokens":\s*(\d+)', events)))]
    fired = bool(re.search(re.escape(case["skill"]) + r"/SKILL\.md", events))
    checks = case["grade"](repo, msg, ctx)
    folder = os.path.join(out_dir, case["id"], f"{arm}-{n}")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "answer.md"), "w", encoding="utf-8") as handle:
        handle.write(msg)
    with open(os.path.join(folder, "project.diff"), "w", encoding="utf-8") as handle:
        handle.write(git_out(repo, "status", "--short") + "\nBRANCHES\n" + git_out(repo, "branch", "-a") + "TAGS\n" + git_out(repo, "tag") + "STASH\n" + git_out(repo, "stash", "list") + "\n" + git_out(repo, "diff", "HEAD")[:20000])
    with open(os.path.join(folder, "events.jsonl"), "w", encoding="utf-8") as handle:
        handle.write(events[:400000])
    shutil.rmtree(base, ignore_errors=True)
    record = dict(id=case["id"], arm=arm, run=n, fired=fired, tokens=int(tokens[-1].replace(",", "")) if tokens else 0,
                  seconds=seconds, rc=result.returncode, checks=checks, passed=bool(checks["pass"]))
    with open(os.path.join(folder, "record.json"), "w") as handle:
        json.dump(record, handle, indent=1)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", default="")
    parser.add_argument("--pack", default="", help="comma list of plugin names")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--arms", default="bare,natural,forced")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--out", default=os.path.join(ROOT, "benchmarks", "results", "skills"))
    args = parser.parse_args()
    cases = [c for c in CASES if args.only in c["id"] and (not args.pack or c["plugin"] in args.pack.split(","))]
    jobs = [(c, arm, n, args.out) for c in cases for arm in args.arms.split(",") for n in range(1, args.runs + 1)]
    print(f"{len(cases)} cases, {len(jobs)} runs, workers={args.workers}", flush=True)
    with ThreadPoolExecutor(args.workers) as pool:
        records = list(pool.map(run_job, jobs))
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "records.json")
    old = json.load(open(path)) if os.path.exists(path) else []
    keep = [r for r in old if (r["id"], r["arm"], r["run"]) not in {(x["id"], x["arm"], x["run"]) for x in records}]
    json.dump(keep + records, open(path, "w"), indent=1)
    print(f"done: {len(records)} runs, {sum(r['tokens'] for r in records):,} tokens, {sum(r['rc'] != 0 for r in records)} failed -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
