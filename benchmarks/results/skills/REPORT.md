# Skill benchmark report

19 skills, 120 agent runs, 9.5M tokens (plan allowance, no cash). Token counts are the totals Codex reports, and most of them are cached input that the agent re-reads each turn.

Only skills whose `forced` runs all passed appear here. Other skills were tested and removed from this report, so read it as a list of what worked, not of everything tested.

## Summary

| Group | Skills | bare | natural | forced |
|---|---:|---:|---:|---:|
| Agent tasks | 13 | 13/28 | 23/28 | 28/28 |
| Generative | 6 | 11/18 | n/a | 18/18 |

Cells are passed runs over total runs. `natural` minus `bare` is what installing the skill does in everyday use. `forced` minus `bare` is what the skill adds when the agent uses it.

## Method

Each run gets a fresh seeded project folder and a throwaway `HOME` and `CODEX_HOME`, so nothing from the author's setup is present. A grader inspects the project state and planted facts. It never looks for the skill's own wording.

| Arm | Meaning |
|---|---|
| `bare` | No skill installed |
| `natural` | Skill installed in the project. The agent decides whether to use it |
| `forced` | Skill installed and the prompt starts "Use the `<skill>` skill." |

`fired` means the agent opened the skill's `SKILL.md`. Prompts, fixtures and graders are in `cases.py` and `fixtures.py`.

## Agent-task skills

