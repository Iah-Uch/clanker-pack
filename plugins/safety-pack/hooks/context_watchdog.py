#!/usr/bin/env python3
"""UserPromptSubmit hook: tell Claude when the context grows past a threshold.

Reads the last assistant usage from the transcript. Warns once for each 100k tokens
above the threshold, so it does not repeat on every prompt. Set
CLANKER_WATCHDOG_TOKENS to change the threshold (default 250000).
"""
import json
import os
import sys
import tempfile

DEFAULT_THRESHOLD = 250_000
STEP = 100_000
TAIL_BYTES = 400_000


def last_context_tokens(transcript_path: str):
    try:
        size = os.path.getsize(transcript_path)
        with open(transcript_path, "rb") as handle:
            handle.seek(max(0, size - TAIL_BYTES))
            tail = handle.read().decode("utf-8", errors="ignore")
    except OSError:
        return None
    for line in reversed(tail.splitlines()):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = entry.get("message")
        usage = message.get("usage") if isinstance(message, dict) else None
        if entry.get("type") == "assistant" and isinstance(usage, dict):
            return sum(int(usage.get(key) or 0) for key in (
                "input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens",
            ))
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    path = payload.get("transcript_path")
    if not isinstance(path, str):
        return 0
    try:
        threshold = int(os.environ.get("CLANKER_WATCHDOG_TOKENS", DEFAULT_THRESHOLD))
    except ValueError:
        threshold = DEFAULT_THRESHOLD
    tokens = last_context_tokens(path)
    if tokens is None or tokens < threshold:
        return 0
    level = (tokens - threshold) // STEP
    session = "".join(c for c in str(payload.get("session_id") or "unknown") if c.isalnum() or c in "-_")
    marker = os.path.join(tempfile.gettempdir(), f"clanker-watchdog-{session}-{level}")
    if os.path.exists(marker):
        return 0
    try:
        open(marker, "w").close()
    except OSError:
        pass
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                f"safety-pack watchdog: this session's context is about {tokens // 1000}k tokens. "
                "Every turn now costs more and answers get worse. In your next reply, tell the user in one short line, "
                "and suggest a fresh session with a short handoff of what is done and what is next."
            ),
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
