# Meshes, surfaces and 3D geometry

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Most mesh algorithms are linear algebra on a graph.** The cotangent Laplacian L (a sparse matrix built from triangle angles) turns smoothing, deformation, hole filling, and geodesic distance into solving L x = b.
- **Local-global iteration:** fix a hidden variable (rotations), solve the global linear system, then re-fit the hidden variable. ARAP deformation works this way.
- **Quadric error:** a vertex's squared distance to a set of planes is a quadratic form; summing the forms of neighboring faces tells you how much it costs to move or merge vertices.
- **Acceleration structures:** a bounding volume hierarchy or a grid makes ray and distance queries logarithmic.
- **Charts and atlases:** to texture a surface, cut it into pieces that flatten with low distortion, flatten each, then pack the pieces.

## Differential geometry and deformation

### Geometry Central — nmwsharp/geometry-central
**Status:** MIT, pushed Jun 2026. Checked: README, src/surface/intrinsic_geometry_interface.cpp.
**Principle:** a surface mesh data structure plus the operators of discrete differential geometry.
**Mechanism:** an element-based mesh with attached data containers; geometric quantities (edge lengths, normals, curvatures, tangent bases) are computed lazily on demand (the code wires each quantity to a compute function). The intrinsic geometry layer uses only edge lengths, so algorithms work after edge flips without positions. The heat method for geodesic distance (literature): diffuse heat from the source for a short time, normalize the gradient field, then solve a Poisson equation for distance.
**Use it when:** geodesics, parallel transport, curvature flows, vector fields on surfaces.
**Build it yourself:** the heat method needs two sparse solves with the cotangent Laplacian.

### libigl — libigl/libigl
**Status:** licensing is mixed: its description says MPL-2.0 core, GitHub reports GPL-3.0; check each module header. 5.1k★, pushed Sep 2026. Checked: README, an SVD kernel header.
**Principle:** a header-only toolbox of geometry processing functions on matrices.
**Mechanism (ARAP, literature):** as-rigid-as-possible deformation alternates a local step, fitting the best rotation per vertex by SVD of a 3x3 covariance matrix (the repo ships a fast Givens-rotation SVD kernel), with a global step solving a Laplacian system for new positions with the handles fixed.
**Use it when:** deformation, parameterization, curvature, boolean and remeshing prototypes.

### mesh-laplacian — mikolalysenko/mesh-laplacian
**Status:** MIT, pushed 2015. Checked: README, laplacian.js.
**Mechanism:** builds the mesh Laplacian with cotangent weights: for an edge (i,j) the weight is half the sum of the cotangents of the two opposite angles. Returns `[i, j, w]` triples to load into a sparse matrix.
**Idea:** with L in hand, smooth by solving (I − t·L) x' = x, which is stable for large time steps.