| Skill | bare | natural | forced | Fired (natural) | Tokens bare | Tokens natural | Tokens forced |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ship-checklist` | 0/2 | 2/2 | 2/2 | 2/2 | 76k | 89k | 102k |
| `db-migration-safe` | 1/2 | 1/2 | 2/2 | 2/2 | 105k | 106k | 78k |
| `deploy-recipes` | 2/2 | 2/2 | 2/2 | 2/2 | 74k | 274k | 246k |
| `rollback-plan` | 1/3 | 2/3 | 3/3 | 2/3 | 35k | 57k | 63k |
| `animate` | 0/2 | 1/2 | 2/2 | 1/2 | 93k | 99k | 37k |
| `animation-performance` | 2/2 | 2/2 | 2/2 | 0/2 | 79k | 70k | 104k |
| `emil-design-eng` | 2/2 | 2/2 | 2/2 | 0/2 | 86k | 90k | 99k |
| `review-animations` | 1/2 | 2/2 | 2/2 | 2/2 | 62k | 52k | 45k |
| `improve-animations` | 2/2 | 2/2 | 2/2 | 2/2 | 48k | 75k | 100k |
| `tailwind-patterns` | 2/2 | 2/2 | 2/2 | 0/2 | 93k | 118k | 104k |
| `docker-expert` | 0/2 | 1/2 | 2/2 | 0/2 | 108k | 105k | 163k |
| `speed-setup` | 0/2 | 2/2 | 2/2 | 2/2 | 486k | 53k | 126k |
| `python-patterns` | 0/3 | 2/3 | 3/3 | 2/3 | 98k | 80k | 47k |

## Generative skills

Each skill has three cases. A case states a problem with no technique named and asks what to use under a commercial license. It passes when the answer names the target project or another project on the same topic. These ran text-only (read-only sandbox, short answers), 1 run per case, with no `natural` arm.

| Skill | bare | forced | Fired (forced) | Names exact target (bare) | Names exact target (forced) |
|---|---:|---:|---:|---:|---:|
| `audio-signal` | 1/3 | 3/3 | 2/3 | 1/3 | 3/3 |
| `creative-tooling` | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 |
| `data-spatial` | 2/3 | 3/3 | 2/3 | 1/3 | 1/3 |
| `geometry-structure` | 2/3 | 3/3 | 3/3 | 0/3 | 2/3 |
| `motion-time` | 2/3 | 3/3 | 3/3 | 1/3 | 3/3 |
| `physics-simulation` | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 |

## Reading the results

- Skills where `bare` already passes every run add little on these tasks: the model does the job alone.
- A low `natural` fire rate with a high `forced` pass rate means the skill works but its description does not trigger it on a plain prompt.
- Installed skills can raise cost. Compare the token columns before you keep a skill that does not raise the pass rate.

## Checks per case

Share of runs where each check was true.

### `ship-checklist`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| found_secret | 2/2 | 2/2 | 2/2 |
| found_auth | 0/2 | 2/2 | 2/2 |
| found_no_tests | 0/2 | 1/2 | 1/2 |
| false_all_clear | 0/2 | 0/2 | 0/2 |
| score | 2/2 | 2/2 | 2/2 |

### `db-migration-safe`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| data_intact | 2/2 | 2/2 | 2/2 |
| renamed | 1/2 | 0/2 | 0/2 |
| backup_made | 1/2 | 0/2 | 0/2 |
| asked_first | 0/2 | 1/2 | 2/2 |
| dropped_old_same_run | 1/2 | 0/2 | 0/2 |

### `deploy-recipes`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| flags_public_secret | 2/2 | 2/2 | 2/2 |
| fixed_in_code | 1/2 | 2/2 | 2/2 |
| warns_shared_db | 1/2 | 2/2 | 2/2 |
| deployed | 0/2 | 0/2 | 0/2 |

### `rollback-plan`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| cites_current_version | 1/3 | 1/3 | 3/3 |
| cites_lockfile | 1/3 | 3/3 | 3/3 |
| has_git_checkpoint | 1/3 | 2/3 | 3/3 |
| flags_irreversible | 1/3 | 0/3 | 2/3 |

### `animate`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| added_animation | 2/2 | 1/2 | 0/2 |
| pushed_back | 0/2 | 1/2 | 2/2 |

### `animation-performance`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| no_transition_all | 2/2 | 2/2 | 2/2 |
| no_layout_props | 2/2 | 2/2 | 2/2 |
| uses_transform | 2/2 | 2/2 | 2/2 |

### `emil-design-eng`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| no_ease_in | 2/2 | 2/2 | 2/2 |
| no_scale0 | 2/2 | 2/2 | 2/2 |
| has_active | 2/2 | 2/2 | 2/2 |
| no_transition_all | 2/2 | 2/2 | 2/2 |

### `review-animations`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| flags_ease_in | 1/2 | 2/2 | 2/2 |
| flags_duration | 2/2 | 2/2 | 2/2 |
| flags_transition_all | 2/2 | 2/2 | 2/2 |
| edited_files | 0/2 | 0/2 | 0/2 |

### `improve-animations`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| source_untouched | 2/2 | 2/2 | 2/2 |
| plan_files | 0/2 | 0/2 | 0/2 |
| issues_named | 2/2 | 2/2 | 2/2 |

### `tailwind-patterns`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| uses_theme | 2/2 | 2/2 | 2/2 |
| imports_tailwind | 2/2 | 2/2 | 2/2 |
| no_config_js | 2/2 | 2/2 | 2/2 |
| no_v3_directives | 2/2 | 2/2 | 2/2 |
| has_brand | 2/2 | 2/2 | 2/2 |

### `docker-expert`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| has_dockerfile | 2/2 | 2/2 | 2/2 |
| has_dockerignore | 2/2 | 2/2 | 2/2 |
| non_root | 0/2 | 1/2 | 2/2 |
| multi_stage | 0/2 | 1/2 | 1/2 |
| prod_deps | 2/2 | 2/2 | 2/2 |
| healthcheck | 2/2 | 2/2 | 2/2 |

### `speed-setup`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| recommends_low_and_200k | 0/2 | 2/2 | 2/2 |
| changed_file | 2/2 | 0/2 | 1/2 |
| asked_first | 0/2 | 1/2 | 1/2 |

### `python-patterns`

| Check | bare | natural | forced |
|---|---:|---:|---:|
| asked_question | 0/3 | 2/3 | 3/3 |
| scaffolded | 3/3 | 1/3 | 0/3 |
| names_frameworks | 3/3 | 2/3 | 2/3 |

### `audio-signal-1`

| Check | bare | forced |
|---|---:|---:|
| names_target | 1/1 | 1/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `audio-signal-2`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 1/1 |
| names_same_topic | 0/1 | 1/1 |
| names_any_catalog | 0/1 | 1/1 |

### `audio-signal-3`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 1/1 |
| names_same_topic | 0/1 | 1/1 |
| names_any_catalog | 0/1 | 1/1 |

### `creative-tooling-1`

| Check | bare | forced |
|---|---:|---:|
| names_target | 1/1 | 1/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `creative-tooling-2`

| Check | bare | forced |
|---|---:|---:|
| names_target | 1/1 | 1/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `creative-tooling-3`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 1/1 |
| names_same_topic | 0/1 | 1/1 |
| names_any_catalog | 0/1 | 1/1 |

### `data-spatial-1`

| Check | bare | forced |
|---|---:|---:|
| names_target | 1/1 | 1/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `data-spatial-2`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 0/1 |
| names_same_topic | 0/1 | 1/1 |
| names_any_catalog | 0/1 | 1/1 |

### `data-spatial-3`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 0/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `geometry-structure-1`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 1/1 |
| names_same_topic | 0/1 | 1/1 |
| names_any_catalog | 0/1 | 1/1 |

### `geometry-structure-2`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 0/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `geometry-structure-3`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 1/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `motion-time-1`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 1/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `motion-time-2`

| Check | bare | forced |
|---|---:|---:|
| names_target | 1/1 | 1/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `motion-time-3`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 1/1 |
| names_same_topic | 0/1 | 1/1 |
| names_any_catalog | 0/1 | 1/1 |

### `physics-simulation-1`

| Check | bare | forced |
|---|---:|---:|
| names_target | 1/1 | 1/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

### `physics-simulation-2`

| Check | bare | forced |
|---|---:|---:|
| names_target | 0/1 | 1/1 |
| names_same_topic | 0/1 | 1/1 |
| names_any_catalog | 0/1 | 1/1 |

### `physics-simulation-3`

| Check | bare | forced |
|---|---:|---:|
| names_target | 1/1 | 1/1 |
| names_same_topic | 1/1 | 1/1 |
| names_any_catalog | 1/1 | 1/1 |

## Saved answers

The first run of the `bare` and `forced` arms for each agent-task skill. Every run is saved under `<case>/<arm>-<run>/` (`answer.md`, `project.diff`, `events.jsonl`, `record.json`).

### `ship-checklist`

<details><summary><b>bare</b>: passed=False, fired=False</summary>

```text
**Not ready to go live.** The current project is only a few files, with no build or deployment configuration, and the new user route references `db` without defining or importing it. The billing code also contains what looks like a hard-coded live Stripe secret key in [billing.ts](/tmp/bench2-nwwf9_nh/repo/src/billing.ts:1); if that value is real, revoke it and move the replacement to a secret store.

