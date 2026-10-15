# Spatial indexes, clustering, terrain meshes and contours

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Index once, query many times.** A spatial index turns "which of these million items are near here" from O(n) into O(log n + k).
- **Static beats dynamic when you can.** If data does not change, build a packed, array-backed index (one typed array, transferable between threads, cheap to store) instead of a pointer tree.
- **Space-filling curves.** Sort items along a Hilbert curve and packed leaves become spatially coherent; the R-tree is then built bottom-up with no balancing.
- **Hierarchical aggregation for zoom.** Precompute clusters per zoom level so the browser draws a few hundred markers, not a million.
- **Hierarchical grids.** Cover the globe with cells that subdivide (S2, H3, quadtree tiles) so any point maps to an id, and neighbors, parents and children are arithmetic.
- **Level of detail from error.** Precompute a per-triangle or per-vertex error, then pick the coarsest mesh within a tolerance at runtime.
- **Topology-aware simplification.** Simplify shared borders once (arcs), not per polygon, so neighbors never separate.

## Entries

### RBush — mourner/rbush
**Status:** MIT, about 2.8k stars, pushed Oct 2026. Checked: README.
**Principle:** a dynamic R-tree: nodes hold bounding boxes that contain their children; search descends only into boxes that intersect the query.
**Mechanism (literature):** bulk loading uses OMT (overlap-minimizing top-down): sort by x, cut into vertical slices, sort each by y, pack; inserts choose the subtree needing least area enlargement and split with a heuristic.
**Use it when:** boxes that change over time (editors, collision, hit testing).

### Flatbush — mourner/flatbush
**Status:** ISC, about 1.6k stars, pushed Jul 2026. Checked: README.
**Principle:** a static packed Hilbert R-tree: compute each box's Hilbert index of its center, sort, fill leaves in order, build parent levels from consecutive groups of N children, store everything in one array buffer.
**Use it when:** millions of static rectangles or points; faster and smaller than a dynamic tree. The README states the trade-off: no adding or removing items after indexing.

### KDBush — mourner/kdbush
**Status:** ISC, about 700 stars, pushed Oct 2026. Checked: README.
**Principle:** a flat KD-tree for points, stored as one array buffer: recursively split by the median (via a selection algorithm), alternating x and y, with the tree implicit in array positions. About half the memory of Flatbush for points, per the README.

### flatqueue — mourner/flatqueue
**Status:** ISC, about 140 stars, pushed Jul 2026. Checked: README.
**Idea:** a binary heap priority queue on two flat arrays (values and priorities), the core of best-first search, nearest-neighbor queries and A*.

### d3-quadtree — d3/d3-quadtree
**Status:** ISC, about 240 stars, pushed Oct 2023. Checked: README.
**Principle:** recursive subdivision of 2D space into four quadrants; supports adding points, finding the closest point to (x, y) within a radius, and visiting nodes. The basis for Barnes-Hut approximation in d3-force and collision detection.

### Supercluster — mapbox/supercluster
**Status:** ISC, about 2.4k stars, pushed Sep 2026. Checked: README.
**Principle:** hierarchical greedy clustering of points for every zoom level.
**Mechanism (literature, the Mapbox write-up):** index all points with KDBush; for zoom z from max down to min, take each unvisited point, find neighbors within a pixel radius (converted to the zoom's scale), merge them into a cluster at their weighted centroid, and index those clusters for the next zoom; queries are bounding-box lookups per zoom. Cluster properties can be aggregated with map and reduce callbacks.
**Use it when:** maps with huge point sets.

### H3 — uber/h3
**Status:** Apache-2.0, about 6.6k stars, pushed Oct 2026. Checked: README.
**Principle:** hexagonal hierarchical geospatial index.
**Mechanism (literature):** project the sphere onto an icosahedron, cover each face with a hexagonal grid, subdivide by aperture 7 (each cell holds about seven children, rotated slightly) across 16 resolutions; twelve pentagons at the icosahedron's vertices absorb the topology. A cell is a 64-bit id; neighbors, rings, parents and children are bit and coordinate arithmetic.
**Use it when:** binning, density maps, joining data by area, smoothing. Hexagons have one neighbor distance, which makes gradients and smoothing cleaner than squares.
**Pitfalls:** cells do not nest exactly, so a child's area may spill across its parent.

### MARTINI — mapbox/martini
**Status:** ISC, about 660 stars, pushed Jun 2026. Checked: README, index.js.
**Principle:** real-time terrain mesh generation with Right-Triangulated Irregular Networks from a (2^k + 1)² height grid.
**Mechanism:** the grid is split into a binary tree of right triangles; triangle ids are positions in an implicit binary tree (the source reconstructs each triangle's corners from its id by repeated midpoint splitting); an error value per triangle is computed bottom-up as the vertical distance between the real height at the hypotenuse midpoint and the average of its endpoints, propagated up so a parent's error is at least its children's; at runtime, descend and split any triangle whose error exceeds the tolerance, then emit a crack-free mesh.
**Use it when:** terrain tiles with adjustable detail.

### TopoJSON Simplify — topojson/topojson-simplify
**Status:** ISC, about 100 stars, pushed Jan 2023. Checked: README.
**Principle:** topology-preserving simplification: `presimplify` gives every coordinate a weight (the area of the triangle it forms with its neighbors), `simplify` drops points below a threshold, and because shared arcs are stored once, neighboring shapes stay in agreement.
**Mechanism (literature):** Visvalingam's algorithm, which repeatedly removes the point with the smallest effective triangle area.

### d3-tricontour — Fil/d3-tricontour
**Status:** ISC, about 43 stars, pushed Sep 2026. Checked: README.
**Principle:** contours of scattered data: triangulate the points (Delaunay), then apply **meandering triangles** per threshold: in each triangle, classify the three vertices as above or below, and interpolate the crossing along the edges that change sign, joining them into polylines and then polygons.
**Use it when:** isolines from irregular samples (weather stations, sensors) without gridding first.

### d3-geo-voronoi — Fil/d3-geo-voronoi
**Status:** ISC, about 280 stars, pushed Mar 2026. Checked: README.
**Principle:** Voronoi and Delaunay on the sphere: the spherical Delaunay triangulation is the convex hull of the points as 3D unit vectors; Voronoi cells follow from the dual (circumcenters of the hull triangles). Also provides geographic contours and nearest-site queries.
**Use it when:** nearest-station maps, spherical meshes.
