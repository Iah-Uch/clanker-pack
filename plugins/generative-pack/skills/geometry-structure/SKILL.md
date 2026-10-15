---
name: geometry-structure
description: Use when a task involves curves, splines, polygons, boolean clipping, triangulation, convex or concave hulls, Voronoi or Delaunay, packing, tiling, space-filling curves, meshes (smoothing, simplification, UV unwrapping, deformation), implicit surfaces, signed distance fields, marching cubes or squares, CSG, CAD, vector graphics, plotter output or fonts. A catalog of techniques with the math and mechanism of each, to reason from, not a set of drop-in libraries.
---

# Geometry and structure

A catalog of ideas drawn from about 115 open-source projects. Each entry explains the principle, the mechanism (formulas or steps), when to use it, and how to build it yourself.

## Read this first

- **These are not drop-in solutions.** A project is an example of a technique. The value is the idea: abstract it, adapt it to the task, and combine it with others. Recommend a project only when it actually fits the user's stack, license and constraints.
- **Do not assume a library does what its name suggests.** Each entry says what I checked. "Literature" means the mechanism comes from the published algorithm, not from that project's code. Check current docs before relying on a project feature.
- **Licenses matter when you reuse code.** MIT, BSD, ISC, Apache and similar: adapt with the notices kept. GPL, AGPL, LGPL: take the technique and write your own code. Several large libraries are mixed or per-package licensed (libigl, CGAL, FontForge, libfive); the entry says so. If an entry says "no license detected", do not copy code.
- A code license does not cover bundled fonts, models or data.
- Facts were checked against each repository on 2026-10-15; projects change.

## Pick by goal

| You want | Read |
|---|---|
| Smooth curves, Bezier or B-spline math, curve fitting, thick strokes, flow lines | `references/01-curves-and-splines.md` |
| Polygon union and difference, offsetting, triangulation, hulls, Delaunay, Voronoi, exact predicates | `references/02-polygons-hulls-triangulation.md` |
| Packing circles or rectangles, nesting, blue-noise sampling, space-filling curves, tilings, box overlap | `references/03-packing-tiling-sampling-indexing.md` |
| Mesh smoothing, deformation, simplification, remeshing, UVs, BVH, voxels, reconstruction from photos | `references/04-meshes-and-surfaces.md` |
| Shapes as functions, SDFs, marching cubes or squares, contour lines, CSG, ray marching | `references/05-implicit-surfaces-contours-sdf.md` |
| CAD kernels, vector graphics APIs, fonts, plotters, string art | `references/06-cad-vector-graphics-fonts-fabrication.md` |

## Ideas that recur across the references

- Exactness comes from two predicates (orientation, in-circle). Without them, geometry code fails on near-degenerate input.
- Sweep a line and only neighbors interact: boolean clipping, triangulation and intersection tests.
- Lift to a higher dimension to simplify (Delaunay is a convex hull in one dimension up).
- Many mesh operations are sparse linear solves with the cotangent Laplacian.
- Represent a shape as a function (an SDF) to make booleans trivial (min, max) and rendering a loop.
- Accelerate with a hierarchy or grid; order points along a Hilbert or Morton curve for locality.

## How to answer with this

1. Match the goal to a reference and read only that file.
2. Explain the technique first, in terms of the user's problem. Mention a project as an example or a possible tool, with its license.
3. If the user wants to build it, give the mechanism and a minimal recipe. Do not paste code from a copyleft project.
4. When the task mixes areas (for example "texture a procedurally generated mesh"), combine entries from several references.
