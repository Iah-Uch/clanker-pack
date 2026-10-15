# Procedural art, tilings, terrain and search

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Seeded randomness.** Derive everything from one seed (a small PRNG such as xorshift or mulberry32), so a result is reproducible and shareable as a string.
- **Parameters define a species.** Model a thing (a fish, a flower, a mountain) as a structure with parameters; one seed picks the values, so every output is a new individual of the same kind.
- **Imperfect strokes read as hand-made.** Draw each line a bit wrong: jitter, overshoot, repeat, vary width and pressure.
- **Hierarchy gives aperiodic order.** Aperiodic tilings come from substitution: groups of tiles are replaced by larger tiles, over and over.
- **Search with pruning for puzzles.** Split a huge search into stages whose subproblems are small and precomputed.

## Entries

### Rough.js — rough-stuff/rough
**Status:** MIT, 21k★, pushed 2024. Checked: README, src/renderer.ts.
**Principle:** make clean shapes look sketched.
**Mechanism:** each line or curve is drawn as more than one stroke with random offsets and slight bowing, controlled by roughness and bowing options; closed shapes are filled by fillers (hachure, cross-hatch, zigzag, dots, solid); SVG paths are parsed and normalized first; the random number generator is seeded so a drawing is stable.
**Use it when:** diagrams and UI with a hand-drawn feel.

### p5.brush — acamposuribe/p5.brush
**Status:** MIT, pushed Oct 2026. Checked: README, src/stroke/stroke.js imports.
**Principle:** natural media (pencil, charcoal, marker, watercolor) on a canvas.
**Mechanism (inferred from the modules; check the docs):** a stroke is a polyline with pressure, drawn as many small marks with Gaussian jitter and noise; fills layer translucent washes; hatching lays parallel lines at an angle; vector fields can bend strokes so they follow a flow. Color mixing and seeded randomness are core utilities.
**Use it when:** generative art that should look painted.

### fishdraw — LingDong-/fishdraw
**Status:** MIT, pushed 2021. Checked: README, fishdraw.js.
**Principle:** one seed generates a whole, plausible, drawable fish as polylines.
**Mechanism:** a xorshift random generator (shift-xor steps on a 32-bit state) seeded from a string, p5-style Perlin noise (4 octaves) for organic variation, and parametric body, fin and pattern construction output as polylines (SVG, JSON, CSV, even an animation of the drawing). Single file, no dependencies, aimed at pen plotters.
**Use it when:** procedural creatures; a template for "species from a seed".

### Nonflowers — LingDong-/nonflowers
**Status:** MIT, pushed 2021. Checked: README; the file head only defines array helpers.
**Idea:** paintings of invented flowers in the Gongbi style, from a structural model of plants (stem, leaves, petals) plus a simulated brush with varying width and texture. The README describes the goal as capturing plant structure and delicate brushwork.

### Shan Shui Infinite — LingDong-/shan-shui-inf
**Status:** MIT, pushed 2018. Checked: README only.
**Idea:** an endless scrolling Chinese landscape produced from noise and mathematical functions that model mountains and trees from scratch, as vector output. Because everything is a function of position and a seed, new stretches can be generated on demand.

### Trianglify — qrohlf/trianglify
**Status:** GPL-3.0, pushed 2025. Checked: README, src/trianglify.js imports.
**Principle:** low-poly gradient backgrounds.
**Mechanism:** scatter points on a jittered grid, triangulate (Delaunator), then color each triangle by sampling a color scale at its center in a 2D gradient field (chroma-js scales and ColorBrewer palettes), with a seeded random generator (mulberry32). Output as SVG or canvas.
**Use it when:** backgrounds. Copyleft: reimplement from the recipe; it is short.

### hatviz — isohedral/hatviz
**Status:** BSD-3-Clause, pushed 2023. Checked: README, geometry.js.
**Principle:** the "hat" is a single tile that tiles the plane only aperiodically (discovered 2023).
**Mechanism (literature):** hats are built from kites on a hexagonal lattice (the code converts lattice coordinates with x + y/2 and (sqrt(3)/2)·y) and placed by 2x3 affine matrices; patches grow by substitution into metatiles and supertiles, which the app draws as outlines.
**Use it when:** aperiodic patterns, hierarchical substitution tilings.

### mapgen4 — redblobgames/mapgen4
**Status:** Apache-2.0, unmaintained badge, pushed Mar 2026. Checked: README, mapgen4.ts parameters.
**Principle:** a wilderness map that regenerates in real time as you paint the terrain, tuned to look good rather than be realistic (README).
**Mechanism (literature, the author's write-up; not read in code):** a Delaunay and Voronoi mesh; painted elevation constraints plus noise; wind drives moisture that falls as rain over rising terrain; rivers follow downhill flow and accumulate; biomes come from elevation and moisture.
**Use it when:** game maps, fantasy worldbuilding, interactive terrain.

### RubiksCube-TwophaseSolver — hkociemba/RubiksCube-TwophaseSolver
**Status:** GPL-3.0, pushed Jul 2026. Checked: README, solver.py imports.
**Principle:** Kociemba's two-phase algorithm solves a cube in under 19 moves on average.
**Mechanism (literature; module names confirm the structure):** phase 1 searches for moves that bring the cube into the subgroup reachable with only U, D, R2, L2, F2 and B2 (corner and edge orientation fixed, slice edges in the middle layer); phase 2 solves inside that subgroup. Positions are encoded as small integer coordinates; move tables and pruning tables (the repo has coordinate, move, pruning and symmetry modules) drive an iterative-deepening search, run on several threads.
**Use it when:** puzzle solving by staged search with precomputed lower bounds.
