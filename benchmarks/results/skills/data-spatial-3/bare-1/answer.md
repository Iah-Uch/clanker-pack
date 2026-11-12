For spherical geometry, use **S2** as the core spatial model. It represents the globe as a hierarchy of cells, supports robust spherical predicates and indexing, and is Apache 2.0 licensed. It’s a strong fit for geometry and queries, but not a complete map renderer.

For projections and map display, consider **PROJ** (MIT) for coordinate transforms and **MapLibre GL JS** (BSD 3-Clause) for interactive vector maps. For static maps, **Mapnik** (LGPL 2.1) is an option. Check each project’s current license and dependencies before shipping.

A practical stack is S2 for spherical operations, PROJ for projections, and a renderer suited to your client platform. Confirm that your data sources and any fonts, tiles, or styles also permit commercial use; their terms can matter as much as the software license.

If you need specialized projection support or seamless globe rendering, evaluate the renderer’s projection capabilities before committing.