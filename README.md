# clanker-pack

A personal Claude Code plugin marketplace — 28 skills across 6 focused packs. Each pack is a plugin you install independently. An installed skill adds its description to every session's skill list, and Claude loads the full skill only when the description matches the task. Install only the packs you use.

## Install

```
/plugin marketplace add Iah-Uch/clanker-pack

/plugin install ui-pack@clanker-pack         # Tailwind v4, assets, animation
/plugin install tools-pack@clanker-pack      # diagrams
/plugin install stack-pack@clanker-pack      # Docker, Python
/plugin install safety-pack@clanker-pack     # guardrails: ship checks, safe migrations, rollback, hooks
/plugin install generative-pack@clanker-pack # generative and creative-coding techniques
```

One mod:

```
/plugin install reread-guard@clanker-pack   # refuses a repeat Read of an unchanged large file
```

A setup skill and a slice runner for short, cheap sessions, and a bundle that installs 15 plugins from other authors. Read its README first, because the ai-memory plugin needs its binary:

```
/plugin install turn-discipline@clanker-pack   # effort and compaction setup, slice runner
/plugin install recommended-pack@clanker-pack  # 15 plugins from other authors
```

### Quick start

The smallest useful set. It needs no extra binary.

```
/plugin marketplace add Iah-Uch/clanker-pack
/plugin install recommended-core@clanker-pack
/plugin install safety-pack@clanker-pack
/plugin install reread-guard@clanker-pack
```

Add `recommended-extras` for the optional plugins. Add `recommended-memory` only after you install the `ai-memory` binary. `recommended-pack` still installs all 15 third-party plugins in one step.

Update after new skills land:

```
/plugin marketplace update clanker-pack
```

## At a glance

| Pack | Skills | Focus |
|------|:------:|-------|
| **ui-pack** | 7 | Tailwind v4, asset sourcing, animation craft |
| **tools-pack** | 1 | Diagrams |
| **stack-pack** | 2 | Stack-specific depth: Docker, Python |
| **turn-discipline** | 1 | Short, cheap sessions: effort and compaction setup, slice runner |
| **recommended-pack** | 0 | Bundle: installs 15 plugins from other authors, such as context-mode, ai-memory, superpowers and context7 |
| **safety-pack** | 6 | Guardrails for work you cannot fully review: ship checklist, plain-language diff, safe migrations, rollback, git safety net, deploy checks, plus 3 hooks |
| **generative-pack** | 11 | Generative and creative-coding techniques by field (motion, geometry, rules and generation, physics, creative tooling, learning and inference, data and spatial, audio, shaders, image and color) |

## Packs

### ui-pack — design & front-of-house
- **tailwind-patterns** — Tailwind v4 CSS-first config, container queries, design-token architecture.
- **emil-design-eng**, **animate**, **animation-performance**, **review-animations**, **improve-animations** — Emil Kowalski's animation and UI polish skills: when to animate, easing and duration, composite-only performance, review and audit against a craft bar.
- **design-asset-sourcing** — vetted library of free illustrations, icons, SVG logos, stock photos, placeholders, patterns, fonts, palettes, UI blocks and mockup tools, with verified fetch endpoints, license rules, and a gate on whether the task needs an asset at all.

### tools-pack — utilities
- **mermaid-diagrams** — class, sequence, flowchart, ERD, C4, state, git-graph, gantt diagrams from plain requests.

### stack-pack — stack-specific depth
- **docker-expert** — multi-stage builds, image-size optimization, container security, Compose orchestration, prod deployment.
- **python-patterns** — framework selection, async patterns, type hints, project structure — teaches the decision, not a copy-paste.

### safety-pack — guardrails
Original skills and hooks for work you cannot fully review. Details, limits and tests are in the [safety-pack README](plugins/safety-pack/README.md).

- **ship-checklist** — checks the real diff for secrets, auth, input handling, dependencies and tests before work is called done.
- **explain-the-diff** — explains what changed in plain words, with the risk of each change.
- **db-migration-safe** — backup first, small reversible steps, a dry run, no drops without approval.
- **rollback-plan** — writes the way back before a risky change and checks that it exists.
- **git-safety-net** — branch and checkpoint tag before a large edit.
- **deploy-recipes** — provider-neutral pre-deploy gate, secret rules and post-deploy check.
- **Hooks** — deny or ask before destructive shell commands, deny file writes that contain a secret, and warn at 250k tokens of context.

### generative-pack — creative-coding techniques by field
Reference skills in the style of the big web-dev ones: a short `SKILL.md` that routes by goal, with per-project detail under `references/`. Each entry names a real open-source project, its verified license, the technique it embodies and how to reuse the idea without the library. These are catalogs of ideas to enrich reasoning, not drop-in solutions.

