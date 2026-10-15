# Curves, splines, strokes and fields

A catalog of ideas. The projects below are examples of each technique, not drop-in solutions. Use the principle and mechanism to build what the task needs, and cite the project only when it is the right tool. "Checked" says what I read; anything marked "literature" comes from the published algorithm, not from this project's code.

## Cross-cutting ideas

- A curve is a function of a parameter. Almost every operation (drawing, length, offsetting, intersecting) is either sampling that function, or solving an equation in the parameter.
- Flatten adaptively: subdivide until a flatness tolerance is met, instead of sampling at a fixed step.
- Convert to a polynomial (power) basis when you need exact algebra such as roots, extrema and intersections.
- Smooth by local rules (corner cutting, spline fitting) and simplify by dropping points within a tolerance. Those two are inverse operations in spirit.

---

### adaptive-bezier-curve — mattdesl/adaptive-bezier-curve
**Status:** Modified BSD (Anti-Grain Geometry 2.4 license), pushed 2014. Checked: LICENSE, function.js.
**Principle:** turn a cubic Bezier into a polyline with as few points as the on-screen scale needs.
**Mechanism:** recursively split the curve at t = 0.5 (de Casteljau). Stop when the control points lie within a distance tolerance of the chord (compared squared), optionally also an angle tolerance and a cusp limit; cap recursion (default 8). The tolerance is divided by the display `scale`, so zoomed-in curves get more points.
**Use it when:** you need a polyline from a Bezier for drawing, stroking, or collision.
**Build it yourself:** `flatten(p0,p1,p2,p3)`: if flat(p0..p3, tol) emit p3 else split at 0.5 and recurse on both halves.
**Pitfalls:** fixed recursion cap limits accuracy on extreme curves; cusps need the angle/cusp options.

### b-spline — thibauts/b-spline
**Status:** MIT, pushed 2022. Checked: README, index.js.
**Principle:** a B-spline is a weighted blend of control points with local support; de Boor's algorithm evaluates it stably.
**Mechanism:** for degree p and n control points the knot vector has n+p+1 entries. Remap t into the valid domain [knots[p], knots[n]]. Find the knot span containing t, then repeatedly interpolate: d(r,i) = (1−a)·d(r−1,i−1) + a·d(r−1,i), with a = (t − knot[i]) / (knot[i+p+1−r] − knot[i]). Optional weights make it a rational curve (NURBS); clamped knots (repeated ends) make the curve pass through the first and last point.
**Use it when:** smooth curves through or near control points in any dimension.
**Build it yourself:** the loop above is about 20 lines.
**Variations:** NURBS, Catmull-Rom (interpolating), Bezier (a special clamped case).
**Pitfalls:** degree must be at most n−1; wrong knot vector length is the common bug.

