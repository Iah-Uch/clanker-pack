# Implicit surfaces, contours, distance fields and CSG

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **A shape as a function.** An implicit surface is the set where f(x, y, z) = 0, with f < 0 inside. A signed distance function (SDF) is the special case where |f| is the distance to the surface. Union is min(a, b), intersection is max(a, b), difference is max(a, −b).
- **Extract, don't render, when you need geometry.** Sample f on a grid, then run marching cubes (3D) or marching squares (2D) to get a mesh or polylines. Or never extract: ray-march f directly in a shader.
- **Smooth blends.** Replace min with a smooth minimum so shapes merge like clay instead of meeting at a crease.
- **Prune with intervals.** If you can bound f over a region, whole regions can be skipped as clearly inside or outside.

## Primitives and operators

### glsl-sdf-primitives — marklundin/glsl-sdf-primitives
**Status:** MIT, pushed 2020. Checked: README.
**Principle:** closed-form distance functions for basic shapes, from Inigo Quilez's reference pages.
**Mechanism:** each primitive returns the signed distance from a point p to the shape (a sphere is length(p) − r; a box uses q = abs(p) − half-size and combines length(max(q, 0)) with the largest component of q capped at 0). A ray marcher steps along the ray by the returned distance, which is always a safe step.
**Use it when:** shader scenes, SDF modeling.
**Build it yourself:** sphere tracing: t += f(origin + t·dir) until f is tiny or t is too large.

### glsl-smooth-min — glslify/glsl-smooth-min
**Status:** MIT (LICENSE read; GitHub shows no classification), pushed 2015. Checked: README, LICENSE head.
**Mechanism:** `smin(a, b, k)` blends two distances smoothly instead of the hard min. The polynomial form (literature, Inigo Quilez) uses h = max(k − |a − b|, 0)/k and returns min(a, b) − h·h·k/4, so the blend zone has width k.
**Use it when:** organic unions in raymarched scenes.

### glsl-ray-sphere — wellcaffeinated/glsl-ray-sphere
**Status:** MIT, pushed 2024. Checked: README.
**Principle:** ray-sphere intersection that stays accurate for tiny spheres and glancing rays.
**Mechanism (the cited paper, Haines, Gunther, Akenine-Moller):** the textbook quadratic loses precision from cancellation. The improved method works from the closest point of the ray's line to the sphere center and computes the discriminant from a more stable quantity.
**Use it when:** ray tracing at extreme scales.

### sdf — fogleman/sdf
**Status:** MIT, 2k★, pushed Sep 2026. Checked: README, sdf/core.py.
**Principle:** model in Python with SDF operators, then mesh.
**Mechanism:** shapes are functions; `&`, `|` and `-` overload to intersection, union and difference. To mesh, sample the SDF on a grid in batches (it uses threads and a large sample budget), run marching cubes at level 0 (via scikit-image), and write STL.
**Use it when:** programmatic CAD-like models for 3D printing.

## Extracting surfaces and contours

### PyMCubes — pmneila/PyMCubes
**Status:** BSD-3-Clause, pushed 2024. Checked: README, mcubes/src/marchingcubes.cpp.
**Principle:** marching cubes (Lorensen and Cline 1987).
**Mechanism:** for each cube of 8 grid samples, classify each corner as inside or outside (256 combinations), look up which of the 12 edges are crossed (the source holds the edge table), place a vertex on each crossed edge by linear interpolation t = (iso − f1)/(f2 − f1), and join them with the triangle table.
**Use it when:** volumes or functions to meshes in Python.

