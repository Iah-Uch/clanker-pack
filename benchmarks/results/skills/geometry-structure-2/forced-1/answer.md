For CAM, keep geometry as line and circular-arc segments (for example, a line/arc chain with center, radius, start and end angles). Run offsets and intersections on that representation; tessellate only for display. Robust predicates and explicit tolerances matter near tangencies and nearly coincident edges.

For a commercial product, start with **Clipper2** (Boost license) for 2D polygon clipping and offsetting. It uses integer coordinates, so choose a scale that preserves your required precision. It does not preserve exact arcs through polygon operations: use it only for polygonal work, or rebuild arc-aware operations on top.

If you need a full CAD kernel with exact curve geometry and B-rep operations, consider **Open CASCADE** (LGPL-2.1 with exception; check obligations for your distribution model) or **truck** (Apache-2.0, Rust, NURBS B-rep). These are broader than a 2D CAM path engine.

Recommendation: represent paths as analytic line/arc primitives and implement or adopt arc-aware offset/intersection logic. Avoid converting arcs to polylines anywhere in the manufacturing path. Use polygon kernels only where approximation is acceptable.