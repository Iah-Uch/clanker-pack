# clanker-pack

A personal Claude Code plugin marketplace — 16 skills across 4 focused packs. Each pack is a plugin you install independently. An installed skill adds its description to every session's skill list, and Claude loads the full skill only when the description matches the task. Install only the packs you use.

## Install

```
/plugin marketplace add Iah-Uch/clanker-pack

/plugin install ui-pack@clanker-pack         # Tailwind v4, asset sourcing
/plugin install tools-pack@clanker-pack      # diagrams
/plugin install stack-pack@clanker-pack      # Docker, Python
/plugin install generative-pack@clanker-pack # generative and creative-coding techniques
```

Two mods, installed the same way:

```
/plugin install cache-keeper@clanker-pack   # keeps the prompt cache warm, holds a cold send once
/plugin install reread-guard@clanker-pack   # refuses a repeat Read of an unchanged large file
```

Update after new skills land:

```
/plugin marketplace update clanker-pack
```

## At a glance

| Pack | Skills | Focus |
|------|:------:|-------|
| **ui-pack** | 2 | Tailwind v4, asset sourcing |
| **tools-pack** | 1 | Diagrams |
| **stack-pack** | 2 | Stack-specific depth: Docker, Python |
| **generative-pack** | 11 | Generative and creative-coding techniques by field (motion, geometry, rules and generation, physics, creative tooling, learning and inference, data and spatial, audio, shaders, image and color) |

## Packs

### ui-pack — design & front-of-house
- **tailwind-patterns** — Tailwind v4 CSS-first config, container queries, design-token architecture.
- **design-asset-sourcing** — vetted library of free illustrations, icons, SVG logos, stock photos, placeholders, patterns, fonts, palettes, UI blocks and mockup tools, with verified fetch endpoints, license rules, and a gate on whether the task needs an asset at all.

### tools-pack — utilities
- **mermaid-diagrams** — class, sequence, flowchart, ERD, C4, state, git-graph, gantt diagrams from plain requests.

### stack-pack — stack-specific depth
- **docker-expert** — multi-stage builds, image-size optimization, container security, Compose orchestration, prod deployment.
- **python-patterns** — framework selection, async patterns, type hints, project structure — teaches the decision, not a copy-paste.

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

- **cache-keeper** — keeps the one-hour prompt cache warm during breaks, refuses a cold send once with its rewrite price, and reports cache breaks. Follows the design of cache-tax.
- **reread-guard** — refuses a repeat `Read` of an unchanged file of 8 KB or more, so its text is not added to the context twice.

## Design heuristics

The packs share a point of view:

- **Skills teach judgment, not recipes.** The Python and Tailwind skills explicitly teach *how to decide*, not snippets to paste.
- **Trigger-scoped loading.** A skill's description is a precise "use when…" so Claude loads the full skill when it is relevant and ignores it otherwise.
- **Nothing ships unchecked.** `scripts/check.py` runs in CI. It fails on broken frontmatter, scripts that a skill references but does not ship, plugin manifests that disagree with the marketplace, and a wrong skill count in this file.
- **One capability per skill.** Small, composable, independently installable — pick the packs you want.

## Attribution

Not everything here is mine. Four skills and one mod come from other MIT-licensed projects. [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) names each one, its upstream repository, and its copyright notice.

## License

MIT. See [LICENSE](LICENSE).
