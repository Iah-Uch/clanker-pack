# CAD kernels, vector graphics, fonts and fabrication

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Scripted geometry is reproducible geometry.** A model described by code can be parametrized, diffed, and regenerated; this is why OpenSCAD and JSCAD exist.
- **B-rep topology** (vertices, edges, wires, faces, shells, solids) stores how pieces connect; the geometry (NURBS curves and surfaces) stores where they are.
- **Vector output for plotters** needs path optimization: merge touching lines, order paths to reduce pen travel, simplify.
- **Single-stroke fonts** (Hershey) store glyphs as a few polylines instead of outlines, which suits plotters and engraving.

## Solid modeling and CAD

### OpenSCAD — openscad/openscad
**Status:** GPL-2.0-or-later style license with a linking exception for CGAL (LICENSE head read; GitHub shows no classification), 10k★, pushed Oct 2026. Checked: README, LICENSE head, src/openscad.cc.
**Principle:** a solid is a program: primitives, transforms and boolean operations in a script, not an interactive session. Focused on mechanical parts rather than artistic modeling.
**Mechanism:** the script evaluates to a CSG tree of shapes and operations, which is then turned into a mesh by a geometry backend (CGAL is named in its license exception).
**Use it when:** parametric mechanical parts and 3D printing.

### JSCAD — jscad/OpenJSCAD.org
**Status:** MIT, pushed Sep 2026. Checked: README, an OpenSCAD deserializer file.
**Principle:** parametric 2D and 3D design in JavaScript, running in the browser or on the command line.
**Mechanism:** modular packages; CSG operations; exporters for formats such as 3MF and AMF; a converter reads OpenSCAD source into JSCAD solids.
**Use it when:** code-driven CAD in a JavaScript pipeline.

### truck — ricosjp/truck
**Status:** Apache-2.0, pushed Sep 2026. Checked: README, truck-topology/src/wire.rs.
**Principle:** a CAD kernel in Rust: boundary representation with NURBS geometry.
**Mechanism:** a topology crate defines wires (ordered edge loops), faces, shells and solids; geometry crates hold curves and surfaces; rendering targets WebGPU.
**Use it when:** you need B-rep modeling in Rust or the browser.

### Processing Geometry Suite — micycle1/PGS
**Status:** GPL-3.0, pushed Jul 2026. Checked: README, PGS_Voronoi.java.
**Idea:** a large set of 2D geometry algorithms as static methods that take and return Processing shapes, so they chain easily in creative code; built on the JTS geometry library (the imports are from LocationTech). Topics include concave and convex hulls, circle packing and Voronoi. Copyleft: study the techniques, do not port the code.

## Vector graphics and rendering

### Lyon — nical/lyon
**Status:** Apache-2.0 (LICENSE head read; GitHub shows no classification), pushed Oct 2026. Checked: README, crates/lyon/src/lib.rs.
**Principle:** turn SVG-style paths into triangles for GPU rendering.
**Mechanism (literature):** a fill tessellator sweeps the path left to right, decomposes it into monotone pieces and triangulates them; a stroke tessellator builds quads along segments with joins and caps. The result is plain vertex and index buffers.
**Use it when:** GPU vector rendering in games or UI.

### Paper.js — paperjs/paper.js
**Status:** MIT (LICENSE read; GitHub shows no classification), 15k★, pushed 2024. Checked: README, src/core/PaperScript.js.
**Principle:** a scene graph for vector graphics on canvas, with a scripting layer.
**Mechanism:** PaperScript is JavaScript with operator overloading: the source is parsed (with Acorn) and arithmetic on points is rewritten into method calls, so `a + b` works on vectors.
**Idea:** parse-and-rewrite is a cheap way to give a host language geometric operators.

### Go Graphics (gg) — fogleman/gg
**Status:** MIT, 4.8k★, pushed 2023. Checked: README, context.go.
**Mechanism:** a canvas-style drawing context in pure Go (paths, fills, strokes with round, butt or square caps and round or bevel joins, text), rasterizing through the freetype raster package. A good model of a small 2D API.

