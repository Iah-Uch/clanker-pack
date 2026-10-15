# Classic rendering from first principles, and vector-field visualization

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published technique, not this project's code.

## Cross-cutting ideas

- **Understand the pipeline by writing it.** A software renderer needs only line drawing, triangle rasterization with barycentric coordinates, a z-buffer, and matrix transforms; everything a GPU does is an optimization of that.
- **Barycentric coordinates.** For a triangle with vertices A, B, C, a point P = u·A + v·B + w·C with u + v + w = 1; P is inside if all are non-negative; the same weights interpolate depth, color, normals and texture coordinates.
- **Heightmap tricks.** A terrain stored as height and color maps can be drawn by casting columns from the screen bottom up, projecting each sample, and drawing a vertical strip when it rises above the horizon so far.
- **Smear noise along a field.** Line integral convolution shows a vector field by averaging a noise texture along streamlines.

## Entries

### tinyrenderer — ssloy/tinyrenderer
**Status:** a zlib-style custom license (head read: "provided as-is", permission terms; GitHub shows no classification), about 24k stars, pushed Jul 2026. Checked: README, LICENSE head. The README says the code is of little interest and the course notes are the point.
**Course path (from the README):** Bresenham line drawing, triangle rasterization, barycentric coordinates, hidden-face removal with a z-buffer, then perspective, shading and shaders written as plain functions.
**Mechanism:** Bresenham steps along the major axis, accumulating an error term to decide when to step the minor axis; triangles are filled by testing every pixel in the bounding box with barycentric coordinates; the z-buffer keeps the nearest depth per pixel.
**Use it when:** learning or teaching graphics; building a rasterizer for a platform with no GPU.

### VoxelSpace — s-macke/VoxelSpace
**Status:** MIT, about 6.8k stars, pushed Apr 2024. Checked: README.
**Principle:** the Comanche terrain engine in under twenty lines: a height map and a color map, rendered on the CPU without polygons.
**Mechanism (README and literature):** for each screen column, march along the ray in the ground plane from the camera outward in steps of increasing size; at each step read the terrain height, project it to a screen y with perspective (y = (cameraHeight − terrainHeight) / z · scale + horizon); if y is above the highest line drawn so far in this column, draw a vertical strip from y down to that line in the sampled color, and update the line. Front to back, with occlusion handled by the running maximum.
**Use it when:** retro landscapes, cheap terrain on weak hardware, a very small rendering exercise.

### LineIntegralConvolutions — AstroKriel/LineIntegralConvolutions
**Status:** MIT, about 24 stars, pushed Sep 2026. Checked: README.
**Principle:** visualize a 2D vector field with line integral convolution.
**Mechanism (literature, Cabral and Leedom 1993):** start with white noise; for each pixel, trace a short streamline forward and backward through the field (integrating dx/dt = v(x), for example with Runge-Kutta), average the noise along the streamline with a kernel (box or Hann), and write the result; noise is correlated along the flow and uncorrelated across it, so the image is streaky in the direction of the field. Multiplying by magnitude or coloring by a scalar adds information; iterating (LIC on the LIC) sharpens.
**Use it when:** wind, fluid, plasma, magnetic fields, any flow data.
