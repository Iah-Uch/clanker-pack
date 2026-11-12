Use adaptive flattening: recursively split each cubic Bezier at t = 0.5 with de Casteljau until its control points are within a chosen distance tolerance of the endpoint chord. This gives finer polylines where the curve bends and fewer points on flatter sections. Set tolerance in output-space units for drawing; for collision, choose a tolerance based on the acceptable positional error. Add a recursion limit and handle sharp turns or cusps carefully.

For a ready-made example, mattdesl/adaptive-bezier-curve is designed for drawing, stroking, and collision. Its listed license is Modified BSD (Anti-Grid Geometry 2.4); retain its notices if you reuse code. You can also implement the short subdivision algorithm yourself.

For stroke meshes and joins, look at extrude-polyline (MIT); it consumes a polyline rather than flattening Beziers. For a broader curve toolkit with controlled accuracy and stroke operations, Kurbo is Apache-2.0.

My recommendation: implement adaptive flattening or use the BSD example, then pair it with a stroke library only if you need mesh output. Check the exact license files and notices in the version you ship.