I couldn’t establish a release-ready state from this repo: `package.json` only defines a test script, and I found no deployment setup or tests. I did not run tests or change files.
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
Not ready

- **FAIL — Secrets:** `src/billing.ts` contains a hard-coded Stripe live secret key. If it is real, revoke and rotate it immediately; move the replacement to a protected environment variable.
- **FAIL — Auth and ownership:** `src/routes/users.ts` exposes user records by ID without checking the caller’s identity or ownership. That could let one user read another user’s data.
- **FAIL — Input:** The route passes the request’s `id` directly to the database lookup without validation.
- **FAIL — Env files:** There is no `.gitignore`. `.env` and key files are not ignored, which could allow credentials to be committed.
- **FAIL — Tests:** `npm test` passed but found **zero tests**. The n ...
```

</details>

### `db-migration-safe`

<details><summary><b>bare</b>: passed=True, fired=False</summary>

```text
Renamed `users.email` to `users.contact_email` in `app.db` and updated the query and initial migration. All three user rows were preserved. A backup is at [app.db.pre_contact_email.bak](/tmp/bench2-8qmd2mpf/repo/app.db.pre_contact_email.bak).
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
`app.db` is the live production database, so the `db-migration-safe` skill requires me to stop before changing the schema and get explicit confirmation in words. I have not modified the database or files.

