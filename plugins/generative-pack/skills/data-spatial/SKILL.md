---
name: data-spatial
description: Use when working with graphs and networks (force layout, shortest paths, route planning), spatial indexes and clustering (R-tree, KD-tree, quadtree, H3, hierarchical clustering), terrain meshes and contours, maps (projections, vector tiles, globes, wind and flow visualization), chart layouts (treemap, sankey, chord, word cloud), large-data rasterization, point clouds and 3D scans, or sun, moon, satellite and star positions. A catalog of techniques with mechanisms and formulas, to reason from, not a set of drop-in libraries.
---

# Data and spatial techniques

A catalog of ideas drawn from about 48 open-source projects: how graphs, maps, spatial data and astronomical positions are indexed, laid out, projected and drawn.

## Read this first

- **These are not drop-in solutions.** A project is an example of a technique. Abstract the idea and adapt it. Recommend a library only when it fits the user's stack, scale and license.
- **Do not assume a library does what its name suggests.** Each entry says what I checked; "literature" marks the published algorithm rather than the project's code. Check current docs before relying on a feature.
- **Licenses matter when you reuse code.** MIT, BSD, ISC, Apache: adapt with notices. GPL and AGPL (healpy, GPlates, Astrometry.net, prettymaps): take the technique and write your own code. "No license detected" (PathFinding.js): do not copy code. Map and tile data have their own licenses (OpenStreetMap is ODbL); the code license does not cover them.
- Facts were checked against each repository on 2026-10-15; projects change.

## Pick by goal

| You want | Read |
|---|---|
| Graph structures, force layout, shortest path, A*, contraction hierarchies, Kalman and particle filters | `references/01-graphs-networks-pathfinding.md` |
| Spatial indexes (R-tree, KD-tree, quadtree), point clustering, hexagonal grids, terrain mesh LOD, simplification, contours from scattered points | `references/02-spatial-indexes-and-geometry-structures.md` |
| Map libraries, projections, vector tiles, globes, wind maps, plate tectonics, equal-area sphere grids | `references/03-maps-projections-globes.md` |
| Treemaps, sankey, chord, word clouds, rasterizing millions of points, text shaping | `references/04-chart-layouts-and-large-data.md` |
| Point clouds, 3D scan registration, scientific visualization pipelines, sun and moon position, satellites, plate solving | `references/05-3d-data-sun-sky-and-orbits.md` |

## Ideas that recur

- Index once, query many times; prefer packed static indexes when data does not change.
- Precompute hierarchies (zoom clusters, octrees, tile pyramids, error trees) so runtime work is proportional to what is visible.
- Separate data model, layout and rendering.
- Aggregate before drawing when data is large.
- Use a library for coordinates, time and text; do not hand-roll geodesy or shaping.

## How to answer with this

1. Match the goal to a reference and read only that file.
2. Explain the technique in terms of the user's data and scale; mention a project as an example with its license.
3. If the user wants to build it, give the mechanism and a minimal recipe; do not paste code from a copyleft or unlicensed project.
