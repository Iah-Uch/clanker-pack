# Maps, projections, globes and geographic data

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published method, not this project's code. Map data has its own licenses (OpenStreetMap is ODbL, tile services have terms); the code license does not cover the data.

## Cross-cutting ideas

- **Projections.** A projection maps (longitude lambda, latitude phi) on a sphere to plane coordinates (x, y), and every projection distorts something. Web Mercator: x = R·lambda, y = R·ln(tan(pi/4 + phi/2)); conformal (angles right), area grossly wrong near the poles. Equal-area projections (Albers, Mollweide) preserve area, compromise projections (Robinson, Winkel tripel) balance errors.
- **Datum and CRS.** Coordinates are meaningful only with their reference system. Transformations between systems (datum shifts, grids) are a numerical library's job, not hand-written trig.
- **Tiles.** Pre-cut the map into a pyramid of square tiles addressed by z/x/y: at zoom z the world is 2^z × 2^z tiles. Raster tiles are images, vector tiles carry geometry and attributes that the client styles and renders.
- **Vector tile pipeline.** Simplify and drop features per zoom so each tile stays under a size budget, quantize coordinates to a tile-local integer grid (typically 4096), encode as protobuf.
- **GPU map layers.** Keep data in buffers, draw layers with instanced shaders, pick with an offscreen color-coded pass.
- **Rendering the globe.** Treat the earth as an ellipsoid mesh with level-of-detail terrain tiles; draw imagery draped on it.
- **Equal-area pixelization of the sphere.** HEALPix divides the sphere into 12 base pixels, each subdivided into equal-area cells, with an index that supports fast neighbor and hierarchical operations.

## Entries

### Leaflet — Leaflet/Leaflet
**Status:** BSD-2-Clause, about 46k stars, pushed Oct 2026. Checked: README.
**Idea:** a small, mobile-friendly raster-tile map library with a plugin ecosystem. Layers (tiles, markers, vectors) share one pan and zoom model; the simplicity is the design lesson.
**Use it when:** a simple interactive map without vector styling needs.

### MapLibre GL JS — maplibre/maplibre-gl-js
**Status:** BSD-style (the license head names redistribution terms; GitHub shows no classification), about 12k stars, pushed Oct 2026. Checked: license head, README.
**Idea:** open vector-tile rendering in WebGL, descended from Mapbox GL JS before its license change. A style document (JSON) declares sources and layers; the renderer decodes tiles, tessellates polygons and draws lines and symbols with shaders, with smooth zoom and rotation, labels placed collision-free.
**Use it when:** styled vector maps with no usage fee.

### CesiumJS — CesiumGS/cesium
**Status:** Apache-2.0, about 16k stars, pushed Oct 2026. Checked: README.
**Idea:** a 3D globe and map engine: ellipsoid terrain with level of detail, imagery layers, 3D Tiles (an open format that streams massive 3D datasets as a spatial hierarchy), time-dynamic data through CZML.
**Use it when:** globes, 3D city models, satellites and flight paths.

### deck.gl — visgl/deck.gl
**Status:** MIT, about 15k stars, pushed Oct 2026. Checked: README.
**Idea:** a layer-based WebGL2 framework for large data: every layer (scatterplot, arc, hexagon, heat, trips) maps arrays of data accessors to GPU attributes, updates only changed attributes, and can be overlaid on any base map. Picking renders ids to an offscreen buffer.

### kepler.gl — keplergl/kepler.gl
**Status:** MIT, about 12k stars, pushed Oct 2026. Checked: README.
**Idea:** a no-code geospatial exploration application built on deck.gl: drag in CSV or GeoJSON, pick layers, filters and a time playback. A model for turning a visualization framework into a product.

