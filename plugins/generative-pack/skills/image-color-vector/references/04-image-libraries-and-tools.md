# Image, video and font libraries and tools

A catalog of ideas. The projects are tools and building blocks, not drop-in solutions for every task. "Checked" says what I read; "literature" marks the published technique, not this project's code. Licenses here matter most: several are LGPL, dual-licensed or GPL-optional.

## Cross-cutting ideas

- **Stream, do not load.** Libraries like libvips process images in small regions through a demand-driven pipeline, so memory use stays low for huge images; whole-image bitmaps do not scale.
- **Separable and recursive filters.** A Gaussian blur is separable, and an IIR (recursive) approximation runs in time independent of the radius.
- **Distance fields as texture.** Store, per texel, the signed distance to a shape's edge; a shader reconstructs a sharp edge from a low-resolution texture with smoothstep. Multi-channel versions keep corners sharp.
- **Perceptual diff.** Compare images in a perceptual color space (YIQ with a weighted difference) and ignore anti-aliased pixels to avoid false alarms in visual regression tests.
- **Optical flow.** Estimate per-pixel motion between frames: sparse (Lucas-Kanade tracks corners by solving a small least-squares system from image gradients) or dense (Farneback fits polynomial expansions to neighborhoods).
- **Inverse warping.** To transform an image, loop over output pixels, map each back to the source, and sample (nearest or bilinear); forward warping leaves holes.
- **Font rendering has stages:** shaping (HarfBuzz, see data-spatial), rasterization (FreeType), compositing.

## Entries

