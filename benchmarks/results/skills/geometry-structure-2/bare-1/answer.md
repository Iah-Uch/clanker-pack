For exact circular arcs, keep geometry in a curve-aware representation rather than flattening everything to polylines. Store arcs as center/radius and start/end angles (or use a standard format such as STEP); preserve them through transforms and export, and only tessellate for displays or machines that require it.

Useful open-source options:

- **Open CASCADE Technology (OCCT)**: mature CAD kernel with exact analytic curves and STEP support. **LGPL 2.1 with an additional exception**; check the exception and linking terms for your distribution.
- **libnest2d / Clipper2**: useful for 2D manufacturing geometry and offsets, but polygon-based workflows approximate arcs. Check each project’s license and arc support before adopting.
- **CavalierContours**: 2D polyline operations that retain bulge-encoded circular arcs. **MIT**; a focused option if that representation fits your needs.

For a commercial product, first define which operations must preserve arcs—offsetting, intersections, transforms, and G-code export—and test those cases. Avoid assuming a library is “exact” just because it accepts arc input: some operations convert curves to line segments internally.

Review the license of the exact version and dependencies you ship with counsel; this is product guidance, not legal advice.