The skill also requires a confirmed backup before any migration. After you confirm, I can make a backup, create and dry-run a reversible migration on a copy, then report the row count and results. The skill requires an additive migration—add `contact_email`, copy `email`, and switch the code—so removing `email` would need to happen in a later change.
```

</details>

### `deploy-recipes`

<details><summary><b>bare</b>: passed=True, fired=False</summary>

```text
The repository is **not ready for a Vercel production deploy yet**. It has a `package.json` and one source file, but no Next.js app entry point, build scripts, or lockfile. I can’t make it deployable without knowing what the app should show.

I also found a likely secret-exposure issue: `src/pay.ts` reads `NEXT_PUBLIC_STRIPE_SECRET_KEY`. Next.js exposes variables with the `NEXT_PUBLIC_` prefix to browser code, so a Stripe secret must use a server-only name such as `STRIPE_SECRET_KEY`. `.env.local` is ignored by Git, so its values won’t be transferred to Vercel automatically.

What should the deployed app do, and is that variable intended to be a Stripe **secret key**?
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
I made two deployment-safety changes:

- In [src/pay.ts](/tmp/bench2-1ga3q17f/repo/src/pay.ts), changed the Stripe key to `STRIPE_SECRET_KEY`, so Next.js won’t inline it into browser bundles.
- In [.gitignore](/tmp/bench2-1ga3q17f/repo/.gitignore), ignored `.env*` files while allowing `.env.example`. Confirmed `.env.local` is ignored.

The project is **not ready to deploy yet**: this checkout contains no app entry point, build script, lockfile, or Vercel project link. There is also no database client in the code despite `DATABASE_URL` being present in `.env.local`. I couldn’t run a production build.

For Vercel, configure `STRIPE_SECRET_KEY` and `DATABASE_URL` in the project’s **Production** ...
```

</details>

### `rollback-plan`

<details><summary><b>bare</b>: passed=False, fired=False</summary>

```text
Treat it like a release with a rollback plan, not a one-way migration.

**Before you upgrade**

- Commit or tag the current working version so you can return to it.
- Make the upgrade on a branch and keep the change set small.
- Check React’s official [upgrade guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide) and run the React 19 codemods.
- Confirm your framework, router, UI libraries, test tools, and React types support React 19. Upgrade incompatible dependencies before or alongside React.
- Run your existing tests and build on React 18 first. Save the results as a baseline.
- Make sure you know how to redeploy the current React 18 build. If you can, stage the React 19 relea ...
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
React 18 → 19 is a dependency upgrade. In this repo, `react` and `react-dom` are both `18.2.0`, and `package-lock.json` is tracked. The working tree is clean on `main`, at commit `2150c55` (`base`).

1. **Before upgrading:** create a separate branch and record the starting commit: `git switch -c upgrade/react-19` and `git rev-parse HEAD`. Keep the upgrade in its own commit.
2. **If it breaks before merging:** switch back to `main`. If you need to undo the upgrade on its branch, run `git revert <upgrade-commit>`.
3. **Restore dependencies:** use `git restore --source=main -- package.json package-lock.json`, then run `npm ci` to reinstall from the React 18 lockfile. This works because `package ...
```

</details>

### `animate`

<details><summary><b>bare</b>: passed=False, fired=False</summary>

```text
Added a 180 ms opening animation to the command palette: it fades in while moving down slightly and scaling into place. Reduced-motion settings disable the animation.
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
The animate skill says command palettes opened by keyboard shortcuts should remain instant because they’re used frequently. Since Cmd+K is the primary way to open this palette, I’m not adding an opening animation.
```

</details>

### `animation-performance`

<details><summary><b>bare</b>: passed=True, fired=False</summary>

```text
Updated [sidebar.css](/tmp/bench2-2fab12_v/repo/src/sidebar.css) to animate the sidebar with `transform` instead of `left`, which avoids animating layout during the slide. The panel now fits narrow screens, and reduced-motion preferences are respected.

I didn’t run tests.
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
Changed the sidebar animation in [sidebar.css](/tmp/bench2-141cc1qc/repo/src/sidebar.css:1) to move with `transform: translateX()` instead of animating `left`, and replaced `transition: all` with an explicit transform transition. This avoids per-frame layout work that can make the animation janky on phones.

The cause and fix are verified from the code. Confirm the result with a performance recording on a mid-range phone; I haven’t profiled it on a device.
```

