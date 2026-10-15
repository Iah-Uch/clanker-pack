# Vectorization, tracing, skeletons and differentiable vector graphics

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published technique, not this project's code.

## Cross-cutting ideas

- **Tracing = segment, outline, fit.** Reduce the image to regions (thresholding or color clustering), extract boundaries (marching squares or border following), then fit curves (piecewise Bezier) to the boundary points within a tolerance.
- **Curve fitting.** Fit one cubic Bezier to a run of points by least squares with a chord-length parameterization; if the maximum error exceeds the tolerance, split at the worst point and recurse (Schneider's algorithm). Corners are detected by turning angle and kept as breaks.
- **Skeletons.** The topological skeleton (medial axis) of a shape: the set of points with more than one nearest boundary point. Thinning peels pixels while preserving connectivity; tracing methods return polylines directly.
- **Centerline versus outline.** Outlines trace shape borders (filled output); centerlines trace the skeleton (strokes, for pen plotters and line art).
- **Stacking.** Color images are traced as layers: quantize to N colors, trace each, stack from background to foreground, or cluster hierarchically.
- **Differentiable rasterization.** If the rasterizer reports gradients with respect to path control points, colors and widths, you can optimize vector shapes with gradient descent to match a target image or a text prompt.

## Entries

### VTracer — visioncortex/vtracer
**Status:** MIT, about 7.3k stars, pushed Oct 2026. Checked: README.
**Principle:** raster to vector with a fast, linear pipeline that handles color.
**Mechanism (README):** unlike Potrace, which handles binary images and uses an optimal-polygon search, VTracer clusters colors hierarchically, stacks the clusters, and traces and simplifies each into splines, skipping the expensive optimization; this stays faithful at high resolution and works for photographs.
**Use it when:** logos, illustrations and photographs to compact SVG.

### ImageTracerJS — jankovicsandras/imagetracerjs
**Status:** Unlicense (public-domain dedication), about 1.5k stars, pushed Nov 2023. Checked: README.
**Idea:** raster tracing in JavaScript for the browser and Node: color quantization, layer-by-layer path extraction, and curve fitting, with presets (for example "posterized") and options for scale, blur and rounding. Small enough to read in one sitting.

### AutoTrace — autotrace/autotrace
**Status:** GPL-2.0, about 740 stars, pushed Oct 2026. Checked: README.
**Idea:** the classic bitmap tracer: **outline and centerline** tracing, color reduction, many input and output formats (SVG, EPS, PDF, DXF). Copyleft: use as a tool; take the ideas, not code, for a closed product.

### Skeleton Tracing — LingDong-/skeleton-tracing
**Status:** MIT, about 600 stars, pushed Jul 2022. Checked: README.
**Principle:** retrieve the topological skeleton of a binary image as a set of polylines, directly, rather than a thinned raster that you then must trace.
**Mechanism (README gives the goal; the method is from memory of the author's write-up, unverified here):** a divide-and-conquer trace that splits the image into smaller regions, finds skeleton fragments and joins them across the splits; the README says it avoids the post-processing that thinning plus contour tracing needs.
**Use it when:** centerlines for plotters, letterforms, road and vein extraction.

### Skan — jni/skan
**Status:** BSD-3-Clause, about 150 stars, pushed Jun 2026. Checked: README (points to the documentation).
**Idea:** analysis of skeleton images: turn a thinned image into a graph of junctions and branches and compute per-branch statistics (length, type, curvature); useful for fibers, vessels, roots, cracks. Pairs with a thinning step from scikit-image.

### diffvg — BachiLi/diffvg
**Status:** Apache-2.0, about 1.3k stars, pushed May 2025. Checked: README.
**Principle:** a differentiable rasterizer for 2D vector graphics.
**Mechanism (literature, Li et al. 2020):** the pixel coverage of a path is an integral that is differentiable almost everywhere; the gradient with respect to control points has an interior part and a boundary part, estimated by sampling points on the boundaries; gradients flow to path points, widths, colors and gradient stops. Example apps in the README: painterly rendering (fit N strokes to a photo, with a perceptual LPIPS loss), SVG refinement, and finite-difference comparison.
**Use it when:** optimize vector art to match an image, or use vectors as the output layer of a generative model.