### Tippecanoe — felt/tippecanoe
**Status:** BSD-2-Clause, about 1.6k stars, pushed Sep 2026. Checked: README.
**Idea:** builds vector tilesets from large GeoJSON, FlatGeobuf or CSV collections, choosing per-zoom strategies to stay within size limits: dropping the densest features, coalescing, clustering or simplifying so each tile stays readable and small.
**Use it when:** serving large datasets as vector tiles.

### d3-geo — d3/d3-geo
**Status:** ISC (license head read; GitHub shows no classification; read the full LICENSE file), about 1.1k stars, pushed Jun 2024. Checked: LICENSE head, README.
**Principle:** projections as composable stream transforms. Geometry flows through a pipeline: clip to the sphere (antimeridian cutting, small-circle clipping), project, resample adaptively (subdivide a segment until the projected midpoint is close to the interpolated one), then clip to the viewport.
**Mechanism:** spherical math for great-circle interpolation, distance, area and centroid; `d3.geoPath` turns projected geometry into SVG paths or canvas calls.
**Use it when:** static and interactive maps in any projection, spherical geometry.

### d3-geo-projection — d3/d3-geo-projection
**Status:** ISC (license head read), about 1.2k stars, pushed Jul 2023. Checked: LICENSE head, README.
**Idea:** dozens of extra projections (Robinson, Mollweide, Winkel tripel, interrupted, polyhedral) built on the d3-geo projection interface, plus command-line tools for reprojecting GeoJSON.

### PROJ — OSGeo/PROJ
**Status:** an MIT-style license with notes on bundled data (head read; GitHub shows no classification; read the file), about 2k stars, pushed Oct 2026. Checked: LICENSE head, README.
**Idea:** the standard library for coordinate reference systems and transformations: EPSG definitions, datum shifts by grid files, operation pipelines (`+proj=pipeline`), and inverse operations. Use it instead of hand-written geodesy.

### prettymaps — marceloprates/prettymaps
**Status:** **AGPL-3.0** (the README says so, and asks to keep the printed message on figures), about 14k stars, pushed Jul 2026. Checked: README.
**Idea:** artistic maps from OpenStreetMap data: query layers (streets, buildings, water, parks) with osmnx, clip to a circle or rectangle, draw each layer as styled polygons with matplotlib, optionally export for plotters via vsketch. A recipe for turning map data into posters. Copyleft: reimplement the recipe with your own code.
**Pitfalls:** OSM data carries ODbL attribution requirements.

### earth — cambecc/earth
**Status:** MIT, about 6.6k stars, pushed Oct 2022. Checked: README.
**Principle:** an animated global wind map: a vector field sampled from forecast data (a grid of u and v wind components, interpolated bilinearly) is shown by thousands of particles advected through the field, each leaving a fading trail.
**Mechanism (literature):** each frame, move a particle by (u, v)·dt in projected space, fade the previous frame's canvas slightly, draw the new segment, respawn particles that leave the field or age out. Same recipe works for ocean currents or any 2D flow.
**Use it when:** visualizing any vector field.

### GPlates — GPlates/GPlates
**Status:** GPL (the license file is the GPL text; GitHub shows no classification), about 150 stars, pushed Oct 2026. Checked: README, license head.
**Idea:** plate-tectonic reconstruction: features carry a plate id and a rotation model assigns each plate a finite rotation (a rotation about an Euler pole by an angle) through geologic time; to move a feature to a past time, apply the composition of rotations along the plate hierarchy. A desktop app plus the PyGPlates library. Copyleft: reuse the math, not the code.

### healpy — healpy/healpy
**Status:** GPL-2.0, about 320 stars, pushed Oct 2026. Checked: metadata, README.
**Principle:** HEALPix maps in Python: equal-area pixelization with a hierarchical (nested) or ring ordering, used for sky maps (cosmic microwave background); includes spherical harmonic transforms (map to coefficients a_lm and back), smoothing by multiplying coefficients with a beam window, and projection views.
**Use it when:** any data on the full sphere needing equal-area bins or spectral analysis.
