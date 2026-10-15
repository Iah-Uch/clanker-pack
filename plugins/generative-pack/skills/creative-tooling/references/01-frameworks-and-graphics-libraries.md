# Creative-coding frameworks and graphics libraries

A catalog of ideas. The projects are examples of each design, not drop-in solutions. "Checked" says what I read; "literature" marks general knowledge of the technique, not this project's code.

## Cross-cutting ideas

- **A sketch is a loop.** Every framework reduces to `setup()` once, then `draw(time)` per frame, with a canvas, a clock and input. The differences are how much state the framework hides.
- **Immediate vs retained mode.** Immediate mode (p5, canvas-sketch, openFrameworks, Cinder) re-issues drawing commands every frame. Retained mode (Three.js, Babylon.js, PixiJS) keeps a scene graph of objects and diffs it into draw calls.
- **Draw-call batching.** The GPU is fast, the CPU-to-GPU call is slow. Fast 2D engines merge many sprites with the same texture and blend state into one buffer and one draw call.
- **Render state as data.** regl-style libraries describe a draw as a declarative command (shader, attributes, uniforms, state) instead of a sequence of stateful `gl.*` calls, which removes whole bug classes.
- **Reconciliation.** React Three Fiber shows the pattern: a declarative tree diffed against a live scene graph, with the renderer being anything that has create, append, update and remove operations.
- **Compute-centric 2D.** Instead of rasterizing path triangles, run a GPU compute pipeline that flattens curves, bins them into tiles and accumulates coverage.

## 2D and sketch frameworks

### p5.js — processing/p5.js
**Status:** LGPL-2.1, about 24k stars, pushed Oct 2026. Checked: README, GitHub license field (the library license is the file in the repo; read it before bundling in closed code).
**Principle:** the Processing model for the browser: global `setup` and `draw`, a canvas, and a flat function vocabulary (`ellipse`, `noise`, `lerp`, `map`).
**Mechanism:** `draw` runs through `requestAnimationFrame`; state such as fill, stroke and transforms lives in a stack saved by `push()` and restored by `pop()`; a WebGL mode adds 3D with the same calls. Add-on libraries extend it.
**Use it when:** teaching, quick visual prototypes, a huge ecosystem of examples.
**Build it yourself:** a frame loop, a style stack, and a few mapping helpers (`map(v,a,b,c,d) = c + (v-a)/(b-a)*(d-c)`) cover the core in an afternoon.
**Pitfalls:** LGPL: linking is fine, modifying the library obliges you to share the changes. Global mode pollutes the namespace; use instance mode inside apps.

### py5 — py5coding/py5
**Status:** LGPL-2.1, pushed Oct 2026. Checked: README.
**Principle:** the Processing (Java) renderer exposed to CPython through a bridge, so sketches can use NumPy, Pillow and the Python ecosystem.
**Mechanism:** a JVM is started in-process; py5 wraps Processing's API in Python functions and converts between NumPy arrays and Processing pixel buffers.
**Use it when:** generative art in Python with Processing's rendering and libraries.
**Pitfalls:** needs a Java runtime; crossing the Python and Java boundary per pixel is slow, so move whole arrays.

### canvas-sketch — mattdesl/canvas-sketch
**Status:** MIT, about 5k stars, marked beta, pushed 2026. Checked: README.
**Principle:** a framework for making prints and animations: the sketch exports high-resolution, correctly sized output.
**Mechanism:** a sketch module exports a function that receives `{context, width, height, time, frame}` and returns a render function; settings declare physical size, units, DPI and pixel ratio, and the framework scales the canvas and handles export of PNG, video frames and SVG paths.
**Use it when:** art for print, plotter or video output where physical size and resolution matter.

### PixiJS — pixijs/pixijs
**Status:** MIT, about 48k stars, pushed 2026. Checked: README.
**Principle:** a fast 2D scene graph with GPU batching (WebGL and WebGPU).
**Mechanism (literature):** display objects form a tree with local transforms (2x3 matrices) multiplied down to world space; a renderer walks the tree, groups consecutive objects sharing texture and blend mode into batches and writes their vertices into one buffer per draw call; filters render to textures and apply fragment shaders.
**Use it when:** sprites, interactive 2D, many objects at 60 fps.
**Pitfalls:** texture atlas switches and blend-mode changes break batches; thousands of unique textures kill the speedup.

