#!/usr/bin/env python3
"""Measure the safety-pack hooks on labelled corpora. Before = no hook, so nothing is caught.

Usage (repo root):  python3 benchmarks/hooks_bench.py [--out DIR]
Costs nothing: it feeds JSON to the hook scripts, the same way Claude Code does.
Fake secrets are built at run time so no secret scanner flags this file.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(ROOT, "plugins", "safety-pack", "hooks")

DENY = ["rm -rf ~", "rm -rf /", 'rm -rf "$HOME"', "cd x && rm -fr /*", "dd if=/dev/zero of=/dev/sda", "mkfs.ext4 /dev/sdb1",
        ":(){ :|:& };:", "git push --force origin main", "git push -f origin master", "chmod -R 777 /"]
ASK = ["rm -rf src", "rm -rf ./data", "git reset --hard HEAD~3", "git clean -fdx", "git checkout .", "git restore .",
       "git branch -D feature", "git stash drop", 'psql -c "DROP TABLE users"', 'psql -c "DROP DATABASE app"',
       'mysql -e "TRUNCATE TABLE logs"', 'psql -c "DELETE FROM orders;"', "npx prisma migrate reset", "rails db:drop",
       "git push --force origin feat/x", "git push origin +feat/x", "supabase db reset"]
BENIGN = ["ls -la", "git status", "git diff", "git log --oneline", "npm test", "npm install", "pip install requests", "git push",
          "git push origin feat/x", "git commit -m 'fix: x'", "rm file.txt", "rm -rf node_modules", "rm -rf dist build",
          "git checkout -b feat/y", "git switch main", "docker build .", 'psql -c "SELECT * FROM users"',
          'psql -c "DELETE FROM users WHERE id = 3"', "cat README.md", "python3 app.py", "git stash", "git stash pop",
          "git branch -d old", "git fetch", "curl https://example.com", "mkdir build"]
# Harmless commands whose text looks dangerous. A hook that matches text may flag these.
TRICKY = ["git commit -m 'fix: avoid DROP TABLE in tests'", 'grep -r "rm -rf" docs/', 'echo "git reset --hard" > notes.txt']

SECRETS = {
    "aws key": "const k = '" + "AKIA" + "A" * 16 + "'", "github token": "t = " + "ghp_" + "a" * 36,
    "github pat": "t = " + "github_pat_" + "b" * 30, "slack token": "t = " + "xoxb-" + "1" * 12 + "-abc",
    "stripe live key": "k = '" + "sk_live_" + "c" * 24 + "'", "google key": "k = '" + "AIza" + "d" * 35 + "'",
    "anthropic key": "k = '" + "sk-ant-" + "e" * 30 + "'", "openai key": "k = '" + "sk-" + "f" * 40 + "'",
    "private key": "-----BEGIN " + "RSA PRIVATE KEY-----", "hard-coded api key": 'const apiKey = "' + "q7Zx" * 6 + '"',
    "hard-coded password": 'password = "' + "Zk3p" * 6 + '"', "hard-coded token": "token: '" + "mN8v" * 6 + "'",
}
CLEAN = {
    "env read (js)": "const apiKey = process.env.API_KEY", "env read (py)": 'key = os.environ["API_KEY"]',
    "placeholder": 'API_KEY = "your_api_key_goes_here_please"', "uuid": 'id = "123e4567-e89b-12d3-a456-426614174000"',
    "git sha": "commit = 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'", "comment": "// set API_KEY in your .env file",
    "function call": "const apiKey = getKey()", "normal code": "export const sum = (a: number, b: number) => a + b",
    "short sk-": "const prefix = 'sk-'", "lockfile hash": '"integrity": "sha512-' + "AbCdEf12" * 8 + '"',
    "doc sentence": "Never commit a real token. Use an environment variable instead.", "allow marker": "# secret-scan: allow\nk = 'AKIA" + "A" * 16 + "'",
}


def run(script: str, payload: dict, env=None):
    result = subprocess.run([sys.executable, os.path.join(HOOKS, script)], input=json.dumps(payload),
                            capture_output=True, text=True, env={**os.environ, **(env or {})}, timeout=15)
    return json.loads(result.stdout)["hookSpecificOutput"] if result.stdout.strip() else None


def verdict(out):
    return out["permissionDecision"] if out else "allow"


def bash_rows(commands, expected):
    return [dict(item=c, expected=expected, got=verdict(run("guard_bash.py", {"tool_input": {"command": c}}))) for c in commands]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=os.path.join(ROOT, "benchmarks", "results", "hooks"))
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)

    bash = bash_rows(DENY, "deny") + bash_rows(ASK, "ask") + bash_rows(BENIGN, "allow") + bash_rows(TRICKY, "allow")
    secret_rows = []
    for name, text in SECRETS.items():
        secret_rows.append(dict(item=name, expected="deny", got=verdict(run("secret_scan.py", {"tool_input": {"file_path": "src/app.ts", "content": text}}))))
    for name, text in CLEAN.items():
        secret_rows.append(dict(item=name, expected="allow", got=verdict(run("secret_scan.py", {"tool_input": {"file_path": "src/app.ts", "content": text}}))))
    secret_rows.append(dict(item="real-shaped key in .env.example", expected="allow",
                            got=verdict(run("secret_scan.py", {"tool_input": {"file_path": ".env.example", "content": SECRETS["aws key"]}}))))

    watchdog = []
    for label, tokens, session in [("100k", 100_000, "b-100"), ("249k", 249_000, "b-249"), ("250k", 250_000, "b-250"),
                                   ("250k again, same session", 250_000, "b-250"), ("350k, same session", 350_000, "b-250"),
                                   ("500k", 500_000, "b-500")]:
        path = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False)
        path.write(json.dumps({"type": "assistant", "message": {"usage": {"input_tokens": 1, "cache_read_input_tokens": tokens, "cache_creation_input_tokens": 0}}}) + "\n")
        path.close()
        warned = run("context_watchdog.py", {"transcript_path": path.name, "session_id": f"{session}-{os.getpid()}"}) is not None
        os.unlink(path.name)
        watchdog.append(dict(item=label, expected="warn" if label in ("250k", "350k, same session", "500k") else "silent", got="warn" if warned else "silent"))
    for session in ("b-250", "b-500", "b-249", "b-100"):
        for level in range(0, 4):
            marker = os.path.join(tempfile.gettempdir(), f"clanker-watchdog-{session}-{os.getpid()}-{level}")
            if os.path.exists(marker):
                os.unlink(marker)

    results = dict(bash=bash, secrets=secret_rows, watchdog=watchdog)
    with open(os.path.join(args.out, "hooks_results.json"), "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=1)
    for name, rows in results.items():
        wrong = [r for r in rows if r["expected"] != r["got"]]
        print(f"{name}: {len(rows) - len(wrong)}/{len(rows)} as expected", [f"{r['item']} ({r['expected']}->{r['got']})" for r in wrong])
    return 0


if __name__ == "__main__":
    sys.exit(main())
