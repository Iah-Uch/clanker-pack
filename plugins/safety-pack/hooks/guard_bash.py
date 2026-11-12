#!/usr/bin/env python3
"""PreToolUse hook for Bash: deny catastrophic commands, ask before destructive ones.

Reads the hook JSON on stdin. Prints a permission decision on stdout, or prints
nothing to let the call continue. It never runs the command.
"""
import json
import re
import shlex
import sys

# A target that wipes a whole machine or home directory.
CATASTROPHIC_TARGETS = {"/", "/*", "~", "~/", "~/*", "$HOME", "$HOME/", "$HOME/*", "${HOME}", "${HOME}/", "${HOME}/*"}
# Build output that is safe and common to delete with rm -rf.
DISPOSABLE_TARGETS = {
    "node_modules", "dist", "build", ".next", ".nuxt", ".turbo", ".cache", "coverage",
    "__pycache__", ".pytest_cache", ".venv", "venv", "target", "out", ".parcel-cache",
}

SEGMENT_SPLIT = re.compile(r"\|\||&&|;|\||\n")
RM_RECURSIVE = re.compile(r"^-[a-zA-Z]*[rR][a-zA-Z]*$|^--recursive$")
RM_FORCE = re.compile(r"^-[a-zA-Z]*f[a-zA-Z]*$|^--force$")

DENY_PATTERNS = [
    (re.compile(r":\s*\(\s*\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:"), "fork bomb"),
    (re.compile(r"\bmkfs(\.\w+)?\s"), "formatting a disk"),
    (re.compile(r"\bdd\b[^\n]*\bof=/dev/(sd|nvme|hd|vd|disk)"), "writing raw data to a disk"),
    (re.compile(r">\s*/dev/(sd|nvme|hd|vd)\w*"), "writing raw data to a disk"),
    (re.compile(r"\bchmod\s+-R\s+0?777\s+/(\s|$)"), "opening permissions on the whole system"),
]

ASK_PATTERNS = [
    (re.compile(r"\bgit\s+reset\s+--hard\b"), "git reset --hard throws away uncommitted work"),
    (re.compile(r"\bgit\s+clean\s+-[a-zA-Z]*f"), "git clean deletes untracked files for good"),
    (re.compile(r"\bgit\s+checkout\s+(--\s+)?\.(\s|$)"), "git checkout . throws away uncommitted work"),
    (re.compile(r"\bgit\s+restore\s+(--\S+\s+)*\.(\s|$)"), "git restore . throws away uncommitted work"),
    (re.compile(r"\bgit\s+branch\s+-D\b"), "git branch -D deletes a branch that may be unmerged"),
    (re.compile(r"\bgit\s+stash\s+(drop|clear)\b"), "git stash drop deletes saved work"),
    (re.compile(r"\bdrop\s+(table|database|schema)\b", re.I), "a SQL DROP deletes data for good"),
    (re.compile(r"\btruncate\s+(table\s+)?\w", re.I), "TRUNCATE deletes every row"),
    (re.compile(r"\bdelete\s+from\s+\w+\s*(;|$|\")", re.I), "DELETE with no WHERE deletes every row"),
    (re.compile(r"\b(prisma\s+migrate\s+reset|prisma\s+db\s+push\s+.*--force-reset|rails\s+db:(drop|reset)|rake\s+db:(drop|reset)|sequelize\s+db:drop|drizzle-kit\s+drop)\b"), "this resets or drops a database"),
    (re.compile(r"\b(supabase\s+db\s+reset)\b"), "this resets a database"),
]

FORCE_FLAG = re.compile(r"(^|\s)(--force\b(?!-with-lease)|-f\b)")
PROTECTED_BRANCH = re.compile(r"\b(main|master|production|prod|release)\b")


def decision(kind: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": kind,
            "permissionDecisionReason": f"safety-pack: {reason}",
        }
    }))


def split_args(segment: str) -> list[str]:
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def check_rm(segment: str):
    args = split_args(segment)
    if "rm" not in args:
        return None
    rest = args[args.index("rm") + 1:]
    flags = [a for a in rest if a.startswith("-")]
    targets = [a for a in rest if not a.startswith("-")]
    recursive = any(RM_RECURSIVE.match(f) for f in flags)
    force = any(RM_FORCE.match(f) for f in flags)
    if not recursive:
        return None
    if any(t in CATASTROPHIC_TARGETS for t in targets):
        return "deny", "this would delete the whole system or your home directory"
    if force and not all(t.rstrip("/").split("/")[-1] in DISPOSABLE_TARGETS for t in targets):
        return "ask", "rm -rf deletes files with no way back"
    return None


def check_git_push(segment: str):
    if not re.search(r"\bgit\s+push\b", segment):
        return None
    if FORCE_FLAG.search(segment) or "--force-with-lease" in segment:
        if PROTECTED_BRANCH.search(segment):
            return "deny", "a force push to a protected branch can erase other people's work"
        return "ask", "a force push rewrites remote history"
    if re.search(r"\bgit\s+push\s+\S+\s+\+", segment):
        return "ask", "a + refspec is a force push"
    return None


def evaluate(command: str):
    for pattern, label in DENY_PATTERNS:
        if pattern.search(command):
            return "deny", f"blocked, {label}"
    verdicts = []
    for segment in SEGMENT_SPLIT.split(command):
        for check in (check_rm, check_git_push):
            found = check(segment)
            if found:
                verdicts.append(found)
    for pattern, label in ASK_PATTERNS:
        if pattern.search(command):
            verdicts.append(("ask", label))
    for kind, reason in verdicts:
        if kind == "deny":
            return kind, reason
    return verdicts[0] if verdicts else None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str) or not command.strip():
        return 0
    result = evaluate(command)
    if result:
        decision(*result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