</details>

### `emil-design-eng`

<details><summary><b>bare</b>: passed=True, fired=False</summary>

```text
Updated [button.css](/tmp/bench2-5nbcah3d/repo/src/button.css) with a subtle color and shadow change on hover, a quick press response, and a visible keyboard focus state. The previous hover rule shrank the button to zero; it’s removed. Reduced-motion preferences are respected.
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
Updated [button.css](/tmp/bench2-skeds_s6/repo/src/button.css) with a subtle color and shadow change on hover, plus a quick scale-down on press. Hover is limited to mouse-like pointers, and reduced-motion settings disable the transform animation.

| Before | After | Why |
| --- | --- | --- |
| `transform: scale(0)` on hover | Slightly darker background and soft shadow | Keeps the button visible while giving clear hover feedback |
| `transition: all 300ms ease-in` | Specific properties with short transitions | Makes feedback quicker and avoids animating unrelated properties |
| No press state | `transform: scale(0.97)` on `:active` | Gives immediate tactile feedback |
```

</details>

### `review-animations`

<details><summary><b>bare</b>: passed=False, fired=False</summary>

```text
**Finding — the transition can animate every changed property.** In [src/tooltip.css](/tmp/bench2-1srlcych/repo/src/tooltip.css:1), `transition: all` applies to any animatable property that changes on `.tooltip`, which can cause unintended or costly animations. Scope it to `opacity`:

'''css
.tooltip { opacity: 0; transition: opacity 600ms ease-in; }
'''

The `.show` rule changes opacity as expected. I couldn’t verify how the class is applied: the only other source file, `src/App.jsx`, renders an empty `<main />`, and there are no tooltip callers in the repo.
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
### Part 1 — Findings

| Before | After | Why |
| --- | --- | --- |
| `transition: all 600ms ease-in` in [src/tooltip.css](/tmp/bench2-kxqob1gj/repo/src/tooltip.css:1) | `transition: opacity 150ms cubic-bezier(0.23, 1, 0.32, 1)` | `all` can animate unintended properties, `ease-in` makes the entrance feel sluggish, and 600ms exceeds the tooltip’s 125–200ms budget and the 300ms UI limit. |

### Part 2 — Verdict

**Feel-breaking regressions**

The tooltip entrance uses `ease-in` and takes 600ms, far beyond the skill’s 300ms UI limit.

**Performance**

`transition: all` allows unintended properties to animate.

**Verdict: Block.** Replace the unbounded transition with an explicit property and sh ...
```

</details>

### `improve-animations`

<details><summary><b>bare</b>: passed=True, fired=False</summary>

```text
There’s very little app to audit yet: [App.jsx](/tmp/bench2-fag6gs7l/repo/src/App.jsx) renders an empty `<main />`, and the three CSS files define the only motion I found.

## Fix first

1. **Remove the infinite row wiggle.** [list.css](/tmp/bench2-fag6gs7l/repo/src/list.css) animates `margin-left` continuously on hover. That can cause repeated layout work and makes rows jitter. Prefer a brief, subtle `transform` transition—or remove the motion if it doesn’t communicate a useful interaction.
2. **Replace the modal’s `transition: all`.** [modal.css](/tmp/bench2-fag6gs7l/repo/src/modal.css) transitions every property and scales from zero, which can feel abrupt and may animate unrelated changes ...
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
## Motion audit

The app is a minimal React 18 shell with three CSS motion rules and no shared motion tokens. Based on the code, the UI appears to call for restrained interaction feedback. The most frequent motion is the row hover; the modal and menu are occasional interactions.

| # | Severity | Category | Location | Finding | Fix summary |
|---|---|---|---|---|---|
| 1 | HIGH | Purpose & frequency | [src/list.css:1](/tmp/bench2-uoruv0np/repo/src/list.css:1) | Hover starts an infinite 900ms wiggle, and [line 2](/tmp/bench2-uoruv0np/repo/src/list.css:2) animates `margin-left`. This repeats during a common interaction and triggers layout. | Remove the continuous wiggle. If hover feedback is n ...
```

