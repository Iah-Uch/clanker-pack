# GLSL building blocks: antialiasing, blending, dithering, blur, color lookup, lighting, composition

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published technique, not this project's code. Most of these are small modules written for the old glslify and WebGL1 era: read them for the math, then write the modern version (WebGL2, WebGPU or compute) yourself.

## Cross-cutting ideas

- **A fragment shader is a pure function of position.** color = f(uv, time, textures). Compose effects by feeding one pass's output texture into the next (a render-to-texture chain).
- **Screen-space derivatives.** `fwidth(x)` (about |dFdx| + |dFdy|) tells how fast a value changes per pixel; a smoothstep whose width equals fwidth gives edges that stay one pixel soft at any zoom.
- **Separable filters.** A 2D Gaussian blur equals a horizontal pass then a vertical pass, N taps each instead of N². Taps can be halved by sampling between two texels and letting the hardware's bilinear filter do the weighting.
- **Ordered dithering.** Compare a pixel's value to a threshold from a tiled matrix indexed by (x mod n, y mod n); the Bayer matrix of size 2n is built recursively from size n.
- **Color as a lookup.** Any per-pixel color transform can be baked into a lookup table texture (LUT) that the shader indexes with the input color.
- **Work in linear light.** Blending, blurring and lighting are physically meaningful in linear space; convert from sRGB first (c^2.2 approximately, or the exact piecewise curve) and back at the end.

## Entries

### glsl-aastep — glslify/glsl-aastep
**Status:** MIT, about 150 stars, pushed Apr 2015. Checked: README.
**Principle:** an antialiased `step`. aastep(threshold, value) = smoothstep(threshold − w, threshold + w, value) with w = 0.7·length(vec2(dFdx(value), dFdy(value))) (the README describes standard derivatives, falling back to a hard `step` without them).
**Use it when:** crisp shapes, SDF text and procedural patterns at any zoom, without supersampling.

### glsl-blend — jamieowen/glsl-blend
**Status:** MIT, about 1.1k stars, pushed Jun 2022. Checked: README, all.glsl (a `blendMode` dispatcher over the modes).
**Principle:** Photoshop blend modes as functions of (base, blend) colors. Standard formulas: multiply a·b, screen 1 − (1−a)(1−b), overlay (a < 0.5 ? 2ab : 1 − 2(1−a)(1−b)), soft light, color dodge a/(1−b), color burn 1 − (1−a)/b, difference |a−b|, exclusion a + b − 2ab; an opacity parameter mixes the result with the base.
**Use it when:** layered compositing in shaders.

### glsl-dither — hughsk/glsl-dither
**Status:** MIT (license text read; GitHub shows no classification), about 225 stars, pushed Jun 2014. Checked: LICENSE head, README, 8x8.glsl.
**Principle:** Bayer matrix ordered dithering (2x2, 4x4, 8x8). The source hardcodes the 64-entry threshold table (values k/64 spread so consecutive indices are far apart) and returns 1 when the brightness exceeds the entry.
**Mechanism (literature):** the Bayer matrix recursion M_{2n} = [[4M_n, 4M_n + 2], [4M_n + 3, 4M_n + 1]], normalized by the cell count; add the matrix value (centered) to the pixel before quantizing to the target palette.
**Use it when:** retro looks, banding removal, limited palettes.

### glsl-fast-gaussian-blur — Experience-Monks/glsl-fast-gaussian-blur
**Status:** MIT, about 750 stars, pushed Jun 2016. Checked: README, tools/coefficients.js.
**Principle:** the linear-sampling trick: take a row of binomial (Pascal) weights as the kernel (the tool uses `28 56 70 56 28` for 5 taps), and merge each pair of adjacent taps into one fetch at offset t = (o1·w1 + o2·w2) / (w1 + w2) with combined weight w1 + w2, so bilinear filtering reproduces both. Halves the texture reads of a separable blur. The code in the tool is exactly that merge.
**Use it when:** bloom, depth of field, frosted glass on weak GPUs.

### glsl-fxaa — mattdesl/glsl-fxaa
**Status:** MIT, about 350 stars, pushed Oct 2015. Checked: README, fxaa.glsl.
**Principle:** FXAA v2: a post-process that finds edges from luma contrast in the 3x3 neighborhood and blurs along the edge direction.
**Mechanism (read in the source):** sample the four diagonal neighbors and the center; compute luma with a dot product; edge direction dir = (−((lumaNW + lumaNE) − (lumaSW + lumaSE)), (lumaNW + lumaSW) − (lumaNE + lumaSE)); scale dir by the smallest component so it spans about one pixel, with the constants FXAA_REDUCE_MIN, FXAA_REDUCE_MUL and FXAA_SPAN_MAX; take samples along dir and choose between a narrow and a wide average depending on whether the result's luma stays within the local min and max.
**Use it when:** cheap antialiasing where MSAA is unavailable (deferred or post-processed scenes). Softens textures slightly.

### glsl-halftone — glslify/glsl-halftone
**Status:** MIT, about 50 stars, pushed Apr 2015. Checked: README.
**Principle:** a halftone screen: rotate the pixel grid by an angle, find the nearest cell center, draw a dot whose radius grows with the local brightness (or ink coverage per channel for CMYK screens at four angles), antialiased by derivatives. Adapted from Stefan Gustavson's tutorial per the README.

### glsl-lut — mattdesl/glsl-lut
**Status:** MIT, about 185 stars, pushed Jun 2024. Checked: README.
**Principle:** color grading with a 2D lookup table (512×512 laid out as a grid of tiles for the blue channel, per the README, because 3D textures are not assumed): blue picks the tile, red and green pick the position inside it, and two neighboring tiles are blended for smooth blue interpolation.
**Use it when:** film looks, Instagram-style filters, any color transform you can bake once.

### glsl-specular-blinn-phong — glslify/glsl-specular-blinn-phong
**Status:** MIT, about 12 stars, pushed Aug 2017. Checked: README.
**Mechanism:** with the half vector H = normalize(L + V), specular = max(0, dot(N, H))^shininess. Cheaper and better behaved than Phong's reflection vector, and the basis of many stylized shaders.

### gl-react — gre/gl-react
**Status:** MIT, about 3k stars, pushed Oct 2026. Checked: README.
**Principle:** shaders as React components: a `Node` has a fragment shader and uniforms, and any uniform can be another `Node`, which renders to a texture first; the tree is the effect chain. Implementations exist for the DOM (WebGL) and React Native.
**Use it when:** declarative composition of image and video effects inside a React app.

### HatchingShader — nkihrk/HatchingShader
**Status:** MIT, about 120 stars, pushed Mar 2021. Checked: README (in Japanese).
**Principle:** hatching with a Tonal Art Map: a set of stroke textures from light to dark, selected and blended per pixel by the lighting intensity, so shading looks hand-drawn; the repository ships tone-style and pencil-style maps and options to mask outlines. A Unity shader.
**Mechanism (literature, Praun et al. 2001):** mipmapped TAMs keep stroke density constant under zoom; the lighting value picks two adjacent tones and interpolates.

### Hydra Synth — hydra-synth/hydra-synth
**Status:** AGPL-3.0, about 400 stars, pushed Jul 2026. Checked: README.
**Idea:** a video synth engine for live coding: chain functions in JavaScript (`osc().rotate().modulate(noise()).out()`), each compiled into one fragment shader; sources (oscillators, noise, camera, video), geometry, color, blend and modulation functions compose like patch cables. AGPL: take the design (function chain compiled to GLSL), not the code, for closed or networked products.
