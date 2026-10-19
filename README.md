# clanker-pack

A personal Claude Code plugin marketplace — 23 skills across 5 focused packs. Each pack is a plugin you install independently; each skill loads only when its triggers match, so you carry the capability without paying the context cost until you need it.

## Install

```
/plugin marketplace add Iah-Uch/clanker-pack

/plugin install ui-pack@clanker-pack         # design systems, theming, perf
/plugin install quality-pack@clanker-pack    # research-backed writing
/plugin install tools-pack@clanker-pack      # diagrams, PDFs, testing, file org
/plugin install stack-pack@clanker-pack      # Docker, Python
/plugin install generative-pack@clanker-pack # generative and creative-coding techniques
```

Update after new skills land:

```
/plugin marketplace update clanker-pack
```

## At a glance

| Pack | Skills | Focus |
|------|:------:|-------|
| **quality-pack** | 1 | Research-backed writing |
| **ui-pack** | 5 | Design systems, Tailwind v4, theming, asset sourcing, web performance |
| **tools-pack** | 4 | Diagrams, PDF processing, web-app testing, file organization |
| **stack-pack** | 2 | Stack-specific depth: Docker, Python |
| **generative-pack** | 11 | Generative and creative-coding techniques by field (motion, geometry, rules and generation, physics, creative tooling, learning and inference, data and spatial, audio, shaders, image and color) |

## Packs

### quality-pack — writing
- **content-research-writer** — research-backed writing with citations, hooks, outline iteration, and section-level feedback.

### ui-pack — design & front-of-house
- **ui-design-system** — design tokens, component docs, responsive calculations, design→dev handoff.
- **tailwind-patterns** — Tailwind v4 CSS-first config, container queries, design-token architecture.
- **theme-factory** — apply one of 10 preset themes (or generate one) to slides, docs, reports, landing pages.
- **design-asset-sourcing** — vetted library of free illustrations, icons, SVG logos, stock photos, placeholders, patterns, fonts, palettes, UI blocks and mockup tools, with verified fetch endpoints, license rules, and a gate on whether the task needs an asset at all.
- **web-performance-optimization** — Core Web Vitals, loading speed, bundle size, caching, runtime performance.

### tools-pack — utilities
- **mermaid-diagrams** — class, sequence, flowchart, ERD, C4, state, git-graph, gantt diagrams from plain requests.
- **pdf-processing-pro** — production PDF workflows: forms, tables, OCR, validation, batch operations.
- **webapp-testing** — drive and test local web apps with Playwright: verify UI, capture screenshots, read browser logs.
- **file-organizer** — context-aware cleanup: dedupe, restructure, and reorganize directories.

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

## Design heuristics

The packs share a point of view:

- **Skills teach judgment, not recipes.** The Python and Tailwind skills explicitly teach *how to decide*, not snippets to paste.
- **Trigger-scoped loading.** A skill's description is a precise "use when…" so Claude loads it exactly when relevant and ignores it otherwise — keeping context lean.
- **Process before implementation.** Debugging, review, and git skills gate *how* work happens; they run before the domain skills that do it.
- **The human owns and approves the work.** Nothing commits without explicit approval, and work is never attributed to the AI.
- **One capability per skill.** Small, composable, independently installable — pick the packs you want.

## Attribution

Not everything here is mine. This repo is a mix of skills I built and ones I found useful around the web and collected into one place. Credit for the latter belongs to their original authors.

## License

MIT