### unity-mesh-smoothing — mattatz/unity-mesh-smoothing
**Status:** MIT, pushed 2016. Checked: README, MeshSmoothing.cs header.
**Mechanism:** plain Laplacian smoothing moves each vertex toward the average of its neighbors, which shrinks the mesh. The HC (Humphrey's Classes) filter, from Vollmer et al., corrects part of the movement back toward the original positions; the README uses alpha 0.7 and beta 0.16.
**Idea:** smoothing without shrinkage needs a correction term that pulls back.

### hole_fixer — Erkaman/hole_fixer
**Status:** MIT, pushed 2018, demo quality. Checked: README, bundled Eigen sparse Cholesky.
**Principle:** fill a hole with a patch that blends smoothly into its surroundings.
**Mechanism (literature):** triangulate the hole boundary, subdivide to the target density, then fair the patch by minimizing a smoothness energy with the surrounding vertices fixed, which means solving a sparse linear system (the bundled Cholesky solver). Fairing with a higher-order operator gives tangent-continuous fills.

### barycentric — mikolalysenko/barycentric
**Status:** MIT, pushed 2014. Checked: README only.
**Idea:** barycentric coordinates express a point p in a simplex as weights summing to 1 on the vertices, p = sum of w_i·v_i. In a triangle, w_i is the area of the sub-triangle opposite vertex i over the total. They interpolate any per-vertex attribute.

## Remeshing, simplification, parameterization

### simplify — fogleman/simplify
**Status:** MIT, pushed 2017. Checked: README, simplify.go.
**Principle:** reduce triangles by collapsing edges in order of least error (Garland and Heckbert, SIGGRAPH 97).
**Mechanism:** every vertex gets a 4x4 quadric Q, the sum over its faces of p·pT for the plane p = (a, b, c, d). The cost of placing a vertex at v is vT·Q·v. A heap holds candidate pairs by cost; repeatedly collapse the cheapest pair into the position that minimizes the combined quadric (solve a linear system, or fall back to an endpoint or midpoint), update the neighbors' costs, until the face count target is met.
**Use it when:** LOD generation. The README shows 270,000 faces down to 2,700.

### meshoptimizer — zeux/meshoptimizer
**Status:** MIT, 8.6k★, pushed Oct 2026. Checked: README opening, src/vertexfilter.cpp (SIMD detection).
**Principle:** reorder and compress mesh data so GPUs process it faster.
**Mechanism (from its documented API, not read here):** vertex cache ordering, overdraw ordering, vertex fetch ordering, quadric-based simplification, index and vertex buffer compression, quantization, and SIMD decode filters.
**Use it when:** shipping meshes to the GPU or web.

### Instant Meshes — wjakob/instant-meshes
**Status:** BSD-style license (text read, GitHub shows no classification), pushed 2022. Checked: README, LICENSE head.
**Principle:** make a clean quad-dominant mesh whose edges follow the surface's principal directions.
**Mechanism (Jakob et al. 2015, literature):** optimize an orientation field (4-fold rotational symmetry) and a position field (a lattice with 2-fold symmetry) over a multi-resolution hierarchy with Gauss-Seidel smoothing, then extract mesh vertices and edges from the position field.
**Use it when:** automatic retopology.

### xatlas — jpcy/xatlas
**Status:** MIT, pushed 2024. Checked: README, source/xatlas/xatlas.h.
**Principle:** unwrap a mesh into texture coordinates and pack them into an atlas.
**Mechanism:** group faces into charts; the header lists chart types Planar, Ortho, LSCM (least-squares conformal maps) and Piecewise; flatten each chart; pack the charts into an atlas with either random or brute-force placement. A fork of thekla_atlas.
**Use it when:** baking lightmaps or texture painting on generated meshes.

### svg-mesh-3d — mattdesl/svg-mesh-3d
**Status:** MIT, pushed 2018. Checked: README, index.js requires.
**Mechanism:** parse the path, flatten curves into contours, simplify, clean intersections, run constrained Delaunay (cdt2d), normalize, return a triangle mesh. Best for silhouettes such as icons.

## Compression and formats

### Draco — google/draco
**Status:** Apache-2.0, 7.5k★, pushed Oct 2026. Checked: README news (pin versioned decoder URLs), a loader file.
**Principle:** compress mesh and point-cloud geometry for transmission.
**Mechanism (literature, not read here):** quantize attributes, predict values from neighbors, encode connectivity compactly, and entropy-code the residuals.
**Pitfalls:** pin to a versioned decoder URL as the README warns.

### OpenSubdiv — PixarAnimationStudios/OpenSubdiv
**Status:** Tomorrow Open Source Technology License 1.0, which is Apache-2.0 with a different trademark clause (GitHub shows no classification), pushed Oct 2026. Checked: README, LICENSE head, a TBB kernel.
**Mechanism:** evaluate subdivision surfaces on CPU (including a TBB-parallel kernel) and GPU. Subdivision rules refine a coarse control mesh into a smooth limit surface; regular regions reduce to B-spline patches (literature).

## Robust solids and processing libraries

### Manifold — elalish/manifold
**Status:** Apache-2.0, pushed Oct 2026. Checked: README, src/manifold.cpp.
**Principle:** triangle meshes that always represent a valid solid, with booleans that cannot produce broken output.
**Mechanism:** a CSG tree batches operations (csg_tree.h); the boolean is implemented in boolean3. Its published algorithm documentation covers the robustness approach; read it before copying the idea.
**Use it when:** CAD kernels, 3D printing pipelines. Also ships a JS/WASM API.

### Trimesh — mikedh/trimesh
**Status:** MIT, pushed Oct 2026. Checked: README, util.py.
**Idea:** a Python mesh object centered on watertight surfaces: loading, repair and queries.

### geometry3Sharp — gradientspace/geometry3Sharp
**Status:** BSL-1.0, pushed Jan 2026; README says a .NET 8 update is in a branch. Checked: README, spatial/MeshSignedDistanceGrid.cs.
**Mechanism:** a signed distance grid for a mesh: compute exact distances in a narrow band around the surface, then extend to the rest of the grid by fast sweeping. Signs come from inside/outside tests.
**Use it when:** converting a mesh to an SDF for offsets and booleans.

### CGAL — CGAL/cgal
**Status:** per-package GPL or LGPL (GitHub shows no classification; license headers per package), 6k★, pushed Oct 2026. Checked: README, LICENSE head, Tetrahedral_remeshing header.
**Idea:** the broadest computational geometry library: triangulations, meshing, booleans, arrangements and more, built around exact predicates. Copyleft: study algorithms, do not port code.

## Spatial queries, voxels, math, rendering, reconstruction

### Three Mesh BVH — gkjohnson/three-mesh-bvh
**Status:** MIT, pushed Oct 2026. Checked: README, src/webgpu/BVHComputeData.js.
**Principle:** a bounding volume hierarchy makes ray and spatial queries fast.
**Mechanism (literature):** build a binary tree of axis-aligned boxes by splitting along the longest axis (center, average or surface-area-heuristic split); queries skip any subtree whose box is missed or too far. The README casts 500 rays at an 80,000-triangle model at 60 fps. Examples include SDF generation, shape intersection and a WebGPU data layout.

### Embree — RenderKit/embree
**Status:** Apache-2.0, pushed Oct 2026. Checked: README, kernels/sycl/rthwif_embree_builder.cpp.
**Idea:** high-performance ray tracing kernels: BVH builders and SIMD traversal, with a SYCL path for Intel GPUs.

### voxelize — mikolalysenko/voxelize
**Status:** MIT, pushed 2014. Checked: README.
**Idea:** convert a triangle mesh into an ndarray of voxels with a given resolution, returning voxels, origin and resolution. The README does not state the method; common ones test triangle-box overlap for the surface and fill the interior by parity.

### glMatrix — toji/gl-matrix
**Status:** MIT, pushed Jul 2026. Checked: README, src/vec3.js.
**Idea:** hand-tuned vector and matrix math using an `out` parameter convention to avoid allocations, with a configurable array type (Float32Array by default).

### PyTorch3D — facebookresearch/pytorch3d
**Status:** BSD license text (GitHub shows no classification), pushed Sep 2026. Checked: README, structures/meshes.py docstring.
**Idea:** batches of meshes of varying size stored in three interchangeable representations (list, padded, packed), a differentiable mesh renderer, and mesh losses and sampling, so geometry can sit inside a training loop.

### COLMAP — colmap/colmap
**Status:** new BSD license (text read; dependencies are licensed separately), pushed Oct 2026. Checked: README, src/pycolmap/helpers.h.
**Principle:** recover camera poses and 3D structure from photos.
**Mechanism (literature):** detect and match features across images, verify matches geometrically, then incrementally register images, triangulating points and refining everything with bundle adjustment (minimize reprojection error). The MVS stage then estimates dense depth per image and fuses them. Python bindings exist as pycolmap.
