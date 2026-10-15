# Light transport, optics, atmosphere and pigment color

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **The rendering equation.** Light leaving a point = light it emits + the integral over incoming directions of (surface reflectance × incoming light × cosine). Path tracing estimates this integral by random sampling and averaging.
- **Monte Carlo and noise.** Error falls as 1/sqrt(samples). Reduce it with importance sampling (sample where the integrand is large) and multiple importance sampling (combine strategies).
- **Progressive rendering:** average each frame's samples into an accumulation buffer; the image sharpens while you watch.
- **Acceleration structures:** a bounding volume hierarchy makes ray-scene intersection logarithmic.
- **Precompute and look up.** Atmospheres and black holes are too expensive per pixel, so tabulate the physics once in textures.
- **Differentiable rendering:** make the renderer's output differentiable with respect to scene parameters, so an optimizer can fit geometry, materials or lights to images.
- **Color mixing is spectral.** Mixing RGB like paint fails; mix reflectance spectra.

## Offline renderers (references for how a full one is structured)

### pbrt-v4 — mmp/pbrt-v4
**Status:** Apache-2.0, pushed Sep 2026. Checked: README, src/pbrt/textures.h.
**Idea:** the renderer described in the book "Physically Based Rendering", whose full text is free online. The best explanation of the theory and a readable implementation: sampling, BVH, materials, lights, spectral rendering.

### appleseed — appleseedhq/appleseed
**Status:** MIT, pushed Jun 2026. Checked: README, src/appleseed.shaders/stdosl.h.
**Idea:** a physically based global illumination engine for animation and visual effects; shading is programmable with Open Shading Language (the standard OSL header ships with it).

### LuxCoreRender — LuxCoreRender/LuxCore
**Status:** Apache-2.0, pushed Oct 2026. Checked: README, topics, src/pyluxcore/pyluxcoreforblender.cpp.
**Idea:** an unbiased, physically based engine with bidirectional path tracing and CUDA support, integrated with Blender through a Python binding. Bidirectional methods trace from both the camera and the lights and join the paths, which converges faster for caustics.

### Mitsuba 3 — mitsuba-renderer/mitsuba3
**Status:** BSD-style license (head read; GitHub shows no classification), pushed Oct 2026. Checked: README, src/volumes/grid.cpp.
**Idea:** a retargetable forward and inverse renderer: one scene description, several back ends, and differentiation for inverse problems. Its volume plugins (for example the grid volume) show how participating media are described as data.

### redner — BachiLi/redner
**Status:** MIT, pushed 2022. Checked: README, src/redner.cpp.
**Principle:** differentiable rendering without approximating visibility.
**Mechanism (literature, Li et al. 2018):** the rendering integral's derivative has an interior term (smooth shading changes) and a boundary term (edges moving across pixels); the boundary term is estimated by sampling points on object silhouettes. Gradients flow to geometry, materials, lights and camera.
**Use it when:** fitting scenes to photos, inverse graphics.

### pt — fogleman/pt
**Status:** MIT, pushed 2019. Checked: README, pt/mesh.go.
**Idea:** a compact CPU path tracer in Go: OBJ and STL meshes (with a BVH tree), textures and normal maps, SDF ray marching, volume rendering from image slices, and configurable materials. A small enough codebase to read in an evening.

## Real-time and web

### THREE.js-PathTracing-Renderer — erichlof/THREE.js-PathTracing-Renderer
**Status:** CC0-1.0, pushed Oct 2026. Checked: README, shaders/Bi-Directional_PathTracing_Fragment.glsl.
**Principle:** path tracing in a fragment shader with progressive accumulation on top of Three.js.
**Mechanism:** each pixel traces a random path per frame against analytic shapes written into the shader (spheres, ellipsoids, cylinders, cones, disks; the source uses counts such as `N_SPHERES`), plus a bidirectional variant. The new sample is blended into a history buffer, so the image refines while the camera is still.
**Use it when:** interactive global illumination demos.

### diamond-webgl — piellardj/diamond-webgl
**Status:** GPL-3.0, pushed 2024. Checked: README, topics.
**Principle:** real-time ray tracing inside a gemstone.
**Mechanism (literature):** trace each ray into the gem, refract with Snell's law n1·sin(a) = n2·sin(b), reflect internally with Fresnel weights and total internal reflection up to a bounce limit, and split colors by wavelength to show dispersion. The cut is a controllable parameter. Copyleft: reimplement from the physics.

### Ray Optics Simulation — ricktu288/ray-optics
**Status:** Apache-2.0, pushed Oct 2026. Checked: README, src/core/primitive/curveRayCrossings.js.
**Principle:** 2D geometric optics: sources, mirrors, lenses, beam splitters.
**Mechanism:** trace each ray to its nearest intersection, then reflect (r = d − 2(d·n)n) or refract by Snell's law, repeat to a depth limit. Curved elements can be defined by equations; the source counts ray crossings by solving quadratics for even-odd region tests.
**Use it when:** teaching optics, lens and mirror layouts.

## Atmosphere and color

### Precomputed Atmospheric Scattering — ebruneton/precomputed_atmospheric_scattering
**Status:** BSD-3-Clause, pushed Oct 2025. Checked: README, tools/docgen_main.cc.
**Principle:** realistic skies from tabulated scattering (EGSR 2008).
**Mechanism (literature):** model Rayleigh scattering (air molecules, blue sky) and Mie scattering (aerosols, haze) with density falling exponentially with altitude; precompute transmittance and single and multiple scattering into lookup textures indexed by altitude, view angle, sun angle and relative azimuth; the shader reads them per pixel, so sunsets and aerial perspective cost almost nothing at runtime. This implementation adds names, comments, tests and documentation.
**Use it when:** sky, planets, aerial perspective.

### Spectral.js — rvanwijnen/spectral.js
**Status:** MIT, pushed Jan 2026. Checked: README, a bundled demo script.
**Principle:** mix colors like paint, using Kubelka-Munk theory, so blue and yellow make green.
**Mechanism (literature):** represent each color as a reflectance spectrum; for each wavelength, K/S = (1 − R)² / (2R) (absorption over scattering); mix by taking the weighted sum of K/S values by concentration; convert back with R = 1 + K/S − sqrt((K/S)² + 2·K/S); then convert the spectrum to RGB.
**Use it when:** painting apps, gradients that avoid muddy mid-tones.
