---
name: technique-finder
description: Use first when a creative, generative, graphics, audio, simulation, map or data-visualization task does not obviously map to one field, or when the user asks how something visual or procedural could be made. Routes the goal to the right technique catalog (motion, geometry, rules and generation, physics, tooling, learned models, data and spatial, audio, shaders, image and color). Catalogs of ideas, not drop-in solutions.
---

# Technique finder

The generative pack is ten catalogs of techniques drawn from about 400 open-source creative and generative projects. Each catalog explains the principle, the mechanism (formulas or steps), when to use it, and how to build it without the original project. This skill picks the catalog.

## Read this first

- The catalogs are **ideas to reason from, not drop-in solutions.** Repositories change, may not fit the user's stack, and carry licenses that limit code reuse (copyleft means take the technique only; "no license detected" means do not copy code).
- Say where a technique came from only as an example. Recommend a library when it fits the user's constraints, never by default, and never install anything without consent.
- Facts in the catalogs were checked on 2026-10-15.

## Route by goal

| The goal sounds like | Skill |
|---|---|
| Easing, interpolation, springs, timelines, animation engines, vector animation formats (Lottie), procedural rigging, programmatic video, crowds, live-coded time | `motion-time` |
| Curves and splines, polygons, hulls, triangulation, Voronoi, packing, tiling, sampling, spatial structure of shapes, meshes, implicit surfaces, SDFs, CAD, fonts, fabrication paths | `geometry-structure` |
| Noise and randomness, grammars, L-systems, wave function collapse, constraints, cellular automata, growth, aggregation, agents, procedural maps and art, search | `rules-generation` |
| Rigid bodies, cloth, springs, fluids, PDEs, waves, reaction-diffusion, N-body, molecular dynamics, path tracing, optics, atmosphere, pigment mixing | `physics-simulation` |
| Which framework, renderer, audio language or GPU tool to build with: p5, Three.js, regl, PixiJS, Faust, Taichi, ComfyUI | `creative-tooling` |
| Diffusion, video, speech and music models, Gaussian splatting, single-image 3D, depth, segmentation, tracking, restoration, OCR, embeddings, self-play, robot learning | `learning-inference` |
| Graphs, force layout, pathfinding, spatial indexes, clustering, map projections, tiles, globes, treemaps, sankey, rasterizing millions of points, point clouds, sun and satellite positions | `data-spatial` |
| Oscillators, filters, FM, Web Audio, FFT, spectrograms, pitch and onset detection, MFCCs, tomography, images as sound | `audio-signal` |
| Antialiasing, blend modes, dithering, blur, bloom, depth of field, SSAO, glitch, software rasterizers, vector-field visualization | `shader-effects` |
| Color spaces and scales, quantization, vectorization, skeletons, seam carving, triangulated or stippled art, image and video libraries, SDF text | `image-color-vector` |

## Tasks that span fields

Pick the main skill, then read the one that supplies the missing piece.

- Procedural terrain: `rules-generation` (noise), `data-spatial` (mesh levels of detail), `physics-simulation` (erosion, rivers), `shader-effects` (heightmap rendering).
- Generative music visualizer: `audio-signal` (spectra), `shader-effects`, `motion-time`, `creative-tooling`.
- Plotter or fabrication art: `geometry-structure`, `image-color-vector` (tracing, stippling), `rules-generation`.
- Interactive data art: `data-spatial`, `motion-time`, `creative-tooling`.
- Photo to stylized 3D or animation: `learning-inference` (depth, segmentation), `shader-effects`, `motion-time`.

## Not covered

Four index entries had no resolvable repository and are not in the catalogs: Terrain Erosion, Genesis World, Particle Life, BookBookBook. One entry is not a creative technique (a NAS build template) and is listed only for completeness.

## How to answer with this

1. Route to one or two skills and read only the reference files they name.
2. Explain the technique in terms of the user's problem first, then mention projects as examples with their licenses.
3. Combine techniques freely; the point of the catalogs is to enrich thinking about related tasks, not to select a package.
