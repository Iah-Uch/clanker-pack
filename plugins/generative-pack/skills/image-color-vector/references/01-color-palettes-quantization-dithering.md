# Color spaces, scales, quantization and dithering

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published technique, not this project's code.

## Cross-cutting ideas

- **sRGB is not linear.** Decode first: c_lin = c/12.92 for c ≤ 0.04045, else ((c + 0.055)/1.055)^2.4. Do blending, blurring, averaging and lighting in linear light, encode at the end. Gradients computed in gamma space look muddy and too dark in the middle.
- **Perceptual spaces.** CIELAB and OKLab place colors so that equal distances look about equally different. Interpolating in them gives even gradients. LCH (and OKLCH) is the polar form: lightness, chroma, hue, which is the natural space for building palettes.
- **Color difference.** Euclidean distance in Lab is ΔE76; CIEDE2000 adds corrections for lightness, chroma and hue weighting and is the accurate choice for matching.
- **HSL is a convenience, not perceptual.** Equal HSL lightness is not equal brightness (yellow looks brighter than blue). HSLuv fixes that by taking the LCh_uv space and stretching chroma so that 100 percent saturation is the sRGB gamut boundary at each lightness and hue.
- **Scales from data.** Sequential, diverging and categorical schemes (ColorBrewer is the classic source); keep lightness monotonic for sequential data, keep diverging midpoints neutral, and check for color blindness.
- **Quantization** reduces a palette: median cut (split the box along the longest axis at the median), Wu's variance minimization, k-means or neural (NeuQuant) clustering in a perceptual space.
- **Dithering** hides quantization error: ordered (threshold matrix), error diffusion (Floyd-Steinberg pushes each pixel's error to its neighbors with weights 7/16, 3/16, 5/16, 1/16), blue noise.

## Entries

### Color.js — color-js/color.js
**Status:** MIT, about 2.3k stars, pushed Oct 2026. Checked: README.
**Idea:** by editors of the CSS Color specifications. A color is a list of coordinates plus a reference to its color space; operations are color-space agnostic; supports all CSS Color 4 spaces including OKLab and OKLCH, gamut mapping (reducing chroma until the color fits, rather than clipping), and interpolation in any space. The best reference for modern CSS color behavior.

### Chroma.js — gka/chroma.js
**Status:** BSD-style license (the LICENSE head names redistribution conditions; GitHub shows no classification; the file may also carry notices for bundled schemes, read it), about 10.6k stars, pushed Sep 2026. Checked: LICENSE head, README.
**Idea:** color conversion plus **scales**: `chroma.scale(['lightyellow','navy']).domain([1,100000],7,'log')` builds a color ramp over a data domain, with modes for interpolation space (rgb, lab, lch), classes by equidistant or quantile breaks, and logarithmic domains; also contrast ratio, color temperature and blending.

### d3-color — d3/d3-color
**Status:** ISC, about 430 stars, pushed Feb 2024. Checked: README.
**Idea:** color objects for RGB, HSL, CIELAB, CIELCH, Cubehelix with parse, convert, brighter and darker; paired with d3-interpolate to interpolate in any of them.

### d3-scale-chromatic — d3/d3-scale-chromatic
**Status:** ISC head (read; GitHub shows no classification, and the file also carries notices for the ColorBrewer and other bundled schemes; read it before copying data), about 820 stars, pushed Jun 2024. Checked: LICENSE head, README.
**Idea:** ready-made sequential, diverging and cyclical color schemes and interpolators (Viridis, Magma, Turbo, Cividis, Cubehelix, ColorBrewer) as functions from [0, 1] to a color, and categorical sets. Perceptually uniform ramps like Viridis are the safe default for quantitative data.

### HSLuv — hsluv/hsluv-javascript
**Status:** MIT, about 36 stars, pushed Jun 2026. Checked: README.
**Mechanism (README fields and literature):** RGB → CIE XYZ → CIE LUV → LCh_uv; the saturation S is chroma divided by the maximum in-gamut chroma at that lightness and hue, found by intersecting a ray with the six lines bounding the sRGB gamut in the (u, v) plane at fixed L. HPLuv keeps only the colors that are in gamut for all hues (a pastel subset). The API avoids heap allocation.
**Use it when:** generating palettes where equal lightness must look equal (themes, charts, accessibility).

### image-q — ibezkrovnyi/image-quantization
**Status:** no license detected on GitHub; the README says "MIT License", about 170 stars, pushed Oct 2023. Checked: README. Verify the license file in the repository before copying code.
**Idea:** color number reduction with alpha support using RGBQuant, NeuQuant and Xiaolin Wu's algorithms, with Euclidean, Manhattan and CIEDE2000 color distances and several dithering options. A compact comparison of palette strategies and distance formulas.

### dither — makew0rld/dither
**Status:** MPL-2.0 (file-level copyleft: changes to its files must be shared, linking is fine), about 470 stars, pushed Feb 2025. Checked: README.
**Idea:** a Go dithering library where correctness is a priority: it **linearizes** the image before dithering and compares colors with a perceptual metric, so error diffusion does not shift brightness; built-in ordered and error-diffusion algorithms, user-defined matrices, serpentine scanning.
**Mechanism (literature):** error diffusion kernels (Floyd-Steinberg, Atkinson, Stucki, Sierra) differ in how far and how strongly they spread the quantization error; serpentine scanning alternates direction per row to avoid directional artifacts.
**Use it when:** printing, e-ink, retro palettes, plotters.
