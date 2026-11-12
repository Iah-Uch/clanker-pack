I’m applying the data-spatial skill. For a commercial mapping product, a practical stack is:

- **Projection and coordinate transforms:** PROJ, under the permissive MIT license.
- **Spherical and planar geometry:** S2 Geometry, Apache 2.0, for robust spherical operations; GEOS, LGPL 2.1+, for planar geometry.
- **Interactive web maps:** MapLibre GL JS, BSD 3-Clause. Pair it with your own tiles or a separately licensed tile provider.
- **Static maps and rendering:** Mapnik, LGPL 2.1+, or generate vector/raster tiles with tools such as tippecanoe, BSD 2-Clause.

Choose based on whether your core workload is projection, spherical topology, planar analysis, or rendering; these libraries complement each other. Check each project’s current license and dependencies before shipping, and treat map data, tiles, fonts, and imagery as separately licensed assets. This is technical guidance, not legal advice.