### ImageMagick — ImageMagick/ImageMagick
**Status:** the ImageMagick License (a custom, permissive license with an Apache-like character; the file's head states what it allows; GitHub shows no classification), about 17.7k stars, pushed Oct 2026. Checked: README, LICENSE head.
**Idea:** the command-line Swiss army knife: convert, resize, composite, color-manage, draw, montage, animate across many formats. Pipelines in shell scripts for batch work.
**Pitfalls:** security: feeding untrusted files to ImageMagick needs a restrictive policy (policy.xml); prefer libvips for services.

### libvips — libvips/libvips
**Status:** LGPL-2.1 or later (the README says so), about 11.7k stars, pushed Oct 2026. Checked: README.
**Idea:** a fast, low-memory image library: operations build a graph that executes in parallel over small tiles, streamed from source to destination, so a thumbnail of a huge image never loads it whole. Many language bindings. LGPL: linking is fine.

### libjpeg-turbo — libjpeg-turbo/libjpeg-turbo
**Status:** two compatible BSD-style licenses, the IJG License and the Modified BSD License (the license file says so), plus a zlib-style license for some parts; about 4.4k stars, pushed Oct 2026. Checked: LICENSE head.
**Idea:** a JPEG codec accelerated with SIMD. Mechanism (literature): 8×8 DCT, quantization, zigzag and Huffman coding; SIMD helps in the DCT, color conversion and upsampling.

### LibRaw — LibRaw/LibRaw
**Status:** dual-licensed: LGPL-2.1 or CDDL-1.0 (the README says you choose), about 1.6k stars, pushed Oct 2026. Checked: README.
**Idea:** read camera RAW files and run the first stages of a raw pipeline: demosaicing (interpolating the full color image from the Bayer mosaic), white balance, color matrix, gamma. Use it when you need unprocessed sensor data.

### FFmpeg — FFmpeg/FFmpeg
**Status:** mostly LGPL-2.1 or later, with optional GPL-2.0-or-later parts that apply only if built with `--enable-gpl` (the license file says so), about 65k stars, pushed Oct 2026. Checked: LICENSE head. Check the license of the exact build you ship, and patent obligations for some codecs.
**Idea:** the universal audio and video toolkit: demux, decode, filter graphs (scale, crop, overlay, drawtext, blend, loudness), encode, mux; a filter graph is a DAG you describe on the command line.
**Use it when:** any video or audio conversion, frame extraction, programmatic video assembly.

### OpenCV (optical flow and more) — opencv/opencv
**Status:** Apache-2.0, about 91k stars, pushed Oct 2026. Checked: metadata, README.
**Mechanism (literature):** Lucas-Kanade solves, for a patch, [sum Ix², sum IxIy; sum IxIy, sum Iy²]·(u, v) = −[sum IxIt; sum IyIt], assuming brightness constancy and small motion, in a pyramid for large motion; Farneback estimates dense flow with polynomial expansion. The library also covers features, calibration, stereo, tracking, DNN inference and morphology.
**Use it when:** motion estimation, tracking, classical vision, camera calibration.

### scikit-image — scikit-image/scikit-image
**Status:** BSD-3-Clause (the license file lists the files and per-file terms; GitHub shows no classification), about 6.6k stars, pushed Oct 2026. Checked: README, LICENSE head.
**Idea:** readable Python image processing on NumPy arrays: filters, morphology, segmentation (watershed, SLIC superpixels, random walker), feature detection, thinning and skeletonization, geometric transforms, restoration, and a gallery of worked examples. Good for prototyping and for checking an algorithm's intent.

### FreeType — freetype/freetype
**Status:** dual choice, the FreeType License (BSD-like with an advertising clause) or GPL-2.0 (the license file says you choose one), about 920 stars, pushed Oct 2026. Checked: LICENSE head.
**Idea:** the font rasterizer: parses outline fonts (TrueType, OpenType, Type 1), grid-fits (hinting) at small sizes, rasterizes glyph outlines with anti-aliased coverage (scanline area accumulation), and can render signed distance fields. Pair with HarfBuzz for shaping.

### glur — nodeca/glur
**Status:** MIT, about 106 stars, pushed May 2026. Checked: README.
**Idea:** a Gaussian blur in pure JavaScript via an IIR filter whose speed does not depend on the radius (a causal and an anti-causal recursive pass per axis, after Young and van Vliet or Deriche); works in place on RGBA bytes, plus a grayscale 16-bit variant useful for unsharp masking.

### ndarray-warp — scijs/ndarray-warp
**Status:** MIT, about 15 stars, pushed Sep 2014. Checked: README.
**Idea:** inverse image warping on ndarrays: you provide a function mapping output coordinates to input coordinates and the library samples with interpolation. A model for lens distortion, polar transforms and homographies.

### Pixelmatch — mapbox/pixelmatch
**Status:** ISC, about 7k stars, pushed Oct 2026. Checked: README.
**Idea:** a few hundred lines, no dependencies, raw typed arrays: compare two images pixel by pixel with a perceptual color distance (squared YIQ difference with a threshold) and **anti-aliased pixel detection** so edge differences from rendering do not count. For visual regression tests.

### TinySDF — mapbox/tiny-sdf
**Status:** BSD-2-Clause, about 670 stars, pushed Oct 2026. Checked: README.
**Idea:** generate glyph signed distance fields in the browser from the canvas text renderer using a two-pass Euclidean distance transform (the Felzenszwalb and Huttenlocher algorithm, linear time via lower envelope of parabolas), with buffer, radius and cutoff parameters. Used to render text at any scale in WebGL.

### msdfgen — Chlumsky/msdfgen
**Status:** MIT, about 5k stars, pushed Aug 2026. Checked: README.
**Principle:** multi-channel signed distance fields.
**Mechanism (README and literature):** a single-channel SDF rounds off sharp corners at low resolution; assign each edge segment of the shape one of three color channels so that at a corner two channels disagree, then reconstruct with median(r, g, b) in the shader; the corner survives. Also generates perpendicular distance fields and "MTSDF" with a true SDF in the alpha channel.
**Use it when:** crisp text and icons from small textures, outlines and glows in shaders.

### NanoVG — memononen/nanovg
**Status:** Zlib, about 5.7k stars, pushed Feb 2026. Checked: README.
**Idea:** antialiased 2D vector rendering on OpenGL with an API modeled on HTML5 canvas (paths, fills, strokes, gradients, text); antialiasing comes from geometry (extra fringe triangles with alpha ramps) rather than multisampling; tiny and easy to embed in UI and visualization code.
