#!/usr/bin/env python3
"""Print how much skill-listing text each plugin adds to every session.

Run from anywhere: python scripts/cost.py
Needs PyYAML. Prints a Markdown table.

Claude Code lists each skill's `description` and `when_to_use` in every session. A
skill with `disable-model-invocation: true` adds nothing. A skill with `paths` adds
its text only while Claude works on matching files, so it counts as "on match".
Tokens are an estimate of four characters per token. Run `/context` in a real
session for exact numbers.
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHARS_PER_TOKEN = 4


def listing_chars(skill_file: Path):
    match = re.match(r"^---\n(.*?)\n---\n", skill_file.read_text(encoding="utf-8"), re.S)
    meta = yaml.safe_load(match.group(1)) if match else {}
    if not isinstance(meta, dict):
        return 0, "always"
    text = "".join(str(meta.get(key) or "") for key in ("description", "when_to_use"))
    if meta.get("disable-model-invocation") is True:
        return 0, "manual"
    return len(text), ("on match" if meta.get("paths") else "always")


def main() -> int:
    rows = []
    for plugin in sorted((ROOT / "plugins").iterdir()):
        skills = sorted(plugin.glob("skills/*/SKILL.md"))
        if not skills:
            continue
        always = on_match = manual = 0
        for skill in skills:
            chars, mode = listing_chars(skill)
            if mode == "always":
                always += chars
            elif mode == "on match":
                on_match += chars
            else:
                manual += 1
        rows.append((plugin.name, len(skills), always, on_match, manual))
    print("| Plugin | Skills | Always listed (chars) | About tokens | On file match (chars) | Manual only |")
    print("|---|---:|---:|---:|---:|---:|")
    for name, count, always, on_match, manual in rows:
        print(f"| {name} | {count} | {always} | {always // CHARS_PER_TOKEN} | {on_match} | {manual} |")
    total = sum(r[2] for r in rows)
    print(f"| **All** | {sum(r[1] for r in rows)} | {total} | {total // CHARS_PER_TOKEN} | {sum(r[3] for r in rows)} | {sum(r[4] for r in rows)} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
