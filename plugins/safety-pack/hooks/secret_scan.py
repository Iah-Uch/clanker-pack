#!/usr/bin/env python3
"""PreToolUse hook for Write, Edit and MultiEdit: deny content that holds a secret.

The reason names the kind of secret and the line number. It never prints the secret.
Add the text `secret-scan: allow` to the content to skip the check for a known fake.
"""
import json
import os
import re
import sys

PATTERNS = [
    ("AWS access key id", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP |ENCRYPTED )?PRIVATE KEY")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Stripe live key", re.compile(r"\b[rs]k_live_[0-9a-zA-Z]{16,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{32,}\b")),
    ("hard-coded credential", re.compile(
        r"""(?ix)\b(api[_-]?key|secret|token|passw(?:or)?d|private[_-]?key)\w*\s*[:=]\s*['"]([A-Za-z0-9_\-/+=.]{20,})['"]"""
    )),
]
PLACEHOLDER = re.compile(r"(?i)your[_-]|example|changeme|placeholder|dummy|sample|xxxx|<[^>]+>|\$\{|process\.env|os\.environ|getenv|\*{4,}")
EXEMPT_SUFFIXES = (".example", ".sample", ".template", ".dist")
ALLOW_MARKER = "secret-scan: allow"


def collect(tool_input: dict) -> str:
    parts = []
    for key in ("content", "new_string"):
        value = tool_input.get(key)
        if isinstance(value, str):
            parts.append(value)
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict) and isinstance(edit.get("new_string"), str):
            parts.append(edit["new_string"])
    return "\n".join(parts)


def find_secret(text: str):
    for number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in PATTERNS:
            match = pattern.search(line)
            if not match:
                continue
            if label == "hard-coded credential" and PLACEHOLDER.search(match.group(2)):
                continue
            if label != "hard-coded credential" and PLACEHOLDER.search(match.group(0)):
                continue
            return label, number
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    tool_input = payload.get("tool_input") or {}
    path = str(tool_input.get("file_path") or "")
    if path.endswith(EXEMPT_SUFFIXES) or os.path.basename(path) in {".env.example", ".env.sample"}:
        return 0
    text = collect(tool_input)
    if not text or ALLOW_MARKER in text:
        return 0
    found = find_secret(text)
    if found:
        label, number = found
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"safety-pack: a {label} is at line {number} of the new content for {path or 'this file'}. "
                    "Read it from an environment variable and put the real value in an ignored .env file instead."
                ),
            }
        }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