### Pts — williamngan/pts
**Status:** Apache-2.0, pushed Oct 2026. Checked: README, src/_triangulate.ts.
**Mechanism (read in the source comment):** Delaunay by incremental Bowyer-Watson: insert points one at a time in Hilbert-curve order so each new point is found by a short walk from the previous one; remove every triangle whose circumcircle contains the point and fan the hole from it; represent the convex hull with ghost triangles that share a vertex at infinity.
**Idea:** insertion order along a space-filling curve makes point location nearly constant time.

## Curves in the plane and fields

### MapGenerator — ProbableTrain/MapGenerator
**Status:** LGPL-3.0, pushed 2024. Checked: README, src/main.ts.
**Principle:** grow a city from a tensor field.
**Mechanism (literature: Chen et al. 2008, interactive procedural street modeling):** define a tensor field from basis fields (grid, radial) plus noise; trace streamlines along its major and minor eigenvector directions to get roads; the closed regions left between roads are blocks, then lots and buildings. The tool exposes each stage, and exports STL.
**Use it when:** procedural street networks. Idea is free to reimplement; the code is LGPL.

### distance-transform — scijs/distance-transform
**Status:** MIT, pushed 2016. Checked: README, lib/pp.js.
**Principle:** for every cell of a binary image, the distance to the nearest set cell.
**Mechanism (Meijster et al.):** two passes: a scan along each column to get the vertical distance, then along each row finding the lower envelope of parabolas (for the Euclidean case, comparing (x−i)² + g(i)² candidates, with a bisection to find where one candidate overtakes another). The code generalizes the comparison to Lp norms. O(n) per row.
**Use it when:** offsets, skeletons, SDFs from images, outlines.

## Plotters and fabrication

### vpype — abey79/vpype
**Status:** MIT, pushed Oct 2026. Checked: README, vpype_viewer/engine.py.
**Principle:** a command-line pipeline for vector files destined for pen plotters.
**Mechanism:** a chain of commands operating on layered line collections: layout and transforms, plotting optimization, generation, input and output, with a plug-in API; a GPU viewer shows pen-up travel separately from drawn lines.
**Idea:** treat plotting as a pipeline of small composable filters. The same shape works for any batch geometry job.

### Threading — piellardj/image-stylization-threading
**Status:** GPL-3.0, pushed 2024. Checked: README only.
**Principle:** string art: approximate an image with straight thread segments between pegs on a frame.
**Mechanism (literature on string art; the README gives the setup):** place pegs, then repeatedly choose the peg-to-peg segment that most reduces the error between the stacked threads and the target image (greedy selection), starting from the current peg. Monochrome uses one thread; color uses three. Exports SVG.
**Use it when:** any problem of the form "approximate an image with strokes".

### Protein Ribbon Diagrams — fogleman/ribbon
**Status:** MIT, pushed 2022. Checked: README, ribbon/mesh.go.
**Principle:** show the shape of a protein as a ribbon following its backbone.
**Mechanism (literature):** parse atoms from a PDB file, fit a smooth spline through backbone positions, and sweep a profile along it (flat and wide for sheets, a helix ribbon for helices), then output a triangle mesh and render it with a software rasterizer.
**Idea:** sweeping a profile along a curve is the general tube and ribbon recipe.

## Fonts and glyphs

### FontTools — fonttools/fonttools
**Status:** MIT, pushed Oct 2026. Checked: README, Lib/fontTools/fontBuilder.py.
**Idea:** read, edit and write font tables in Python. TTX converts fonts to and from XML. `FontBuilder` builds a working font from scratch, with a required order of setup calls because OpenType tables depend on each other.

### FontForge — fontforge/fontforge
**Status:** GPL-3.0-or-later as a whole, with many parts under more permissive terms (per its licensing note; the text I read is truncated), 8k★, pushed Oct 2026. Checked: README, LICENSE head.
**Idea:** create, edit and convert fonts across OpenType, TrueType, UFO and others; shows what a full glyph editing model needs (contours, hints, kerning, scripting).

### p5-hershey-js — LingDong-/p5-hershey-js
**Status:** MIT code (font data has its own terms; check), pushed 2020. Checked: README, p5.hershey.js.
**Principle:** the Hershey fonts store each glyph as a short sequence of stroke coordinates, developed around 1967 for vector displays.
**Mechanism:** the font file has one line per glyph: a five-character glyph code followed by the coordinate data (the parser slices the first five characters off each line). Draw by walking the pairs, lifting the pen at the separator.
**Use it when:** plotter text, engraving, retro vector looks.
