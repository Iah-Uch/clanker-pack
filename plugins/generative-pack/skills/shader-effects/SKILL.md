---
name: shader-effects
description: "Use when writing shaders and screen effects: antialiased edges, blend modes, dithering, halftone, Gaussian blur, FXAA, color lookup tables, Blinn-Phong, hatching, bloom, depth of field, motion blur, SSAO, outlines, glitch, datamosh, fog, kaleidoscope, watercolor, video-synth chains, software rasterizers, terrain by heightmap, line integral convolution of vector fields. A catalog of techniques with mechanisms and formulas, to reason from, not a set of drop-in libraries."
---

# Shader and effect techniques

A catalog of ideas drawn from about 27 open-source projects: the small, well-understood tricks behind screen effects, stylized shading and classic rendering.

## Read this first

- **These are not drop-in solutions.** A project is an example of a technique. Many are old WebGL1 or Unity-specific modules. Abstract the idea, write the modern version for the user's engine.
- **Do not assume a module does what its name suggests.** Each entry says what I checked; "literature" marks the standard technique rather than the project's code. Check the target platform's requirements (half-float targets, derivatives, motion vectors).
- **Licenses matter when you reuse code.** MIT, ISC, BSD, zlib, Unlicense: adapt with notices. AGPL (Hydra Synth): take the design only. Some Kino packages show no license on GitHub but carry MIT-style text in the README; verify before copying.
- Facts were checked against each repository on 2026-10-15; projects change.

## Pick by goal

| You want | Read |
|---|---|
| Antialiased edges, blend modes, dithering, halftone, blur, FXAA, LUT grading, specular, hatching, shader chains | `references/01-glsl-building-blocks.md` |
| Bloom, depth of field, motion blur, SSAO, outlines, glitch, datamosh, fog, kaleidoscope, watercolor, anamorphic flare, analog video | `references/02-post-processing-effects-kino.md` |
| Writing a rasterizer, heightmap terrain without polygons, visualizing a vector field with LIC | `references/03-classic-rendering-and-flow-visualization.md` |

## Ideas that recur

- A pass is a function from textures to a texture; chain passes.
- Use derivatives and smoothstep for edges that stay crisp at any scale.
- Separate filters, pyramids and linear-sampling tricks make large blurs cheap.
- Pick the buffer that carries the signal: depth, normals, motion, color.
- Bake expensive color transforms into lookup tables.
- Work in linear light, convert at the ends.

## How to answer with this

1. Match the goal to a reference and read only that file.
2. Explain the technique and its formula in terms of the user's engine; mention a project as an example with its license.
3. Write the shader fresh for the target platform; do not paste code from copyleft or unlicensed projects.