- **technique-finder** — routes a creative or generative goal to the right catalog below; start here when the field is unclear.
- **motion-time** — easing and interpolation, animation engines, vector animation formats, procedural motion and rigging, programmatic video, crowds and tracking, live-coded time.
- **geometry-structure** — curves and splines, polygons and triangulation, packing and tiling, meshes, implicit surfaces and SDFs, CAD, vector graphics and fonts.
- **rules-generation** — noise, grammars and rewriting, wave function collapse, growth and cellular automata, procedural art, tilings, maps.
- **physics-simulation** — rigid bodies and springs, fluids and PDE solvers, reaction-diffusion, N-body and molecular dynamics, light transport, atmosphere and color mixing.
- **creative-tooling** — sketch frameworks, 2D and 3D rendering libraries, audio DSP languages, shader sandboxes, GPU kernels in Python, node-graph generation, creative applications.
- **learning-inference** — diffusion and flow matching, video, music and speech models, Gaussian splatting and single-image 3D, depth, segmentation and tracking, restoration and OCR, neural cellular automata, self-play, robot learning.
- **data-spatial** — graphs and pathfinding, spatial indexes and clustering, maps and projections, chart layouts and large-data rasterization, point clouds, sun, satellite and star positions.
- **audio-signal** — synthesis and filters, Web Audio, DSP libraries, FFT and spectrograms, music information retrieval, tomography.
- **shader-effects** — antialiasing, blending, dithering, blur, post-processing effects, software rasterizers, vector-field visualization.
- **image-color-vector** — color spaces and scales, quantization, vector tracing, image art algorithms, image and video tools, distance-field text.

## Mods

A mod is a plugin with hooks instead of skills. It runs unsandboxed and sees the whole session, so each one lists the engine calls it makes and ships its tests. Read the source before you install one.

`safety-pack` also ships hooks, next to its skills. They run as commands and see the same data. See its README for what each one reads.

- **reread-guard** — refuses a repeat `Read` of an unchanged file of 8 KB or more, so its text is not added to the context twice.

## What it costs

Claude Code lists every installed skill's description in every session. `python scripts/cost.py` measures that text for each plugin. The token column is an estimate of four characters per token. Run `/context` in a real session for exact numbers.

| Plugin | Skills | Always listed (chars) | About tokens | On file match (chars) | Manual only |
|---|---:|---:|---:|---:|---:|
| generative-pack | 11 | 5189 | 1297 | 0 | 0 |
| safety-pack | 6 | 1734 | 433 | 0 | 0 |
| stack-pack | 2 | 149 | 37 | 325 | 0 |
| tools-pack | 1 | 731 | 182 | 0 | 0 |
| turn-discipline | 1 | 342 | 85 | 0 | 0 |
| ui-pack | 7 | 1752 | 438 | 115 | 2 |
| **All** | 28 | 9897 | 2474 | 440 | 2 |

The listing is small. The larger cost is a skill that loads in full, so each description says precisely when to use it. `docker-expert` and `tailwind-patterns` set `paths`, and `review-animations` and `improve-animations` are manual only.

## How the skills are tested

Each skill has an eval case in its plugin's `evals/` folder. A case sends a prompt and checks that Claude calls the skill. The `safety-pack` cases also check that no safety skill fires on an unrelated prompt. Run them with:

```
claude plugin eval plugins/safety-pack --runs 3
```

This costs tokens: about $0.05 to $0.25 per run. `generative-pack` and `turn-discipline` have no trigger cases yet. The hooks have unit tests instead, in `plugins/safety-pack/hooks/test_hooks.py`.

A second test runs an agent in a seeded project folder with and without the skill, and grades what the agent did. [benchmarks/results/skills/REPORT.md](benchmarks/results/skills/REPORT.md) lists 19 skills whose named-skill runs all passed. Skills that did not pass every run are left out of that report. Runs per cell are 1 to 3, so treat it as a first signal. Details and limits: [benchmarks/README.md](benchmarks/README.md).

## Design heuristics

The packs share a point of view:

- **Skills teach judgment, not recipes.** The Python and Tailwind skills explicitly teach *how to decide*, not snippets to paste.
- **Trigger-scoped loading.** A skill's description is a precise "use when…" so Claude loads the full skill when it is relevant and ignores it otherwise.
- **Nothing ships unchecked.** `scripts/check.py` runs in CI. It fails on broken frontmatter, scripts that a skill references but does not ship, plugin manifests that disagree with the marketplace, and a wrong skill count in this file.
- **One capability per skill.** Small, composable, independently installable — pick the packs you want.

## Attribution

Not everything here is mine. Nine skills come from other MIT-licensed projects. [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) names each one, its upstream repository, and its copyright notice.

## License

MIT. See [LICENSE](LICENSE).
