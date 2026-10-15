# Packing, tiling, sampling and spatial indexing

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Packing is search with a collision test.** Either place greedily and never move (fast, approximate), or start overlapped and relax (repulsion), or search over order and rotation with a no-fit region (nesting).
- **Blue noise.** Well-spaced random points (no two closer than r) look natural; they come from rejection against a grid, not from plain random numbers.
- **Space-filling curves** map n-dimensional position to a 1D index while keeping neighbors close, which gives cache-friendly ordering and cheap range queries.
- **Spatial indexes** (grids, boxes, trees) turn "find overlaps" from O(n²) into near O(n log n).

## Packing

### circlify — elmotec/circlify
**Status:** MIT, pushed Sep 2025. Checked: README, circlify.py docstring.
**Principle:** circle packing where each circle's area encodes a value (like a treemap).
**Mechanism:** place circles with a front-chain heuristic (Huang et al. 2006, "A1.0"), then enclose all of them in one circle using the Matousek-Sharir-Welzl smallest-enclosing-circle algorithm, the same enclosure used by D3's pack layout. Input is positive values sorted largest to smallest.
**Use it when:** bubble layouts and nested hierarchy views.

### packcircles — mbedward/packcircles
**Status:** MIT-style license file (year and holder only; GitHub shows no classification), pushed 2024. Checked: README, src/packcircles.cpp.
**Principle:** relax overlapping circles by pair repulsion.
**Mechanism:** start with circles anywhere in a rectangle; each iteration, every overlapping pair moves apart along the line between centers, by an amount weighted by the other circle's radius so big circles move less; repeat until no overlap or a limit is hit (the code has a `do_repulsion` step and an optional wrap-around). Adapted from a Processing example.
**Use it when:** a quick non-overlapping layout where exact tightness is not needed.

### pack-spheres — mattdesl/pack-spheres
**Status:** MIT, pushed 2023. Checked: README, index.js options.
**Principle:** random sequential packing: propose a point, grow a circle or sphere as large as allowed, keep it.
**Mechanism (inferred from options; standard method):** sample a random position, set the radius to the distance to the nearest existing circle minus padding, clamp to the maximum, accept if above the minimum, repeat for `packAttempts` tries per round until `maxCount`. Works in 2D or 3D; the `outside` test restricts the region.
**Use it when:** organic filled patterns, particle seeds.

### potpack — mapbox/potpack
**Status:** ISC, pushed Jun 2026. Checked: README, index.js doc comment.
**Principle:** pack rectangles into a near-square container with high fill.
**Mechanism:** sort boxes (by height), then place each into the first free space that fits, splitting the leftover space, and grow the container as needed. It is a variation of the Blackpawn, rectpack2D and bin-pack approaches. Returns the container size and a fill ratio, and writes x and y into each box.
**Use it when:** sprite sheets, texture atlases. Static: no insertion after layout.

