# Polygons, boolean ops, triangulation, hulls, Voronoi

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. Use the principle and mechanism to build what the task needs. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Predicates first.** Almost every algorithm here is a sequence of two tests: which side of a line is a point on (orient2d), and is a point inside a circle through three points (incircle). Wrong answers from rounding make algorithms loop or crash. Robustness means making those two tests exact.
- **Sweep line.** Sort events left to right, keep an ordered set of active segments, and only neighbors can intersect. Boolean clipping and some triangulations use it.
- **Lifting.** Delaunay in d dimensions equals a convex hull in d+1 by mapping p to (p, |p|²).
- **Dual structures.** Voronoi is the dual of Delaunay; skeletons and medial axes are dual to offsets.

## Robust predicates

### robust-predicates — mourner/robust-predicates
**Status:** Unlicense, pushed Sep 2026. Checked: README, src/incircle.js.
**Principle:** exact geometric tests using floating point only when safe.
**Mechanism (Shewchuk):** compute orient2d = (ax−cx)(by−cy) − (ay−cy)(bx−cx) in floating point, bound the rounding error (the code defines error-bound constants for each stage), and if the result's magnitude exceeds the bound its sign is certain. Otherwise recompute with adaptive-precision expansion arithmetic until certain. Functions: orient2d, orient3d, incircle, insphere. In this library the y axis points down, so signs are mirrored relative to Shewchuk's originals.
**Use it when:** any geometry code that decides on a sign (triangulation, hull, point-in-polygon).
**Pitfalls:** flipped y convention; do not mix with a library using the other convention.

### robust-point-in-polygon — mikolalysenko/robust-point-in-polygon
**Status:** MIT, pushed 2023. Checked: README, robust-pnp.js.
**Principle:** crossing-number test with exact orientation.
**Mechanism:** cast a ray, count edges whose y-range straddles the point, and use an exact orient test to decide the side. A zero orientation means the point lies on the boundary. Returns −1 inside, 0 on boundary, 1 outside.
**Use it when:** classification must be exact, including boundary hits.

## Boolean operations and offsetting

### Clipper2 — AngusJohnson/Clipper2
**Status:** BSL-1.0, 2.5k★, pushed Apr 2026. Checked: README, Clipper.cs header.
**Principle:** union, intersection, difference and XOR of arbitrary polygons, plus offsetting.
**Mechanism (literature):** Vatti's sweep-line clipping on integer coordinates, so intersections are exact and robust; offsetting moves each edge outward and joins with round, square or miter corners, then unions the result to remove self-overlap.
**Use it when:** CAD, CAM, nesting, or any polygon boolean at scale.
**Pitfalls:** the README warns its triangulation code is buggy; do not rely on it.

### Martinez polygon clipping — w8r/martinez
**Status:** MIT, pushed Oct 2026. Checked: README, src/connect_edges.ts.
**Principle:** sweep-line boolean ops on polygons with holes, multipolygons, self-intersection and overlapping edges.
**Mechanism:** build events for every edge endpoint, sort left to right, sweep while subdividing segments at intersections, mark each edge as inside or outside the other polygon, keep those the operation selects, then connect the kept edges into contours (the `connect_edges` step orders the result events).
**Use it when:** GeoJSON-scale polygon booleans in JavaScript.

### PolyBool — velipso/polybool
**Status:** 0BSD, pushed May 2026. Checked: README, src/polybool.ts.
**Principle:** the same pipeline as Martinez, split into reusable stages.
**Mechanism:** the module names show the stages: Intersecter (split segments at crossings), SegmentSelector (choose by operation), SegmentChainer (join into regions). Epsilon is configurable. Outer paths come out counter-clockwise and holes clockwise. Bezier cubics are supported experimentally.
**Use it when:** you want to chain many operations efficiently and understand each stage.

### polygon-offset — w8r/polygon-offset
**Status:** MIT, pushed 2023. Checked: README, src/offset.js.
**Principle:** margin and padding by offsetting each edge and repairing with a boolean union.
**Mechanism:** offset edges by distance, add arc joins (a configurable number of arc segments), then union with Martinez to clean overlaps. Negative distance gives padding.
**Use it when:** a small offset for concave shapes without pulling in a large library.

