"""Read the generative-pack reference files into (name, repo, license) entries. Used to grade catalog skills."""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILY = re.compile(r"\b(AGPL|LGPL|GPL|MPL|Apache|BSD|MIT|ISC|CC0|CC[- ]BY(?:[- ]NC)?|Unlicense|Zlib|OFL)", re.I)
RESTRICTIVE = re.compile(r"^(AGPL|LGPL|GPL|CC[- ]BY[- ]NC)", re.I)


def entries(ref_file):
    text = open(ref_file, encoding="utf-8").read()
    for m in re.finditer(r"^### (.+?) — ([\w.-]+/[\w.-]+)\s*\n\*\*Status:\*\* ([^\n]+)", text, re.M):
        yield m.group(1), m.group(2), m.group(3)
    for m in re.finditer(r"^#{2,3} (.+?) \(([\w.-]+/[\w.-]+)\)\s*\n+- License and status: ([^\n]+)", text, re.M):
        yield m.group(1), m.group(2), m.group(3)


def load(skill=None):
    """Return {repo: (name, family)} for one generative skill, or for all of them when skill is None."""
    out = {}
    pattern = os.path.join(ROOT, "plugins", "generative-pack", "skills", skill or "*", "references", "*.md")
    for ref in glob.glob(pattern):
        for name, repo, status in entries(ref):
            fam = FAMILY.match(status)
            out[repo] = (name, fam.group(1).upper().replace(" ", "-") if fam else "UNKNOWN")
    return out


def problems(skill, count=3):
    """Pick `count` entries of a skill and turn each 'Reach for it when' line into a problem statement.

    The problem never names the project, so the answer has to find it. Returns (repo, name, problem, file) rows.
    """
    rows = []
    for ref in sorted(glob.glob(os.path.join(ROOT, "plugins", "generative-pack", "skills", skill, "references", "*.md"))):
        text = open(ref, encoding="utf-8").read()
        blocks = re.split(r"^#{2,3} ", text, flags=re.M)[1:]
        for block in blocks:
            head = re.match(r"(.+?) (?:—|\() ?([\w.-]+/[\w.-]+)", block)
            when = re.search(r"(?:Reach for it when|\*\*Use it when):\*{0,2}\s*([^\n]+)", block)
            if head and when:
                problem = when.group(1).strip().rstrip(".")
                if head.group(1).lower() not in problem.lower() and head.group(2).split("/")[-1].lower() not in problem.lower():
                    rows.append((head.group(2), head.group(1), problem, os.path.basename(ref)))
    step = max(1, len(rows) // count)
    return rows[::step][:count]


def all_rows(skill):
    """Every (repo, name, problem, file) row of a skill, not just the picked ones."""
    return problems(skill, count=10**6)
