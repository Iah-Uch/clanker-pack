---
name: image-color-vector
description: Use when processing or stylizing images, color and vectors: color spaces and gradients (OKLab, LCH, HSLuv), palettes and color scales, quantization and dithering, raster-to-vector tracing, skeletons and centerlines, differentiable vector graphics, seam carving, geometric-primitive and triangulated art, stippling, brush engines, optical flow, image and video tools (ImageMagick, libvips, FFmpeg, OpenCV, scikit-image), RAW and JPEG decoding, font rasterization, signed distance field text, perceptual image diff. A catalog of techniques with mechanisms and formulas, to reason from, not a set of drop-in libraries.
---

# Image, color and vector techniques

A catalog of ideas drawn from about 34 open-source projects: how color is modeled, how images become vectors or art, and which libraries do the heavy lifting.

## Read this first

- **These are not drop-in solutions.** A project is an example of a technique. Abstract the idea and adapt it. Recommend a tool only when it fits the user's stack, scale and license.
- **Do not assume a library does what its name suggests.** Each entry says what I checked; "literature" marks the published technique rather than the project's code. Check current docs before relying on a feature.
- **Licenses matter, especially here.** MIT, BSD, ISC, Apache, zlib, Unlicense: adapt with notices. GPL (AutoTrace, Swingline), LGPL (libvips, StippleGen, LibRaw, FFmpeg's default): link or take the technique, per the entry. MPL-2.0 (dither) is file-level. FreeType and LibRaw are dual-licensed; FFmpeg becomes GPL with `--enable-gpl`. Where GitHub shows no license, I read the file or the README; the entry says which.
- Facts were checked against each repository on 2026-10-15; projects change.

## Pick by goal

| You want | Read |
|---|---|
| Color conversion, perceptual gradients, palettes and scales, quantization, dithering | `references/01-color-palettes-quantization-dithering.md` |
| Raster to SVG, centerlines, skeleton analysis, optimizing vector paths with gradients | `references/02-vectorization-tracing-skeletons.md` |
| Seam carving, shape-approximated and triangulated images, stippling and TSP art, brush engines | `references/03-image-art-algorithms.md` |
| Image and video libraries, RAW and JPEG, fonts and distance-field text, optical flow, visual diffs | `references/04-image-libraries-and-tools.md` |

## Ideas that recur

- Convert to linear or perceptual space before blending, averaging or interpolating.
- Approximate with few marks by hill-climbing the error, one mark at a time.
- Dynamic programming finds optimal paths (seams); Lloyd relaxation spaces points by density.
- Trace in stages: segment, outline, fit curves within a tolerance.
- Stream and tile large images; avoid whole-image bitmaps.
- Store distance, not coverage, when you need crisp edges at any scale.

## How to answer with this

1. Match the goal to a reference and read only that file.
2. Explain the technique and the formula in terms of the user's task; mention a project as an example with its license.
3. Check license and security (untrusted input to ImageMagick or FFmpeg) before recommending a tool for a service.
4. Do not paste code from copyleft or unlicensed projects.