### Cavalier Contours — jbuckmccready/cavalier_contours
**Status:** Apache-2.0, pushed Aug 2026. Checked: README, FFI source.
**Principle:** offsetting and booleans on polylines made of lines and true circular arcs.
**Mechanism:** arcs stay arcs (bulge-encoded). Offset each segment, find intersections among offset segments using an AABB spatial index, slice at intersections, drop slices closer than the offset distance to the original, and stitch what remains (author's approach, literature). Also winding-number tests, containment, area and boolean ops.
**Use it when:** CAM toolpaths or any shape where arcs must stay exact.

## Triangulation and decomposition

### Earcut — mapbox/earcut
**Status:** ISC, 2.6k★, pushed Oct 2026. Checked: README, src/earcut.js.
**Principle:** triangulate a polygon by cutting off ears.
**Mechanism:** an ear is a convex vertex whose triangle contains no other vertex. Repeatedly clip ears from a linked ring. Speed comes from z-order (Morton) curve hashing so containment checks only look at nearby points. Holes are bridged to the outer ring. It favors speed over triangle quality, handles degenerate input, and can refine to Delaunay.
**Use it when:** filling polygons for WebGL or maps.
**Pitfalls:** thin triangles; refine if quality matters.

### libtess2 — memononen/libtess2
**Status:** SGI Free Software License B (GitHub shows no classification), pushed 2025. Checked: README, Source/mesh.c.
**Principle:** general tessellation with winding rules, from the GLU reference tessellator.
**Mechanism:** a half-edge mesh (edges created in pairs) swept left to right, with winding-rule selection (even-odd, non-zero, positive, negative) deciding which regions are filled. A bucketed allocator made it much faster than the original.
**Use it when:** self-intersecting or complex polygons needing a winding rule.

### PolyPartition — ivanfratric/polypartition
**Status:** MIT, pushed 2024. Checked: README.
**Principle:** several algorithms with a quality versus speed tradeoff, for triangulation and convex partitioning.
**Mechanism:** input must be non-self-intersecting, counter-clockwise for outer rings and clockwise for holes, with holes marked. Methods include ear clipping, optimal triangulation by dynamic programming, monotone triangulation, and convex partitioning by Hertel-Mehlhorn or optimal (literature).
**Use it when:** you want fewer pieces than triangles.

### poly-decomp.js — schteppe/poly-decomp.js
**Status:** MIT, pushed 2023. Checked: README, src/index.js.
**Principle:** split a concave polygon into convex pieces.
**Mechanism:** two algorithms, one optimal but slow (`decomp`) and one fast but not optimal (`quickDecomp`). Helpers: makeCCW, isSimple, removeCollinearPoints, removeDuplicatePoints.
**Use it when:** physics engines that need convex shapes.

### cdt2d — mikolalysenko/cdt2d
**Status:** MIT, pushed 2019, marked work in progress. Checked: README, cdt2d.js.
**Principle:** constrained Delaunay: a Delaunay triangulation that must contain given edges.
**Mechanism:** the requires show three stages: build an initial triangulation with a monotone sweep, flip edges toward the Delaunay condition (an edge is flipped when the opposite vertex lies inside the circumcircle) without crossing constraint edges, then filter out exterior or interior triangles.
**Use it when:** meshes that must follow boundaries.

### rectangle-decomposition — mikolalysenko/rectangle-decomposition
**Status:** MIT, pushed 2014. Checked: README, decomp.js.
**Principle:** minimum number of rectangles covering a rectilinear polygon.
**Mechanism:** the README cites a bipartite-matching method. Find axis-aligned chords that connect two concave vertices, build a bipartite graph of horizontal versus vertical chords that cross, take a maximum independent set (via matching), and cut along those chords, then split the rest (literature).
**Use it when:** tile layouts and axis-aligned fills.

## Hulls and shapes of point sets

### monotone-convex-hull-2d — mikolalysenko/monotone-convex-hull-2d
**Status:** MIT, pushed 2022. Checked: README, index.js.
**Mechanism:** Andrew's monotone chain, O(n log n): sort by x, build the lower and upper chains by popping points that make a non-left turn, using an exact orientation test. Returns clockwise indices.

### d3-polygon — d3/d3-polygon
**Status:** ISC, pushed 2023. Checked: README, src/hull.js.
**Mechanism:** area, centroid, containment, length and a convex hull computed with the monotone chain algorithm (upper hull then lower), using cross products.
**Idea:** signed area = 1/2 sum of (x_i·y_{i+1} − x_{i+1}·y_i); the centroid weights each edge by that term.

### QuickHull — akuukka/quickhull
**Status:** public domain per its README (GitHub shows none), pushed 2024. Checked: README, QuickHull.cpp.
**Mechanism (literature):** start from an extreme-point tetrahedron, assign each remaining point to the face it is farthest above, then repeatedly take the farthest point of a face, remove the faces visible from it and join the horizon edges to it. Epsilon defaults differ for float and double.

### concaveman — mapbox/concaveman
**Status:** ISC, pushed Jun 2026. Checked: README, index.js.
**Principle:** an outline of a point set that follows its shape, tunable.
**Mechanism:** start from the convex hull, then repeatedly dig into hull edges toward nearby interior points while a concavity criterion holds. It uses an R-tree for neighbor queries, a priority queue for the longest edges first, and robust orientation. `concavity` of 1 gives detail and infinity gives the convex hull; `lengthThreshold` stops digging at short segments.

### hull.js — andriiheonia/hull
**Status:** BSD-3-Clause, archived and deprecated. Checked: README, src/hull.js.
**Mechanism:** convex hull first, then refine edges using a grid and segment-intersection tests, with a concavity parameter (default 20). Prefer concaveman.

### alpha-shape — mikolalysenko/alpha-shape
**Status:** MIT, pushed 2015. Checked: README.
**Mechanism (literature):** triangulate the points (Delaunay), keep simplices whose circumscribed sphere is smaller than a threshold set by alpha. Small alpha gives detailed shapes with holes; large alpha approaches the convex hull. Works in any dimension.

### delaunay-triangulate — mikolalysenko/delaunay-triangulate
**Status:** MIT, pushed 2014. Checked: README, triangulate.js.
**Principle:** Delaunay in any dimension by lifting.
**Mechanism:** each point p becomes (p, |p|²); the lower convex hull of the lifted points, computed incrementally, is the Delaunay triangulation. An option adds a point at infinity.

### Delaunator — mapbox/delaunator
**Status:** ISC, 2.6k★, pushed Jun 2026. Checked: README, index.js.
**Mechanism:** a sweep-hull approach (literature): pick a seed triangle near the center, sort remaining points by distance from its circumcenter, add each to the growing hull and flip illegal edges using the incircle test. Outputs `triangles` (index triples) and `halfedges` (adjacency). Uses robust orientation.
**Use it when:** fast 2D Delaunay.

### d3-delaunay — d3/d3-delaunay
**Status:** ISC, pushed Nov 2025. Checked: README, src/delaunay.js.
**Mechanism:** Voronoi cells are built by connecting circumcenters of adjacent Delaunay triangles, clipped to a bounding box, with nearest-point lookup and path rendering.
**Idea:** for a point set, Voronoi cell of p = all locations closer to p than any other point.

### Voro++ — chr1shr/voro
**Status:** modified BSD (LBNL; GitHub shows no classification), pushed Mar 2026. Checked: README, src/v_compute.cc.
**Mechanism:** cell-based: computes each particle's Voronoi cell on its own, starting from a bounding box and cutting by the bisecting plane of each nearby particle until no farther particle can affect it. Good for per-cell statistics (volume, neighbors).

## Labels and skeletons

### polylabel — mapbox/polylabel
**Status:** ISC (LICENSE read; GitHub shows no classification), pushed Jun 2026. Checked: README, polylabel.js.
**Principle:** the pole of inaccessibility: the interior point farthest from the outline, best for placing a label.
**Mechanism:** cover the polygon with big square cells, rank cells in a priority queue by the best distance any point in them could achieve (center distance plus half the diagonal), discard cells that cannot beat the current best, and subdivide the rest. It finds the global optimum within a given precision.

### FloMat — FlorisSteenkamp/MAT
**Status:** no license detected (do not copy), pushed Oct 2026. Checked: README, src/mat/simplify-mat.ts.
**Principle:** the medial axis transform: the set of centers of maximal inscribed circles together with their radii; an analytic skeleton for Bezier shapes.
**Use it when:** shape morphing, thinning or fattening, thickness analysis. Built on flo-bezier3.

## Libraries

### Shapely — shapely/shapely
**Status:** BSD-3-Clause, pushed Oct 2026. Checked: README, src/shapely/strtree.py.
**Idea:** a Python geometry object model over GEOS, with an STRtree spatial index (sort-tile-recursive R-tree packing) and predicates (intersects, within, and others).

### GEOS — libgeos/geos
**Status:** LGPL-2.1, pushed Oct 2026. Checked: README, util/geosop.
**Idea:** a C++ port of JTS, used by PostGIS, Shapely and R's sf. Prepared geometries speed repeated predicates; the intersection matrix (DE-9IM) describes topological relations; precision models control coordinate snapping. Copyleft: study the technique, link the library, do not port code.