### Vello — linebender/vello
**Status:** Apache-2.0, pushed Oct 2026. Checked: README.
**Principle:** render vector 2D with GPU compute rather than the rasterizer.
**Mechanism (literature, the project's design notes):** a scene is encoded into a flat stream of path segments, transforms and draw tags; compute shaders flatten curves to lines, bin segments into tiles, run a prefix scan to find per-tile work, then fine-rasterize each tile accumulating coverage and blending. Three renderers exist, including a CPU one (`vello_cpu`) and a hybrid one.
**Use it when:** very large or dense vector scenes, UI renderers, anything where path-heavy rendering must stay on the GPU.
**Pitfalls:** young, Rust-first, needs a capable GPU API.

## 3D libraries

### Three.js — mrdoob/three.js
**Status:** MIT, about 116k stars, pushed Oct 2026. Checked: README.
**Principle:** a scene graph over WebGL and WebGPU: `Scene`, `Camera`, `Mesh = Geometry + Material`, `Renderer`.
**Mechanism (literature):** world matrix = parent world matrix × local matrix; the renderer frustum-culls, sorts opaque front-to-back and transparent back-to-front, sets uniforms (model, view, projection) and draws; materials map to shader programs, with `ShaderMaterial` accepting raw GLSL.
**Use it when:** almost any browser 3D. The reference for examples and community knowledge.
**Pitfalls:** dispose of geometries, materials and textures manually or memory leaks; allocation in the render loop causes garbage-collection stutter.

### React Three Fiber — pmndrs/react-three-fiber
**Status:** MIT, about 33k stars, pushed 2026. Checked: README.
**Principle:** a React reconciler whose host elements are Three.js objects.
**Mechanism:** JSX such as `<mesh><boxGeometry/></mesh>` is turned into constructor calls (`new THREE.Mesh`); props map to properties by name (`position-x` sets `position.x`); the render loop runs outside React state, and per-frame work goes in a `useFrame` callback that mutates objects directly.
**Use it when:** 3D in a React app with declarative composition and state.
**Pitfalls:** never put per-frame values in React state (re-renders at 60 fps); mutate refs.

### Babylon.js — BabylonJS/Babylon.js
**Status:** Apache-2.0, about 26k stars, pushed 2026. Checked: README.
**Principle:** a full engine rather than a library: physics, audio, GUI, a node-based material editor and inspector tooling are included.
**Use it when:** games and apps that want an integrated editor and tooling, TypeScript first.

### OGL — oframe/ogl
**Status:** no license detected on GitHub (the field is empty), about 4.7k stars, pushed 2025. Checked: metadata only. **Do not copy code until the license is confirmed with the author.**
**Idea:** a minimal WebGL library with a Three-like API and no dependencies, small enough to read in full: it shows how little is needed for `Program`, `Geometry`, `Mesh`, `Camera` and `Transform`.

### regl — regl-project/regl
**Status:** MIT, about 5.6k stars, pushed 2026. Checked: README.
**Principle:** functional WebGL: you declare a command and call it.
**Mechanism:** `regl({frag, vert, attributes, uniforms, count})` returns a function; uniforms may be values, functions of the frame context, or props passed per call; regl tracks the whole GL state and applies only the diff, so there is no hidden state leaking between commands.
**Use it when:** custom GPU effects, particle systems and GPGPU through framebuffers, without a scene graph.
**Build it yourself:** a state cache plus a command closure that binds program, buffers and uniforms is the entire idea.

## Native C++ toolkits

### openFrameworks — openframeworks/openFrameworks
**Status:** MIT (the license text is the first thing in the file; GitHub shows no classification), about 10k stars, pushed Oct 2026. Checked: LICENSE head, README.
**Principle:** a C++ toolkit for creative work: `setup/update/draw`, graphics, video, audio, computer vision and hardware through addons.
**Use it when:** installations that need native speed, cameras, projectors and hardware I/O.

### Cinder — cinder/Cinder
**Status:** BSD-style (the license head names redistribution terms; GitHub shows no classification), about 5.5k stars, pushed Mar 2026. Checked: license head, src/cinder/TriMesh.cpp.
**Idea:** a C++ library with a geometry-source and target abstraction: `geom::Source` objects (shapes, loaded meshes) are copied into any `geom::Target` such as a `TriMesh`, with attribute dimensions and index primitives negotiated between them, so procedural shapes, imports and GPU batches share one pipeline.