### Bezier.js — Pomax/bezierjs
**Status:** MIT, 1.9k★, pushed 2024; maintainer asks for funding. Checked: README, src/utils.js, src/bezier.js.
**Principle:** quadratic and cubic Beziers have closed-form or cheap numeric answers to most geometry questions.
**Mechanism:** the utilities carry 24-point Gauss-Legendre abscissae for arc-length integration (L = integral of |B'(t)| dt), and a real cube-root helper for solving cubic equations (extrema and inflections come from roots of the derivative).
**Use it when:** you need length, bounding boxes, splitting, projection of a point, or intersections for 2D/3D Beziers.
**Build it yourself:** length by Gauss-Legendre; extrema by solving B'(t)=0 per axis; bbox from extrema plus endpoints.
**Pitfalls:** the README warns the legacy ES5 version differs; numeric tolerance is 1e-6.

### chaikin-smooth — Experience-Monks/chaikin-smooth
**Status:** MIT, pushed 2018. Checked: README (worked example).
**Principle:** corner cutting: replace each corner with two points closer to it.
**Mechanism:** for each segment P→Q emit 0.75·P+0.25·Q and 0.25·P+0.75·Q, keeping the first and last points. The README example [0,0],[25,25],[13,13] yields 6.25, 18.75, 22, 16 along the diagonal, confirming 1/4 and 3/4. Repeating it converges to a quadratic B-spline (literature).
**Use it when:** you want a smooth-looking path from a rough polyline with no solver.
**Variations:** change the cut ratio (1/4 is the classic); iterate k times.

### fit-curve — soswow/fit-curve
**Status:** MIT, pushed 2020. Checked: README, header of src/fit-curve.js.
**Principle:** fit a few cubic Beziers to many points (Schneider, Graphics Gems 1990).
**Mechanism (literature):** parameterize points by chord length; estimate end tangents; solve a 2x2 least-squares system for the two control-handle lengths along the tangents; measure the maximum squared error; if too large, refine the parameters with Newton-Raphson, and if still too large split at the worst point and recurse. The `error` argument is a squared distance.
**Use it when:** vectorizing freehand input or traced outlines into smooth paths.
**Pitfalls:** duplicate points are removed first; corners should be split before fitting.

### FloBezier — FlorisSteenkamp/FloBezier
**Status:** MIT, pushed Oct 2026. Checked: README, src/index.ts exports.
**Principle:** robust Bezier geometry: intersections, curvature, closest points.
**Mechanism:** the exports show it works through power-basis conversion and hodographs (the derivative curve), with curve-curve intersection returning each point plus both parameters (a cubic pair can have up to 9 intersections), self-intersection, total curvature and curvature extrema, and closest or furthest point or distance between beziers.
**Use it when:** correctness matters more than speed, such as CAD-like boolean work.
**Build it yourself:** express both curves as polynomials, eliminate one variable, and find roots of the resulting polynomial.

### Kurbo — linebender/kurbo
**Status:** Apache-2.0, pushed Oct 2026. Checked: README, svg.rs, stroke.rs.
**Principle:** curve library with an accuracy parameter and analytic results where possible.
**Mechanism:** signed area uses Green's theorem, A = 1/2 times the closed integral of (x dy − y dx), which reduces to a sum over segments. Strokes take a join (bevel, miter, round) and a cap; SVG arcs are converted between endpoint and center forms (adapted from lyon).
**Use it when:** you need area, length, offset or stroke outlines with controlled error.
**Build it yourself:** per-segment area via Green's theorem is a few lines for polylines, and a closed form for Beziers.

### NURBS-Python (geomdl) — orbingol/NURBS-Python
**Status:** MIT, pushed 2025. Checked: README, geomdl/NURBS.py, operations.py.
**Principle:** the full NURBS toolkit from Piegl and Tiller's NURBS Book, in pure Python.
**Mechanism:** operations listed are evaluation, derivatives, knot insertion, knot removal, knot refinement, degree elevation and reduction, plus curve and surface fitting by interpolation and by least squares. Weighted control points are stored as homogeneous coordinates (x·w, y·w, w).
**Use it when:** you need exact CAD-style curves or surfaces and refinement operations.
**Build it yourself:** homogeneous coordinates turn rational evaluation into ordinary B-spline evaluation followed by a divide.

### TinySpline — msteinbeck/tinyspline
**Status:** MIT, 1.4k★, pushed 2024. Checked: README feature list.
**Principle:** one spline type covers B-splines, NURBS and Beziers, with the practical operations around it.
**Mechanism:** interpolation by cubic natural splines and centripetal Catmull-Rom; sampling at equal distances; reparametrization by arc length (a map between length and knot); knot insertion; sub-spline extraction; Bezier decomposition; derivatives; degree elevation; rotation-minimizing frames; morphing between splines.
**Use it when:** you need constant-speed travel along a spline or a twist-free frame for a sweep.
**Build it yourself:** arc-length parameterization: tabulate cumulative length, then invert by binary search.
**Pitfalls:** centripetal Catmull-Rom avoids cusps and overshoot compared to uniform.

### libspiro — fontforge/libspiro
**Status:** GPL (README says GPL2+; GitHub reports GPL-3.0), pushed 2024. Checked: README, spiro.c.
**Principle:** draw smooth curves with only on-curve points, by using clothoid-like spirals whose curvature varies smoothly, so the result looks fair.
**Mechanism:** each segment is a polynomial spiral: its curvature is a low-order polynomial in arc length (the code keeps four coefficients `ks[4]` per segment and integrates them numerically). A banded linear system is solved (the code carries a band-diagonal matrix with an LU-style decomposition) so that tangent angles and curvature match across points. The solved spirals are emitted as Bezier segments.
**Use it when:** designing letterforms or logos where curvature continuity matters.
**Build it yourself:** it is research-grade; copyleft license means take the idea, not the code.

### Perfect Freehand — steveruizok/perfect-freehand
**Status:** MIT, 5.8k★, pushed Apr 2026. Checked: README, getStrokePoints.ts, getStrokeOutlinePoints.ts.
**Principle:** turn noisy pointer input into a smooth, pressure-aware filled outline.
**Mechanism:** first build stroke points: smooth the input with a streamline factor (each new point moves part of the way toward the input), and keep per-point vector, distance, running length and pressure. Then offset left and right of the path by a radius computed from pressure (or simulated from speed), adding caps and corner arcs, and emit one polygon. Very short strokes become a dot.
**Use it when:** drawing apps, signatures, ink-like lines.
**Build it yourself:** exponential smoothing for the path, normals for the offset, radius = f(pressure or speed).

### svgpathtools — mathandy/svgpathtools
**Status:** MIT, pushed Oct 2026. Checked: README feature list.
**Principle:** treat each SVG segment as a polynomial so analysis is algebra.
**Mechanism:** convert Bezier segments to numpy `poly1d` polynomials and back; compute tangents, right-hand normals and curvature; intersect paths; bounding boxes; reverse; split into continuous subpaths.
**Use it when:** analyzing or preparing SVG outlines in Python.
**Build it yourself:** curvature k = (x'y'' − y'x'') / (x'² + y'²)^(3/2).

### polyline-normals — mattdesl/polyline-normals
**Status:** MIT, pushed 2023. Checked: README, index.js.
**Principle:** thick lines on the GPU need a per-vertex offset direction and miter length.
**Mechanism:** for each vertex take the unit direction of the incoming and outgoing segments, form each segment's normal, and the miter direction is their normalized sum; the miter length (output next to the normal) is 1/cos of half the turn angle, which grows as the corner sharpens. The shader offsets each vertex by normal times miter length times half the width.
**Use it when:** drawing wide lines in a vertex shader.
**Pitfalls:** sharp corners explode without a miter limit; see extrude-polyline.

### extrude-polyline — mattdesl/extrude-polyline
**Status:** MIT, pushed 2019. Checked: README, index.js.
**Principle:** turn a centerline into a triangle mesh with join and cap styles and a variable width.
**Mechanism:** options are thickness, cap (butt, square), join (miter, bevel) and a miter limit that falls back to bevel. A `mapThickness(point, i, points)` function sets width per point (taper). Output is positions and triangle cells.
**Use it when:** you need stroke geometry as a mesh, not a canvas stroke.

### d3-shape — d3/d3-shape
**Status:** ISC, pushed Oct 2023. Checked: README, src/arc.js, src/index.js.
**Principle:** shape generators driven by data accessors.
**Mechanism:** the module exports arc, area, line, pie, radial variants, link and symbol generators. The arc generator takes inner and outer radius, start and end angle and a pad angle, and handles the geometry of rounded corners with line intersections (the `intersect` helper in the code).
**Use it when:** charts, radial layouts, or any generated path from data.
**Build it yourself:** a pie is cumulative angles from values; an arc is two radii and two angles.

### Simplify.js — mourner/simplify-js
**Status:** BSD-2-Clause, pushed 2022. Checked: README, simplify.js (distance helpers).
**Principle:** reduce a polyline's points while staying within a tolerance.
**Mechanism:** squared distance of a point to a segment (project onto the segment, clamp t to 0..1) drives the Douglas-Peucker recursion: keep the point farthest from the chord if it exceeds the tolerance, recurse on both halves. A cheap radial-distance pass first drops points closer than the tolerance to their neighbor (literature).
**Use it when:** cutting vertex counts for rendering or storage.
**Pitfalls:** it does not preserve topology (simplified lines can self-intersect).

### Repulsive Curves — ythea/repulsive-curves
**Status:** MIT, pushed 2022. Checked: README, src/tpe_energy_sc.cpp, tpe_flow_sc.cpp.
**Principle:** untangle curves by minimizing an energy that is large when curves nearly touch or come close in a tangent sense, so the curve flows to a tidy, well-spaced shape (Yu, Schumacher, Crane 2020).
**Mechanism:** the tangent-point energy sums, over pairs of points x and y, a kernel of the form |projection of (x−y) perpendicular to the tangent at x| to the power alpha, divided by |x−y| to the power beta. The solver is a gradient flow with a preconditioned (Sobolev-type) inner product, with constraints and multigrid support in the code (parameters `alpha`, `beta`).
**Use it when:** knot or tangle relaxation, spacing of curves.
**Pitfalls:** research code, needs CMake and Eigen-style dependencies.

### streamlines — anvaka/streamlines
**Status:** MIT, pushed Apr 2026. Checked: README, lib/streamLineIntegrator.js, createLookupGrid.js.
**Principle:** draw a vector field as evenly spaced curves.
**Mechanism:** integrate each streamline with a Runge-Kutta 4 step, forward then backward from a seed, until it hits the boundary, comes too close to another line (checked through a spatial lookup grid sized to the step) or loops. New seeds are taken beside existing lines at the separation distance (Jobard-Lefer, literature).
**Use it when:** wind maps, flow fields, tensor-field based layouts.
**Build it yourself:** RK4: k1=f(p), k2=f(p+h/2·k1), k3=f(p+h/2·k2), k4=f(p+h·k3); p += h/6·(k1+2k2+2k3+k4).

### Field Play — anvaka/fieldplay
**Status:** MIT, pushed Sep 2026. Checked: README, src/lib/autoPresets.js.
**Principle:** a vector field is a function from position to velocity; thousands of particles show it.
**Mechanism:** the user supplies a GLSL function `vec2 get_velocity(vec2 p)`; particles are advected on the GPU each frame with a time step, fade trails by a factor, and respawn with a drop probability.
**Use it when:** exploring or prototyping fields before using them in a generator.
