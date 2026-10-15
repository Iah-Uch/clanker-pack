# 3D reconstruction, Gaussian splatting, depth and learned animation

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published method, not this project's code. Code license and weights license are separate; many 3D and face models also depend on third-party weights or data with their own terms. Read the model card.

## Cross-cutting ideas

- **Radiance fields.** Represent a scene as a function (position, view direction) to (color, density) and render by volume rendering along each ray: C = sum_i T_i·(1 − exp(−sigma_i·delta_i))·c_i, with transmittance T_i = exp(−sum_{j<i} sigma_j·delta_j). Fit the function to photos by gradient descent on the photometric error (NeRF).
- **Gaussian splatting.** Replace the implicit function with millions of explicit 3D Gaussians (position, covariance as scale and rotation, opacity, color from spherical harmonics). Render by projecting each Gaussian to a 2D ellipse (covariance Sigma' = J·W·Sigma·W^T·J^T) and alpha-blending front to back per tile. Differentiable, so the same photometric loss optimizes them; adaptive density control clones, splits and prunes Gaussians during training.
- **Camera poses first.** Both families need camera poses, usually from structure-from-motion (COLMAP).
- **Dynamic scenes** add time: a deformation field that moves canonical Gaussians per frame.
- **Feed-forward 3D from one image.** A big transformer predicts a 3D representation in one pass (triplane, sparse voxels), trained on large asset datasets, instead of optimizing per scene.
- **Monocular depth** gives per-pixel relative depth from one image, enough for relighting, parallax, layer separation and 2.5D effects.
- **Structured latents.** 3D generative models first compress assets into a compact latent on sparse voxels, then run diffusion in that latent space.

## Splatting and radiance fields

### gsplat — nerfstudio-project/gsplat
**Status:** Apache-2.0, about 5.8k stars, pushed Sep 2026. Checked: README.
**Idea:** the CUDA rasterizer for Gaussian splatting as a clean library: project, tile-bin, sort by depth, alpha-composite, with backward kernels for training and several densification strategies. The best place to read how the forward and backward pass are organized.

### Nerfstudio — nerfstudio-project/nerfstudio
**Status:** Apache-2.0, about 12k stars, pushed Jul 2025. Checked: README.
**Idea:** a modular framework for radiance-field research: data parsers (COLMAP, phone captures), a model zoo (nerfacto, splatfacto), a viewer, and export to point clouds, meshes and splats. Components are swappable, which is the design lesson.

### OpenSplat — WebODM/OpenSplat
**Status:** AGPL-3.0, about 2.2k stars, pushed Oct 2026. Checked: README.
**Idea:** a splatting trainer that runs on CPU and multiple GPU back ends (not only NVIDIA), driven from COLMAP, nerfstudio or OpenSfM outputs. AGPL: reimplement the technique from the splatting literature if the license does not fit.

### 4D Gaussian Splatting — hustvl/4DGaussians
**Status:** Apache-2.0, about 4k stars, pushed Oct 2024. Checked: README.
**Principle:** dynamic scenes with real-time rendering by deforming a set of canonical Gaussians over time.
**Mechanism (literature):** a compact spatial-temporal encoder (a multi-resolution HexPlane of feature grids over x, y, z, t) feeds a small decoder that outputs per-Gaussian position, rotation and scale offsets at time t; the rest is the standard splat rasterizer. The README reports training in about 8 minutes on D-NeRF data.
**Use it when:** multi-view video of moving scenes.

### Matrix-3D — SkyworkAI/Matrix-3D
**Status:** MIT, about 850 stars, pushed Nov 2025. Checked: README.
**Principle:** explorable 3D worlds from text or an image: generate a panoramic video along a camera trajectory, then lift it to 3D.
**Mechanism:** conditional video generation produces a wide-coverage panorama; two panoramic reconstruction methods (one fast, one detailed) turn it into 3D.

## Single-image 3D

### TRELLIS — microsoft/TRELLIS and TRELLIS.2 — microsoft/TRELLIS.2
**Status:** both MIT, about 14k and 12k stars, pushed Jun and Jul 2026. Checked: both READMEs.
**Principle:** generate 3D assets from structured latents on sparse voxels.
**Mechanism:** TRELLIS.2 uses a "field-free" sparse voxel structure (O-Voxel) that avoids iso-surface fields and so keeps complex topology, sharp features and PBR materials; a sparse 3D VAE with 16× spatial downsampling gives a compact latent, and vanilla diffusion transformers (4B parameters) generate it from an image.
**Use it when:** image-to-3D assets with textures; the idea of splitting geometry from appearance in one latent.

### TripoSR — VAST-AI-Research/TripoSR
**Status:** MIT, about 7k stars, pushed Jun 2026. Checked: README.
**Principle:** feed-forward single-image reconstruction following the Large Reconstruction Model design.
**Mechanism (literature):** an image encoder (a vision transformer) produces tokens, a transformer decodes them into a triplane (three axis-aligned feature planes); a point is shaded by projecting onto the three planes, summing features and passing them through a small MLP to density and color; the mesh comes from marching cubes. The README reports under 0.5 seconds on an A100.

### SAM 3D Objects — facebookresearch/sam-3d-objects
**Status:** the **SAM License** (a custom license for code and weights; the LICENSE head defines "SAM Materials"; read it before any use), about 7.5k stars, pushed Jun 2026. Checked: README, LICENSE head.
**Idea:** object reconstruction from an image and a mask, part of a pair of models with SAM 3D Body for human meshes.

## Depth, relighting and layers

### Depth Anything V2 — DepthAnything/Depth-Anything-V2
**Status:** code Apache-2.0, about 9k stars, pushed Mar 2026. Checked: README. Model sizes have different licenses on the hub; check the one you use.
**Principle:** a foundation model for relative depth.
**Mechanism (literature):** a vision transformer encoder with a DPT decoder, trained on synthetic images with precise depth to teach detail, then used to pseudo-label large amounts of real images for a student; output is a relative depth map, convertible with a scale and shift (or metric fine-tuned variants).
**Use it when:** parallax, fake depth of field, relighting, masking by depth, 2.5D effects.

### Glow Jam — hyun2xyz/Glowjam
**Status:** MIT, 6 stars, pushed Sep 2026. Checked: README.
**Principle:** relight a flat image with a depth map.
**Mechanism (literature):** derive normals from depth (n proportional to (−dz/dx, −dz/dy, 1)), then compute Lambert shading max(0, n·l) per pixel from a movable light, with optional specular and falloff, composited over the footage. The plug-in runs the depth model locally through ONNX Runtime.
**Use it when:** cheap relighting in compositing.

### See-through — shitagaki-lab/see-through
**Status:** Apache-2.0, about 4.6k stars, pushed Oct 2026. Checked: README.
**Principle:** decompose a single anime illustration into up to 23 inpainted layers with inferred draw order (hair, face, eyes, clothing), making a 2.5D rig for animation.
**Use it when:** turning static art into a puppet.

## Portrait animation

### LivePortrait — KlingAIResearch/LivePortrait
**Status:** code MIT (license text read; GitHub shows no classification), about 19k stars, pushed Jun 2026. Checked: README, LICENSE. Dependencies (face detector weights) may carry their own, stricter terms; read the README notes before commercial use.
**Principle:** portrait animation by implicit keypoints, with stitching and retargeting control.
**Mechanism (literature):** extract identity features and implicit 3D keypoints from the source image, compute driving keypoints from a video, warp the source features with the keypoint motion, decode to a frame; small stitching and retargeting modules (eyes, lips) keep the result natural and the paste-back seamless.
**Use it when:** animating a face photo from a driving video; works on animals too.
