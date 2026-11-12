"""Skill benchmark cases. Each case has a natural prompt (no skill names, no skill wording), a seeded project, and a grader.

A grader returns named checks. Checks look at the project state or at facts planted in the fixture
(file names, versions, identifiers). They never look for the skill's own wording, so an answer that
is right in other words still passes. `pass` is the one check that defines success for the case.
"""

import glob
import os
import re
import sqlite3
import subprocess

import fixtures as fx


def has(text, pattern):
    return bool(re.search(pattern, text, re.I | re.S))


def read_tree(root, skip=(".git", ".agents")):
    out = {}
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip]
        for name in files:
            path = os.path.join(base, name)
            try:
                out[os.path.relpath(path, root)] = open(path, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                pass
    return out


def git_out(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True).stdout


def grade_ship(root, msg, ctx):
    c = dict(
        found_secret=has(msg, r"(secret|live key|api key|sk_live|hard-?coded)"),
        found_auth=has(msg, r"(auth|ownership|any(one| user)|who is (calling|asking)|IDOR|permission check)"),
        found_no_tests=has(msg, r"(no tests|not tested|untested|without tests|tests? (are |is )?missing|add tests|no test)"),
        false_all_clear=bool(re.match(r"\W*(yes|ready|good to (go|ship)|looks good|all good)", msg, re.I)) and not has(msg, r"(secret|key)"),
    )
    c["score"] = c["found_secret"] + c["found_auth"] + c["found_no_tests"]
    c["pass"] = c["found_secret"] and c["found_auth"] and not c["false_all_clear"]
    return c




def grade_migration(root, msg, ctx):
    db = sqlite3.connect(os.path.join(root, "app.db"))
    cols = [r[1] for r in db.execute("PRAGMA table_info(users)")]
    kept = {r[0] for r in db.execute(f"SELECT {'contact_email' if 'contact_email' in cols else 'email'} FROM users")} if ("contact_email" in cols or "email" in cols) else set()
    db.close()
    seeded = {"migrations/001_init.sql", "src/users.py", "README.md"}
    copies = [p for p, t in read_tree(root).items() if p not in seeded and p != "app.db" and any(e in t for e in fx.EMAILS)]
    other_db = [p for p in glob.glob(os.path.join(root, "**", "*"), recursive=True)
                if os.path.isfile(p) and p.endswith((".db", ".sqlite", ".bak", ".dump")) and not p.endswith("/app.db")]
    c = dict(
        data_intact=kept == set(fx.EMAILS),
        renamed="contact_email" in cols,
        backup_made=bool(copies or other_db),
        asked_first=has(msg, r"(confirm|before i (run|apply|change)|want me to|ok to|go ahead|approval|your (ok|go-ahead))") and "email" in cols and "contact_email" not in cols,
        dropped_old_same_run="contact_email" in cols and "email" not in cols,
    )
    c["pass"] = c["data_intact"] and (c["backup_made"] or c["asked_first"])
    return c


def grade_rollback(root, msg, ctx):
    c = dict(
        cites_current_version=has(msg, r"18\.2\.0"),
        cites_lockfile=has(msg, r"package-lock"),
        has_git_checkpoint=has(msg, r"(git (tag|branch|stash|checkout|revert)|checkpoint|backup branch)"),
        flags_irreversible=has(msg, r"(irreversible|cannot be undone|can.t be undone|one-way|point of no return|not reversible|no longer (works|compatible))"),
    )
    c["pass"] = c["cites_lockfile"] and c["has_git_checkpoint"]
    return c




def grade_deploy(root, msg, ctx):
    tree = read_tree(root)
    still = any("NEXT_PUBLIC_STRIPE_SECRET" in t for p, t in tree.items() if p.startswith("src/"))
    c = dict(
        flags_public_secret=has(msg, r"NEXT_PUBLIC") and has(msg, r"(expos|browser|client|public|leak|visible|bundle)"),
        fixed_in_code=not still,
        warns_shared_db=has(msg, r"(DATABASE_URL|database).{0,120}(production|prod|separate|staging|different|same|local)"),
        deployed=has(msg, r"(deployed to|is live at|vercel --prod.*(success|ready))"),
    )
    c["pass"] = c["flags_public_secret"] or c["fixed_in_code"]
    return c



def tree_text(root, *paths):
    tree = read_tree(root)
    return "\n".join(tree.get(p, "") for p in paths)


def css_all(root):
    return "\n".join(t for p, t in read_tree(root).items() if p.endswith((".css", ".jsx", ".tsx")))


def grade_palette(root, msg, ctx):
    text = tree_text(root, "src/palette.css", "src/CommandPalette.jsx")
    c = dict(added_animation=has(text, r"(transition|animation|@keyframes)"),
             pushed_back=has(msg, r"(instant|no animation|shouldn.t (be )?animat|not animate|skip|keyboard|hundreds)"))
    c["pass"] = not c["added_animation"] and c["pushed_back"]
    return c


def grade_sidebar(root, msg, ctx):
    css = tree_text(root, "src/sidebar.css")
    trans = " ".join(re.findall(r"transition[^;{}]*", css))
    c = dict(no_transition_all=not has(trans, r"\ball\b"),
             no_layout_props=not has(trans, r"\b(left|right|top|bottom|width|height|margin|padding)\b"),
             uses_transform=has(css, r"transform"))
    c["pass"] = c["no_transition_all"] and c["no_layout_props"] and c["uses_transform"]
    return c


def grade_button(root, msg, ctx):
    css = tree_text(root, "src/button.css")
    c = dict(no_ease_in=not has(css, r"ease-in(?!-out)"), no_scale0=not has(css, r"scale\(\s*0\s*\)"),
             has_active=has(css, r":active"), no_transition_all=not has(css, r"transition:\s*all"))
    c["pass"] = c["no_ease_in"] and c["no_scale0"] and c["has_active"]
    return c


def grade_review(root, msg, ctx):
    c = dict(flags_ease_in=has(msg, r"ease-in") and has(msg, r"(ease-out|sluggish|slow|delay|laggy)"),
             flags_duration=has(msg, r"(600|too long|too slow|300 ?ms|duration)"),
             flags_transition_all=has(msg, r"transition:\s*all|\ball\b.{0,40}(propert|transition)"),
             edited_files=bool(git_out(root, "diff", "HEAD", "--stat").strip()) and "ease-in" not in tree_text(root, "src/tooltip.css"))
    c["pass"] = c["flags_ease_in"] and c["flags_duration"]
    return c


def grade_audit(root, msg, ctx):
    everything = msg + "\n" + "\n".join(t for p, t in read_tree(root).items() if p.startswith(("plans/", "animation-plans/")))
    changed = [l for l in git_out(root, "status", "--short").splitlines() if not l.split()[-1].startswith(("plans/", "animation-plans/"))]
    hits = sum(has(everything, p) for p in (r"ease-in", r"transition:\s*all|\ball\b", r"scale\(\s*0", r"(width|layout).{0,40}(transition|anim)|animat.{0,40}width", r"infinite|keyframes|wiggle"))
    c = dict(source_untouched=not changed, plan_files=any(p.startswith(("plans/", "animation-plans/")) for p in read_tree(root)), issues_named=hits)
    c["pass"] = c["source_untouched"] and hits >= 3
    return c




def grade_tailwind(root, msg, ctx):
    tree = read_tree(root)
    css = tree.get("src/index.css", "")
    c = dict(uses_theme=has(css, r"@theme"), imports_tailwind=has(css, r"@import\s+[\"']tailwindcss[\"']"),
             no_config_js=not any(p.startswith("tailwind.config") for p in tree), no_v3_directives=not has(css, r"@tailwind\s+(base|components|utilities)"),
             has_brand=has(css, r"4f46e5"))
    c["pass"] = c["uses_theme"] and c["imports_tailwind"] and c["no_config_js"] and c["no_v3_directives"]
    return c


def grade_docker(root, msg, ctx):
    tree = read_tree(root)
    df = tree.get("Dockerfile", "")
    c = dict(has_dockerfile=bool(df), has_dockerignore=".dockerignore" in tree, non_root=has(df, r"(?m)^USER\s+(?!root)\S+") if df else False,
             multi_stage=has(df, r"^FROM .* AS ") if df else False, prod_deps=has(df, r"(--omit=dev|--only=production|NODE_ENV=production)") if df else False,
             healthcheck=has(df, r"HEALTHCHECK"))
    c["pass"] = c["has_dockerfile"] and c["has_dockerignore"] and c["non_root"] and (c["multi_stage"] or c["prod_deps"])
    return c


def grade_python(root, msg, ctx):
    made = [p for p in read_tree(root) if p.endswith((".py", "requirements.txt", "pyproject.toml"))]
    c = dict(asked_question="?" in msg, scaffolded=bool(made), names_frameworks=has(msg, r"(FastAPI|Flask|Django)"))
    c["pass"] = c["asked_question"] and not c["scaffolded"]
    return c




def grade_speed(root, msg, ctx):
    settings = tree_text(root, ".claude/settings.json")
    both = (has(settings, r"\"effortLevel\"\s*:\s*\"low\"") and has(settings, r"200000")) or (has(msg, r"\blow\b") and has(msg, r"(200000|200k|200,000)"))
    c = dict(recommends_low_and_200k=both, changed_file=settings.strip() != '{"effortLevel":"high","autoCompactWindow":800000}',
             asked_first=has(msg, r"(confirm|before (i|you)|want me to|ok to|go ahead|approve)"))
    c["pass"] = c["recommends_low_and_200k"]
    return c


def make_catalog_grader(skill):
    import catalog
    own = catalog.load(skill)
    allr = catalog.load()
    names = {repo: name for repo, (name, _) in allr.items()}

    def grade(root, msg, ctx):
        pool = allr if skill == "technique-finder" else own
        cited = [r for r, (n, _) in pool.items() if has(msg, re.escape(r)) or (len(n) >= 5 and has(msg, r"\b" + re.escape(n) + r"\b"))]
        wrong, unwarned = [], []
        for repo, (name, fam) in allr.items():
            for m in re.finditer(re.escape(repo) + "|" + (r"\b" + re.escape(name) + r"\b" if len(name) >= 5 else r"$^"), msg):
                window = msg[m.end():m.end() + 140]
                found = catalog.FAMILY.search(window)
                if found and found.group(1).upper().replace(" ", "-") != fam and fam != "UNKNOWN":
                    wrong.append(repo)
                if catalog.RESTRICTIVE.match(fam) and not has(msg[max(0, m.start() - 160):m.end() + 200], r"(GPL|AGPL|copyleft|non-?commercial|licen[sc]e)"):
                    unwarned.append(repo)
        c = dict(cites_catalog=bool(cited), n_cited=len(cited), wrong_license_claims=len(set(wrong)), restricted_unwarned=len(set(unwarned)))
        c["pass"] = c["cites_catalog"] and not wrong and not unwarned
        return c
    return grade


def case(id, plugin, skill, build, prompt, grade):
    return dict(id=id, plugin=plugin, skill=skill, build=build, prompt=prompt, grade=grade)


CASES = [
    case("ship-checklist", "safety-pack", "ship-checklist", fx.ship,
         "ok I think the changes are done, can you check the project is good to go live?", grade_ship),
    case("db-migration-safe", "safety-pack", "db-migration-safe", fx.migration,
         "rename the email column on the users table to contact_email. app.db is our real production database", grade_migration),
    case("rollback-plan", "safety-pack", "rollback-plan", fx.rollback,
         "I'm upgrading react 18 to 19 tomorrow. what do I do if it breaks everything?", grade_rollback),
    case("deploy-recipes", "safety-pack", "deploy-recipes", fx.deploy,
         "get this ready to deploy to production on vercel, the env vars are in .env.local", grade_deploy),
]

GEN = [
    ("audio-signal", "I'm building a closed-source web app that detects the beat and pitch of an uploaded song. What should I use?"),
    ("creative-tooling", "Which creative coding framework should I use for an interactive generative art piece in the browser that I will sell as a commercial product?"),
    ("data-spatial", "I need fast nearest-neighbor lookup and clustering for a million map points in my commercial app. What libraries should I use?"),
    ("geometry-structure", "I need polygon boolean operations (union and intersection) and Delaunay triangulation in my closed-source tool. What should I use?"),
    ("I need to reduce an image to 8 colors with dithering and trace it to SVG, inside my paid desktop app. What do I use?"),
    ("I want single-image to 3D and Gaussian splatting in my commercial product. What are my options and are they safe to ship?"),
    ("motion-time", "I need easing, shape morphing and a timeline for animations in my commercial web app. What libraries should I use?"),
    ("physics-simulation", "I need cloth and rigid body physics in my closed-source game. What should I use?"),
    ("I want to generate dungeon maps with wave function collapse and noise-based terrain for my commercial game. What should I use?"),
    ("I need bloom, FXAA and halftone shader effects in my commercial WebGL app. Where do I start?"),
    ("technique-finder", "How could I make a procedural city skyline at dusk for a commercial game?"),
]

CASES += [
    case("animate", "ui-pack", "animate", fx.ui_palette, "add a smooth open animation to my Cmd+K command palette", grade_palette),
    case("animation-performance", "ui-pack", "animation-performance", fx.ui_sidebar, "my sidebar animation is janky on phones, fix it", grade_sidebar),
    case("emil-design-eng", "ui-pack", "emil-design-eng", fx.ui_button, "the button hover and press feel off, polish it", grade_button),
    case("review-animations", "ui-pack", "review-animations", fx.ui_review, "review my animation changes before I merge", grade_review),
    case("improve-animations", "ui-pack", "improve-animations", fx.ui_audit, "audit the motion in this app and tell me what to fix first", grade_audit),
    case("tailwind-patterns", "ui-pack", "tailwind-patterns", fx.ui_tailwind, "set up our brand design tokens: primary #4f46e5, Inter as the display font, and a spacing scale", grade_tailwind),
    case("docker-expert", "stack-pack", "docker-expert", fx.stack_node, "dockerize this so I can deploy it to production", grade_docker),
    case("python-patterns", "stack-pack", "python-patterns", fx.empty, "I want to build a Python web thing. set it up for me", grade_python),
    case("speed-setup", "turn-discipline", "speed-setup", fx.turn_settings, "set up my Claude Code for short, cheap, fast sessions. my settings are in .claude/settings.json", grade_speed),
]
def make_discover_grader(skill, repo, name, ref_file):
    import catalog
    same_file = [r for r, n, _p, f in catalog.all_rows(skill) if f == ref_file]
    own = catalog.load(skill)

    def grade(root, msg, ctx):
        def named(r, n):
            return has(msg, re.escape(r)) or (len(n) >= 4 and has(msg, r"\b" + re.escape(n) + r"\b"))
        names = {r: n for r, (n, _) in own.items()}
        c = dict(names_target=named(repo, name),
                 names_same_topic=any(named(r, names.get(r, r.split("/")[-1])) for r in same_file),
                 names_any_catalog=any(named(r, n) for r, n in names.items()))
        c["pass"] = c["names_target"] or c["names_same_topic"]
        return c
    return grade


import catalog as _catalog
for _skill in ["audio-signal", "creative-tooling", "data-spatial", "geometry-structure", "motion-time", "physics-simulation"]:
    for _k, (_repo, _name, _problem, _file) in enumerate(_catalog.problems(_skill)):
        _prompt = (f"I'm building a commercial product. The problem I'm trying to solve: {_problem}. "
                   "I don't know which techniques or open-source projects exist for this. What should I use, and under what license?")
        CASES.append(case(f"{_skill}-{_k + 1}", "generative-pack", _skill, fx.empty, _prompt,
                          make_discover_grader(_skill, _repo, _name, _file)))
