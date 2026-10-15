# Image art algorithms: seam carving, primitives, triangulation, stippling, brushes

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published technique, not this project's code.

## Cross-cutting ideas

- **Approximate an image with few marks.** Choose a mark type (triangle, ellipse, dot, stroke), then search for the placement and color that most reduce the error between the target and the canvas. Hill climbing, genetic algorithms and gradient descent are the usual optimizers.
- **Error metric.** Mean squared error per pixel in a linear or perceptual space; compute incrementally for the region a mark covers.
- **Importance-driven sampling.** Place more points where the image has detail (edges) or darkness (stippling), then connect or Delaunay-triangulate them.
- **Dynamic programming for seams.** Minimum-energy paths across an image are found in O(width × height).

## Entries

### caire — esimov/caire
**Status:** MIT, about 10.7k stars, pushed May 2025. Checked: README.
**Principle:** content-aware resizing by **seam carving** (Avidan and Shamir 2007).
**Mechanism (README steps):** compute an energy map by edge detection; find the vertical seam of pixels with the lowest cumulative energy by dynamic programming, M(i, j) = e(i, j) + min(M(i−1, j−1), M(i−1, j), M(i−1, j+1)), then backtrack from the minimum in the last row; remove the seam; repeat. Growing the image duplicates seams. A mask can protect regions.
**Use it when:** retargeting images to new aspect ratios; seams also work as a glitch-art effect.
**Pitfalls:** structured content (faces, straight lines) breaks without protection masks.

### Primitive — fogleman/primitive
**Status:** MIT, about 13.5k stars, pushed Jul 2024. Checked: README.
**Principle (README):** given a target image, find the single most optimal shape to reduce the error between the target and the drawn image; repeat, adding one shape at a time. About 50 to 200 shapes give a recognizable, abstract result.
**Mechanism:** each step generates random candidate shapes, hill-climbs their parameters (move, resize, rotate a vertex) to lower the error, picks the best color analytically (the average of the target pixels the shape covers, adjusted for alpha), draws it and continues. Output is SVG-friendly (triangles, rectangles, ellipses, rotated shapes, Béziers).
**Use it when:** low-poly and geometric portraits, vector approximations of photos.

### Triangula — rh12503/triangula
**Status:** MIT, about 3.9k stars, pushed Mar 2026. Checked: README (and its linked wiki for the algorithm).
**Principle:** a modified genetic algorithm that evolves point sets whose Delaunay triangulation, filled with each triangle's average color, matches the image.
**Mechanism (README):** a population of point sets mutates and recombines; fitness is the pixel error of the rendered triangulation; the README advises images smaller than 3000 px and fewer than 3000 points, reaching an optimum in minutes.
**Use it when:** triangulated or polygonal art with good fidelity per point.

### triangulate-image — snorpey/triangulate-image
**Status:** MIT, about 136 stars, pushed Jan 2023. Checked: README.
**Idea (literature; the README documents options, not the algorithm):** the fast version of the same art: detect edges (Sobel) and sample points where the gradient is strong plus some random points, run a Delaunay triangulation, fill each triangle with the color at its centroid. Configurable blur, edge threshold, point count and output format (canvas, SVG, data URL, in the browser and Node).

### StippleGen — evil-mad/stipplegen
**Status:** LGPL-2.1, about 485 stars, pushed Apr 2022. Checked: README.
**Principle:** make stipple drawings and "TSP art" (a single continuous line through all stipple points, from an approximate traveling-salesman tour), written in Processing for pen plotters.
**Mechanism (literature, Secord 2002):** weighted centroidal Voronoi stippling (Lloyd's relaxation): start with random points, compute the Voronoi diagram, move each point to the density-weighted centroid of its cell, where density is image darkness; repeat until stable. Points space out evenly with density following tone.

### Swingline — mkeeter/Swingline
**Status:** GPL-2.0, about 67 stars, pushed Mar 2018. Checked: README.
**Principle:** weighted Voronoi stippling entirely on the GPU: compute the Voronoi diagram by rendering a cone per site with depth testing (each pixel takes the nearest site's color), then centroids are accumulated by reductions over the image. Copyleft: reuse the idea.

### libmypaint — mypaint/libmypaint
**Status:** an ISC-style permission notice in the LICENSE head (read; GitHub shows no classification), about 390 stars, pushed Apr 2026. Checked: LICENSE head, README.
**Idea:** the brush engine of MyPaint: a brush is a set of dynamics, each a curve from inputs (pressure, speed, direction, random, tilt) to settings (opacity, radius, hardness, smudge, color change), evaluated for dabs placed along the stroke path; strokes are drawn as many soft dabs, so any tablet or custom input can drive a natural medium. Brushes are JSON files.
**Use it when:** painting software, procedural strokes with tablet-like dynamics.