### isosurface — mikolalysenko/isosurface
**Status:** MIT, pushed 2014. Checked: README, lib/marchingcubes.js.
**Mechanism:** several polygonizers on one potential function: marching cubes (with its edge table), surface nets, and marching tetrahedra (documented in the author's blog posts). `surfaceNets(dims, potential, bounds)` returns a mesh.

### surface-nets — mikolalysenko/surface-nets
**Status:** MIT, pushed 2021. Checked: README, surfacenets.js requires.
**Principle:** one vertex per cell that the surface crosses, instead of one per crossed edge.
**Mechanism (literature, Gibson):** for each grid cell with a sign change, put a vertex at the average of its edge crossing points; connect the vertices of neighboring cells that share a crossing edge. Results are smoother and use fewer triangles than marching cubes, at the cost of rounding sharp features. This version works in any dimension.
**Use it when:** smooth voxel terrain.

### d3-contour — d3/d3-contour
**Status:** ISC, pushed Nov 2024. Checked: README, src/contours.js.
**Principle:** marching squares: classify each cell's four corners against a threshold and draw the edge segments crossing it.
**Mechanism:** a 16-entry case table gives the segment coordinates for each pattern (the source holds it); segments are stitched into closed rings and output as polygons, with thresholds chosen by Sturges' rule unless given.
**Use it when:** contour maps from gridded data.

### MarchingSquaresJS — RaumZeit/MarchingSquares.js
**Status:** AGPL-3.0 (license text read; GitHub shows no classification). Pushed 2020. Checked: README, src/isobands.js.
**Mechanism:** iso lines and iso bands (the region between two thresholds), accelerated by a quad-tree so only cells that can contribute are visited, with case tables that emit polygon paths.
**Use it when:** you need bands, not just lines. Copyleft: take the idea only.

### contourmap — fogleman/contourmap
**Status:** MIT, pushed 2022. Checked: README, contourmap.go.
**Idea:** isolines for any 2D grid of floats or any image, in Go; a small clean implementation of the same marching-squares idea.

### libfive — libfive/libfive
**Status:** library and stdlib MPL-2.0; the Guile bindings and Studio GUI are GPL-2.0-or-later (README read; GitHub shows none). Pushed Oct 2026. Checked: README, stdlib source.
**Principle:** functional representation (f-rep) solid modeling.
**Mechanism:** a model is an expression tree whose leaves are the coordinates X, Y, Z and constants (the code builds `Tree::X()`). The mesher produces watertight, manifold, hierarchical, feature-preserving meshes (the README highlights this), through adaptive subdivision with dual contouring, which uses the surface normals to keep sharp edges (literature).
**Use it when:** CAD-like parametric models with exact edges.

### Fidget — mkeeter/fidget
**Status:** MPL-2.0, pushed Oct 2026. Checked: README, a wgpu source file.
**Principle:** evaluate huge implicit surfaces fast by simplifying the math as you zoom into a region.
**Mechanism:** the expression graph is deduplicated and flattened into a straight-line "tape" of operations. Evaluating the tape with interval arithmetic over a box says which branches of min and max can matter there; the tape is simplified for that box and passed down as the region is subdivided. A JIT compiles tapes to native code (aarch64 and x86_64) for point, interval and SIMD evaluation (literature: Keeter's massively parallel rendering of closed-form implicit surfaces).
**Use it when:** interactive modeling of complex implicit shapes.
**Build it yourself:** interval arithmetic: min([a,b],[c,d]) = [min(a,c), min(b,d)]; if one interval is entirely below the other, drop the other branch.

## Solids and rendering

### csg.js — evanw/csg.js
**Status:** MIT, pushed 2019. Checked: README, csg.js header.
**Principle:** boolean operations on polygon meshes using binary space partition trees.
**Mechanism:** each solid holds a BSP tree of its polygons. To combine, clip one solid's polygons against the other's tree (keeping the parts inside or outside), invert, and merge the trees; union, subtract and intersect are short sequences of clip, invert and build calls on the two trees (literature, from the library's source).
**Use it when:** small meshes in the browser. Not robust for degenerate input.

### ln — fogleman/ln
**Status:** MIT, 3.5k★, pushed 2019. Checked: README, ln/mesh.go.
**Principle:** render a 3D scene as 2D vector paths, for plotters, with hidden lines removed.
**Mechanism:** every shape produces its edges and hatching as 3D paths; each path is split into short pieces and tested for visibility by casting a ray to the camera against the scene (accelerated by a tree built over the shapes); only visible pieces are projected to 2D. Supports spheres, cubes, cylinders, meshes, 3D functions, CSG and vector "textures" such as hatch lines.
**Use it when:** pen plotter art, technical line drawings.

### glsl-solid-wireframe — rreusser/glsl-solid-wireframe
**Status:** no license detected (do not copy code), pushed 2017. Checked: README, cartesian/scaled.glsl.
**Principle:** draw a wireframe in the fragment shader with no extra geometry.
**Mechanism:** every fragment carries barycentric coordinates; its distance to the nearest edge is the smallest coordinate, and a smoothstep turns that into a line. Screen-space derivatives (`fwidth`) keep the line width constant in pixels. The same trick draws grid lines at integer values of any varying quantity.
**Use it when:** debug views and stylized meshes.

### Mandelbulber — buddhi1980/mandelbulber2
**Status:** GPL-3.0, pushed Oct 2026. Checked: README only; no algorithm code read.
**Principle:** render 3D fractals (Mandelbulb, Mandelbox, IFS and hybrids) by ray marching a distance estimate.
**Mechanism (literature):** a fractal has no exact SDF, so use a distance estimator derived from the escape iteration, for the Mandelbulb roughly 0.5·|z|·ln|z| / |dz| where dz tracks the derivative. Ray march with that bound. The software uses OpenCL and multiple GPUs. Copyleft: take the idea, not the code.