### SVGnest — Jack000/SVGnest
**Status:** MIT, pushed 2024. Checked: README, svgnest.js.
**Principle:** nesting: fit irregular shapes into as little material as possible.
**Mechanism:** the code keeps a no-fit-polygon cache and integer-scaled geometry for robust Clipper operations, curve tolerance, spacing and allowed rotations. A no-fit polygon is the set of positions where one shape touches another without overlap, so a part can be slid along it. A search over part order and rotation (genetic search in the README's referenced literature) picks the best sequence.
**Use it when:** laser cutting and CNC layouts.

## Sampling and indexing

### poisson-disk-sampling — kchapelier/poisson-disk-sampling
**Status:** MIT, pushed 2022. Checked: README, src/poisson-disk-sampling.js.
**Principle:** random points with a guaranteed minimum spacing.
**Mechanism (Bridson, literature):** a background grid whose cell size is minDistance divided by the square root of the dimension, so each cell holds at most one point; keep an active list; for a random active point try `tries` candidates in the shell between min and max distance; accept one if no existing point is within min distance, else retire the point. Separate fixed-density and variable-density implementations exist; variable density takes a function giving local spacing.
**Use it when:** stippling, foliage placement, sampling in any dimension.

### hilbertcurve — galtay/hilbertcurve
**Status:** MIT, pushed 2024. Checked: README, hilbertcurve.py docstring.
**Principle:** a 1D index along the Hilbert curve for each cell of an n-dimensional grid.
**Mechanism:** an n-dimensional hypercube of side 2^p holds 2^(n·p) unit cells; the curve visits each exactly once and adjacent indices are adjacent cells. Conversion is done with bit operations per level (Gray code plus rotation and reflection) (literature).
**Use it when:** locality-preserving ordering, 1D indexes for 2D data.

### libmorton — Forceflow/libmorton
**Status:** MIT, pushed Jun 2026. Checked: README, include/libmorton/morton3D_LUTs.h.
**Principle:** Morton (Z-order) code: interleave the bits of the coordinates.
**Mechanism:** for 3D, bit i of x goes to bit 3i, y to 3i+1, z to 3i+2. Implemented with lookup tables (the header holds a 256-entry table) or by hardware bit-deposit instructions. Z-order is less locality-preserving than Hilbert but far cheaper to compute.
**Use it when:** octree and BVH construction, grid sorting.

### box-intersect — mikolalysenko/box-intersect
**Status:** MIT, pushed Mar 2026. Checked: README, lib/intersect.js.
**Principle:** find all overlapping pairs among axis-aligned boxes in d dimensions.
**Mechanism:** based on Zomorodian and Edelsbrunner (2000): recursively partition on the median and sweep, falling back to brute force below a size cutoff (128 in the code). Time is O((n+m) log^d (n+m)) for two sets of n and m boxes.
**Use it when:** broad-phase collision, polygon clipping and CSG candidate search.

### greedy-mesher — mikolalysenko/greedy-mesher
**Status:** MIT, pushed 2016. Checked: README, greedy.js.
**Principle:** merge adjacent same-valued grid cells into the fewest large rectangles.
**Mechanism (literature):** scan the array; at an unvisited cell extend along one axis while values match, then extend the resulting strip along the other axis while whole rows match; emit the box and mark covered. The README example turns a 4x4 label array into two rectangles. It compiles a specialized mesher from your options (order, merge test, append callback).
**Use it when:** voxel face meshing, run-length style compression of grids.

### d3-hexbin — d3/d3-hexbin
**Status:** BSD-3-Clause, pushed 2023. Checked: README, src/hexbin.js (setup).
**Principle:** aggregate points into hexagonal cells.
**Mechanism (literature):** scale points into a skewed grid where hex row spacing is 1.5r and column spacing is r·sqrt(3), round to the nearest candidate cell, and compare the distance to the neighboring cell's center to resolve boundary cases. Hexagons have uniform neighbor distance, which reduces directional bias compared with squares.
**Use it when:** density maps from large scatter data.

## Tilings and constraints

### TactileJS — isohedral/tactile-js
**Status:** BSD-3-Clause, pushed 2024. Checked: README, lib/tactile.js.
**Principle:** isohedral tilings: every tile is an identical copy of one shape, and the symmetry group acts transitively on tiles.
**Mechanism:** a tiling type fixes how many edges the tile has, which edge classes it uses (the code names four: free J, mirror U, half-turn S, straight I) and the affine transforms (2x3 matrices) that carry the base tile to its neighbors. Changing a few parameters or edge curves deforms the whole tiling consistently (Grunbaum and Shephard; Kaplan's tiling theory). The code defines 81 tiling types.
**Use it when:** Escher-style tessellations and pattern generators.

### ORIPA — oripa/oripa
**Status:** GPL-3.0, pushed Sep 2026. Checked: README only; no algorithm code read.
**Principle:** origami crease pattern design with a folded-shape computation.
**Mechanism (literature, not verified in the code):** flat-foldability rules at a vertex: Kawasaki's theorem (alternate angles sum to 180 degrees) and Maekawa's theorem (mountain and valley folds differ by two). The folded shape needs a layer-ordering solution among overlapping faces.
**Use it when:** crease pattern analysis. Copyleft: take the theory, not the code.

### Penrose — penrose/penrose
**Status:** MIT, 8k★, pushed Oct 2026. Checked: README, example file names.
**Principle:** separate what exists from how it looks, so a diagram follows from notation.
**Mechanism:** three plain-text layers: a Domain (types and relations), a Substance (the objects in this diagram), and a Style (visual rules). The layout is solved by numerical optimization of constraints and objectives (literature on the Penrose system).
**Use it when:** mathematical diagrams from notation; a model for any declarative layout system.