</details>

### `tailwind-patterns`

<details><summary><b>bare</b>: passed=True, fired=False</summary>

```text
Added the design tokens in [src/index.css](/tmp/bench2-ijyt262b/repo/src/index.css): primary `#4f46e5`, Inter as the display and default font, and a spacing scale from `0.25rem` to `6rem`. Imported Tailwind CSS so its theme tokens are available.
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
Added Tailwind v4 theme tokens in [index.css](/tmp/bench2-7o3fez0_/repo/src/index.css): primary `#4f46e5`, an Inter display font stack, and a spacing scale from `0` through `24` (up to `6rem`). Also added Tailwind’s CSS import.
```

</details>

### `docker-expert`

<details><summary><b>bare</b>: passed=False, fired=False</summary>

```text
Added a production-oriented Docker setup:

- [Dockerfile](/tmp/bench2-7nv4w59f/repo/Dockerfile) uses Node 22 Alpine, installs production dependencies, runs as the non-root `node` user, and defines a health check.
- [compose.yaml](/tmp/bench2-7nv4w59f/repo/compose.yaml) configures restart behavior, a read-only filesystem, and reduced container privileges.
- [.dockerignore](/tmp/bench2-7nv4w59f/repo/.dockerignore) excludes local dependencies, Git files, and environment secrets from the build context.
- [server.js](/tmp/bench2-7nv4w59f/repo/server.js) now listens on `PORT` (default `3000`) and all interfaces.

Run it with `docker compose up --build -d`; set `PORT` to change the host port. I did ...
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
Added a production Docker setup:

- [Dockerfile](/tmp/bench2-81_zx2z5/repo/Dockerfile) builds a small Node 22 Alpine image, installs production dependencies, runs as a non-root user, and checks `/health`.
- [.dockerignore](/tmp/bench2-81_zx2z5/repo/.dockerignore) excludes secrets, local dependencies, and build artifacts.
- [compose.yaml](/tmp/bench2-81_zx2z5/repo/compose.yaml) sets restart behavior, read-only filesystem, dropped capabilities, and resource limits.

Deploy with `docker compose up -d --build`; set `PORT` to change the host port. I couldn’t verify the image build because access to the Docker daemon was denied.
```

</details>

### `speed-setup`

<details><summary><b>bare</b>: passed=False, fired=False</summary>

```text
Updated [.claude/settings.json](/tmp/bench2-_tdam29c/repo/.claude/settings.json) to use Haiku by default, low effort, and a medium effort cap. Removed the 800,000-token compaction override so Claude Code uses its model-tuned default. JSON validation passed.

I left fast mode off because it increases the cost per token. These settings follow Claude Code’s [settings reference](https://code.claude.com/docs/en/settings-reference); the effort cap requires Claude Code v2.1.267 or later.
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
Set the project defaults to `effortLevel: low` and `autoCompactWindow: 200000` in [.claude/settings.json](/tmp/bench2-sxfoos30/repo/.claude/settings.json), and added the skill’s Turn discipline block to [CLAUDE.md](/tmp/bench2-sxfoos30/repo/CLAUDE.md). I confirmed both files contain the intended changes.
```

</details>

### `python-patterns`

<details><summary><b>bare</b>: passed=False, fired=False</summary>

```text
Set up a minimal Flask web app with a landing page and a `/health` endpoint. The README includes commands to create a virtual environment, install dependencies, and run it locally.

Start it with `flask --app app run --debug` and open <http://127.0.0.1:5000>.
```

</details>

<details><summary><b>forced</b>: passed=True, fired=True</summary>

```text
Which kind of Python web app should I set up?

- Web page (Flask)
- JSON API (FastAPI)
- Full-stack app (Django)
```

</details>

## Limits

- Codex is not Claude Code, so skill triggering may differ.
- Each cell has 1 to 3 runs. A one-run gap is noise.
- The author wrote the prompts and graders. Some skills were edited after seeing results, so those cases are not held out.
- Several agent tasks have a small number of planted traps, so a pass shows the agent caught those traps, not that its work is complete.
- `reread-guard` and `technique-finder` are not covered.
