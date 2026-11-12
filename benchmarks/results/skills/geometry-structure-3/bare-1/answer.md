For 270,000 faces down to 2,700, use mesh simplification: it reduces polygon count while trying to preserve the shape. Start with quadric-error-metric edge-collapse simplification; it’s widely used and practical for offline LOD generation.

Options:
- meshoptimizer: fast, production-oriented simplification; MIT license.
- OpenMesh: broader mesh-processing library with decimation modules; BSD-3-Clause.
- Blender’s Decimate modifier: useful for artist workflows; GPL-3.0-or-later, so check implications before incorporating it into a commercial product.
- Simplygon: commercial product with paid licensing and support.

For a commercial product, meshoptimizer is a strong first choice if its feature set fits. MIT and BSD-3-Clause generally permit commercial use, including in proprietary products, subject to their license notices and terms. Verify the exact version and any dependencies before shipping.

Test on your actual assets: the target face count alone doesn’t guarantee acceptable visual quality. Check silhouette, UVs, normals, materials, and animation needs; generate multiple LODs and choose thresholds based on screen size or distance.