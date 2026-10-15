# Post-processing effects (the Kino collection for Unity)

A catalog of ideas. The projects are examples of each effect, not drop-in solutions. "Checked" says what I read; "literature" marks the standard technique for that effect, not this project's code. These are Unity packages; the techniques are engine-independent and map to any renderer with render targets.

## License note

Licenses vary. Where GitHub shows "none" (KinoBokeh, KinoFog, KinoGlitch, KinoMirror) the README ends with an MIT-style permission text, which I read; GitHub did not classify it, so verify the file in the repository before reuse. Unlicense (KinoAqua, KinoDatamosh) is public-domain dedication. The others are MIT.

## Cross-cutting ideas

- **Post-processing is a chain of full-screen passes** over the rendered color, depth, normal and motion-vector buffers.
- **Pyramids make wide filters cheap.** Downsample repeatedly, filter at low resolution, upsample and add: a blur of any radius costs a few small passes.
- **Use the right buffer.** Depth for fog, focus and outlines; normals for outlines and AO; motion vectors for blur and datamosh; color for everything else.
- **Cheap tricks are fine.** Several authors say their effect is a "quick hack" or not physically correct. Stylization rarely needs correctness.
- **Check platform needs.** Many effects need half-float render textures or motion-vector formats, which some mobile GPUs lack.

## Entries

### KinoBloom — keijiro/KinoBloom
**Status:** MIT, about 1k stars, pushed Apr 2017. Checked: README.
**Mechanism (literature):** keep pixels above a threshold with a soft knee (a quadratic ramp so the cutoff is gradual), build a mip pyramid by downsampling with a small filter, upsample each level and add to the one above, then add the result to the image with an intensity. Parameters in the README: threshold (in gamma space), soft knee, intensity.

### KinoBokeh — keijiro/KinoBokeh
**Status:** README ends with MIT-style permission text; GitHub shows none. About 400 stars, pushed Jan 2017. Checked: README.
**Mechanism (literature):** thin-lens depth of field: the circle of confusion for depth z is coc = A·f·|z − d| / (z·(d − f)), with aperture A, focal length f and focus distance d; the pass samples a disk (Poisson or spiral) scaled by coc, weighting samples by their own coc to avoid sharp foreground leaking onto blur. Needs half-float render targets.

### KinoMotion — keijiro/KinoMotion
**Status:** MIT, about 660 stars, pushed Sep 2017. Checked: README.
**Mechanism (literature):** render per-pixel motion vectors (current minus previous clip-space position), then blur by averaging samples along the vector over the shutter interval; neighbor-max tiles spread fast objects' blur over their surroundings.

### KinoObscurance — keijiro/KinoObscurance
**Status:** MIT, about 330 stars, pushed Oct 2017. Checked: README.
**Mechanism (literature):** screen-space ambient obscurance: for each pixel, reconstruct view-space position from depth, sample points in a hemisphere around the normal, count how many are behind the stored depth (occluded), darken by the occluded fraction, then blur with a depth-aware filter to remove noise.

### KinoContour — keijiro/KinoContour
**Status:** MIT, about 480 stars, pushed Oct 2018. Checked: README.
**Mechanism (literature):** edge detection on color, depth or normals (three sources, per the README): compare a pixel to neighbors (Roberts cross or Sobel); a large difference draws a line with chosen color and opacity. Depth and normal edges give clean silhouettes without texture noise.

### KinoBinary — keijiro/KinoBinary
**Status:** MIT, about 240 stars, pushed Nov 2017. Checked: README.
**Mechanism (literature; the README credits the blue-noise textures):** threshold the luminance with a blue-noise texture instead of a constant (the README credits Christoph Peters for the textures): out = luma > noise ? 1 : 0. Blue noise pushes error into high frequencies, giving a pleasing dithered black and white.

### KinoGlitch — keijiro/KinoGlitch
**Status:** README MIT-style text; GitHub shows none. About 2.8k stars, pushed Dec 2023. Checked: README.
**Mechanism:** two families, per the README. Analog glitch: scanline jitter, color drift, vertical jump and horizontal shake: offset UV by noise keyed to the row and time, shift color channels separately. Digital glitch: blocks of the image displaced or corrupted.

### KinoTube — keijiro/KinoTube
**Status:** MIT, about 190 stars, pushed Oct 2017. Checked: README (marked "still under development").
**Mechanism (literature):** analog video: scanlines, chroma bleeding (blur the chroma channels more than luma in YIQ), noise and slight screen distortion.

### KinoStreak — keijiro/KinoStreak
**Status:** MIT, about 190 stars, pushed Aug 2017. Checked: README ("quick and dirty hack", not physically correct).
**Mechanism (literature):** an anamorphic lens flare: extract the bright pixels, blur them strongly in the horizontal direction only (a pyramid stretched in one axis), tint blue, and add back.

### KinoMirror — keijiro/KinoMirror
**Status:** README MIT-style text; GitHub shows none. About 160 stars, pushed Aug 2015. Checked: README.
**Mechanism (literature):** fold the UV coordinates: reflect across an axis (mirror) or reduce the polar angle modulo 2·pi/n and mirror inside each sector (kaleidoscope), then sample the image.

### KinoDatamosh — keijiro/KinoDatamosh
**Status:** Unlicense, about 540 stars, pushed Oct 2021. Checked: README.
**Mechanism (literature):** simulate a dropped keyframe in video compression: keep the previous output, and instead of showing new frames move its blocks by the new frame's motion vectors, accumulating drift; blocks refresh randomly. Needs motion vectors.

### KinoFog — keijiro/KinoFog
**Status:** README MIT-style text; GitHub shows none. About 980 stars, pushed Jul 2015. Checked: README.
**Mechanism:** distance fog f = 1 − exp(−density·d) (or linear or squared); the twist in this package is **fade to skybox**: the fog color is the skybox sample in the view direction, so horizons blend seamlessly.

### KinoAqua — keijiro/KinoAqua
**Status:** Unlicense, about 570 stars, pushed Aug 2023. Checked: README (says the shader is not optimized enough for practical use and may run slow).
**Principle:** a watercolor look for Unity's URP and HDRP, inspired by a published technique.
**Mechanism (literature):** pigment-like effects: edge darkening where color changes, color bleeding with noise, paper texture; see Bousseau et al. and Kyprianidis for stylization filters.
