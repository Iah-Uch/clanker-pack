# Noise and randomness

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Coherent noise** is random but smooth: values at nearby points are close. Build it from a lattice of random values or gradients and an interpolation rule, evaluated per point with no stored image.
- **Octaves (fractal Brownian motion):** sum noise at doubling frequency and shrinking amplitude: n(p) + n(2p)/2 + n(4p)/4... for natural detail. Ridged and turbulence variants take absolute values or fold the signal.
- **Domain warping:** feed noise into the coordinates of another noise for flowing, organic shapes.
- **Cellular (Worley) noise:** distance to the nearest of many jittered feature points, giving cells, cracks and stone.
- **Stateless hashing:** a GPU shader has no random state, so it hashes the coordinates into a pseudo-random number.

## Entries

### simplex-noise.js — jwagner/simplex-noise.js
**Status:** MIT, pushed 2024. Checked: README, simplex-noise.ts constants.
**Principle:** simplex noise: gradient noise on a simplex grid, which needs fewer corners than Perlin noise and has fewer directional artifacts.
**Mechanism:** skew input coordinates by F = (sqrt(n+1) − 1)/n into a grid of unit hypercubes, each split into n! simplices (triangles in 2D, tetrahedra in 3D); find the simplex containing the point; unskew by G = (1 − 1/sqrt(n+1))/n to get offsets from each of the n+1 corners; each corner contributes max(0, r² − d²)^4 times the dot of its pseudo-random gradient with the offset; sum the contributions. The constants F2, G2, F3, G3, F4, G4 in the source are exactly these. About 2 KB, around 20 ns per 2D sample.
**Use it when:** terrain, clouds, textures, flow fields, in any JavaScript project.
**Build it yourself:** the algorithm above, plus a hashed permutation table for gradient choice.

### OpenSimplex2 — KdotJPG/OpenSimplex2
**Status:** CC0-1.0, pushed 2024. Checked: README, java/OpenSimplex2S.java.
**Principle:** successors to OpenSimplex, which used a different grid than classic simplex and gave uneven contrast in 3D and 4D.
**Mechanism:** instead of rearranging vertices, it builds congruent point layouts and transforms them (README); smooth (`S`) and fast (`F`) variants; coordinates are hashed with large prime multipliers and a seed. Provides 2D, 3D and 4D.
**Use it when:** you want simplex-style noise in public domain with better isotropy.

### FastNoise Lite — Auburn/FastNoiseLite
**Status:** MIT, pushed Jun 2026. Checked: README, WebPreviewApp/main.cpp.
**Idea:** one portable library (C, C++, C#, Java, GLSL, HLSL, JavaScript, Rust, Go and more) offering several noise types (simplex variants, Perlin, value, cubic, cellular) with fractal layering and domain warp behind one interface, tuned for speed; a web preview lets you explore parameters.
**Use it when:** you need the same noise on CPU and GPU, or in several languages.

### libnoise — eXpl0it3r/libnoise
**Status:** LGPL-2.1, pushed Oct 2026. Checked: README, src/noisegen.cpp.
**Principle:** build terrain and textures by connecting noise "modules" into a graph.
**Mechanism:** generators (Perlin, ridged multifractal) feed modifiers and combiners (the module-graph design is described in its docs); the source keeps a version switch between the current coherent-noise function and the flawed original so old results can be reproduced.
**Use it when:** planetary terrain and height maps from composed noise. Copyleft: study the structure, do not port code.

### glsl-worley — Erkaman/glsl-worley
**Status:** MIT (LICENSE read; GitHub shows no classification), pushed 2016. Checked: README, worley3D.glsl.
**Principle:** Worley (cellular) noise computed in a fragment shader (Stefan Gustavson's implementation).
**Mechanism:** divide space into unit cells; jitter one or several feature points per cell with a hashed permutation (the code uses permute(x) = mod((34x + 1)x, 289)); for a pixel, search the neighboring cells for the nearest points; return the nearest and second-nearest distances (F1 and F2) with a jitter parameter and an optional Manhattan distance. F2 − F1 gives cracks and cell edges.
**Use it when:** stone, scales, cells, Voronoi-like textures.

### psrdnoise — stegu/psrdnoise
**Status:** MIT per file header (GitHub shows none), pushed 2023. Checked: README, src/psrdnoise3.wgsl header.
**Idea:** simplex noise that tiles (periodic) and has rotating gradients, which animates as flow; GLSL and WGSL versions, plus a 16-bit-float-friendly 2D variant. Gradients rotating over time make smooth swirling motion.
**Use it when:** seamless tiling textures and flowing animation.

### glsl-random — mattdesl/glsl-random
**Status:** BSD-3-Clause, pushed 2015. Checked: README.
**Principle:** the classic one-line shader hash for a 2D coordinate.
**Mechanism (the well-known form):** fract(sin(dot(p, vec2(12.9898, 78.233))) × 43758.5453). It is cheap but not high quality, and it depends on float precision, so the module offers a high-precision version and a classic one for mobile GPUs.
**Use it when:** dithering, jitter, grain. Not for anything needing statistical quality.

### d3-random — d3/d3-random
**Status:** ISC, pushed 2023. Checked: README only.
**Idea:** random number generators for many distributions (uniform, normal and others in its API docs) with a seedable source, so generative work can be reproduced.
**Use it when:** you need non-uniform randomness with a seed.
