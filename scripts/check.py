#!/usr/bin/env python3
"""Check the marketplace for problems that `claude plugin validate` does not catch.

Run from anywhere: python scripts/check.py
Needs PyYAML. Exits 1 when any check fails.
"""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MAX_DESCRIPTION_CHARS = 1536  # Claude Code truncates longer descriptions in the skill list.
SCRIPT_REF = re.compile(r"scripts/([\w.-]+\.(?:py|sh|js|mjs|ts))")

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: cannot read as JSON ({exc})")
        return {}


def check_frontmatter(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    label = skill_file.relative_to(ROOT)
    match = re.match(r"^---\n(.*?)\n---\n", skill_file.read_text(encoding="utf-8"), re.S)
    if not match:
        fail(f"{label}: no frontmatter block")
        return
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(f"{label}: frontmatter does not parse, quote the description ({exc.__class__.__name__})")
        return
    if not isinstance(meta, dict):
        fail(f"{label}: frontmatter is not a mapping")
        return
    for key in ("name", "description"):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            fail(f"{label}: missing or empty `{key}`")
    description = meta.get("description")
    if isinstance(description, str) and len(description) > MAX_DESCRIPTION_CHARS:
        fail(f"{label}: description is {len(description)} chars, limit {MAX_DESCRIPTION_CHARS}")


def check_script_references(skill_dir: Path) -> None:
    present = {p.name for p in (skill_dir / "scripts").glob("*")} if (skill_dir / "scripts").is_dir() else set()
    for doc in skill_dir.rglob("*.md"):
        for name in sorted(set(SCRIPT_REF.findall(doc.read_text(encoding="utf-8")))):
            if name not in present:
                fail(f"{doc.relative_to(ROOT)}: references scripts/{name}, which does not exist")


def check_plugin(entry: dict) -> int:
    plugin_dir = (ROOT / entry["source"]).resolve()
    if not plugin_dir.is_dir():
        fail(f"marketplace: `{entry['name']}` source {entry['source']} does not exist")
        return 0
    manifest = read_json(plugin_dir / ".claude-plugin" / "plugin.json")
    if manifest.get("name") != entry["name"]:
        fail(f"{entry['name']}: plugin.json name is {manifest.get('name')!r}")
    if manifest.get("version") != entry.get("version"):
        fail(f"{entry['name']}: marketplace version {entry.get('version')} != plugin.json {manifest.get('version')}")

    listed = {(plugin_dir / s).resolve() for s in manifest.get("skills", [])}
    on_disk = {p.parent.resolve() for p in (plugin_dir / "skills").glob("*/SKILL.md")}
    for missing in sorted(listed - on_disk):
        fail(f"{entry['name']}: plugin.json lists {missing.name}, which has no SKILL.md")
    for orphan in sorted(on_disk - listed):
        fail(f"{entry['name']}: skills/{orphan.name} is not listed in plugin.json")

    for skill_dir in sorted(on_disk):
        check_frontmatter(skill_dir)
        check_script_references(skill_dir)
    return len(on_disk)


def check_readme_count(skills: int, packs: int) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    match = re.search(r"(\d+) skills across (\d+) focused packs", readme)
    if not match:
        fail("README.md: the `N skills across M focused packs` line is missing")
    elif (int(match.group(1)), int(match.group(2))) != (skills, packs):
        fail(f"README.md says {match.group(1)} skills in {match.group(2)} packs, repository has {skills} in {packs}")


def main() -> int:
    marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")
    plugins = marketplace.get("plugins", [])
    skills = sum(check_plugin(entry) for entry in plugins)
    check_readme_count(skills, len(plugins))
    for message in errors:
        print(f"FAIL {message}")
    print(f"{len(plugins)} plugins, {skills} skills, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
