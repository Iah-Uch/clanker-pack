# 3D data processing, point clouds, sun, sky and orbits

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published method, not this project's code.

## Cross-cutting ideas

- **Point clouds scale by hierarchy.** Store points in an octree; render only nodes whose projected size is above a threshold and stream nodes from disk or network on demand.
- **Registration.** Align two scans with Iterative Closest Point: match each point to its nearest neighbor, solve the best rigid transform for the matches (SVD of the cross-covariance matrix), apply it, repeat until the error stops falling.
- **Pipelines of filters.** Scientific visualization models data flow as a graph of sources, filters and mappers; the pipeline executes lazily when something is rendered.
- **Astronomy is mostly coordinates and time.** Positions come from series expansions in time; the Julian date is the common clock; observer position and sidereal time turn equatorial coordinates (right ascension, declination) into the sky seen from a place (azimuth, altitude).
- **Orbit propagation** from published element sets uses a simplified perturbation model, not full numerical integration.

## Entries

### Open3D — isl-org/Open3D
**Status:** MIT (license text read; GitHub shows no classification), about 14k stars, pushed Sep 2026. Checked: LICENSE head, README.
**Idea:** a library for 3D data: point cloud and mesh I/O, voxel grids, normal estimation, registration (ICP, global registration with RANSAC over FPFH features), surface reconstruction (Poisson, ball pivoting), TSDF volume integration, visualization, and a GPU tensor API.
**Use it when:** scan processing, aligning and meshing real-world data.

### PyVista — pyvista/pyvista
**Status:** MIT, about 3.9k stars, pushed Oct 2026. Checked: README.
**Idea:** a Pythonic wrapper over VTK: meshes are NumPy-backed objects, filters are methods (`clip`, `slice`, `contour`, `threshold`), plotting is one call. A lesson in hiding a heavy C++ pipeline behind a friendly API.

### VTK — Kitware/VTK
**Status:** BSD-style (the Copyright.txt head names the BSD-style conditions; GitHub shows no classification), about 3.2k stars, pushed Oct 2026. Checked: license head.
**Idea:** the scientific visualization toolkit: the source-filter-mapper-actor pipeline, a large algorithm library (marching cubes, streamlines, clipping, decimation, Delaunay), and rendering to screens, files and the web. Read it as the reference for classic visualization algorithms.

### Potree — potree/potree
**Status:** BSD-2-Clause style (license head read; GitHub shows no classification), about 5.6k stars, pushed Jan 2026. Checked: README, LICENSE head.
**Principle:** render point clouds of billions of points in a browser.
**Mechanism (literature, the author's paper):** a preprocessing step builds an octree (a multi-resolution hierarchy where each node holds a sparse subsample of the points in its cell); at runtime a priority queue loads and draws nodes ordered by projected screen size until a point budget is spent, so nearby areas are dense and far areas coarse. Points are drawn as sized splats with optional eye-dome lighting (a depth-based shading that makes structure visible without normals).
**Use it when:** LiDAR and photogrammetry viewers.

### SunCalc — mourner/suncalc
**Status:** BSD-2-Clause, about 3.5k stars, pushed Oct 2026. Checked: README, index.js (read).
**Principle:** sun and moon position, phases and rise and set times from a date and a location.
**Mechanism (read in the source):** days since J2000 shifted by ΔT (Terrestrial Time versus UT); the Sun's geometric mean longitude L0 = 280.46646° + 36000.76983°·T and mean anomaly M = 357.52911° + 35999.05029°·T, the equation of center C = 1.914602·sin M + 0.019993·sin 2M + 0.000289·sin 3M (degrees, with small T terms), giving the ecliptic longitude and then right ascension and declination through the obliquity; sidereal time = 280.46061837° + 360.98564736629°·d − longitude; hour angle H = sidereal time − right ascension; altitude = asin(sin φ·sin δ + cos φ·cos δ·cos H); azimuth = atan2(sin H, cos H·sin φ − tan δ·cos φ), with atmospheric refraction from Meeus 16.4. The README states it follows the conventions of established astronomical references.
**Use it when:** shadows, golden hour, daylight simulation, circadian lighting.
**Build it yourself:** the entire sun model fits in about fifty lines; a one-minute accuracy is typical for rise and set.

### python-sgp4 — brandon-rhodes/python-sgp4
**Status:** MIT, about 475 stars, pushed Sep 2026. Checked: README.
**Principle:** satellite positions from orbital element sets.
**Mechanism:** the package compiles the official SGP4 C++ code (Vallado's release of "Revisiting Spacetrack Report #3") and feeds it TLE or OMM element sets; SGP4 propagates mean elements with secular and periodic perturbations from Earth's oblateness and drag, returning position and velocity in the TEME frame; convert frames for latitude and longitude.
**Use it when:** satellite tracking, pass predictions, orbit art. Accuracy decays within days of the element epoch.

### SunPy — sunpy/sunpy
**Status:** BSD-2-Clause, about 1k stars, pushed Oct 2026. Checked: README.
**Idea:** solar physics data analysis: map objects that carry coordinate metadata (helioprojective, heliographic frames through Astropy), time-series and spectra containers, downloading of solar observations, and differential rotation of features.

### Astrometry.net — dstndstn/astrometry.net
**Status:** the code is under a 3-clause BSD-style license, but it links GPL libraries (a vendored GSL), so the license head says the whole work must be distributed under **GPL v3 or later**. About 870 stars, pushed Oct 2026. Checked: LICENSE head, README. Treat as copyleft.
**Principle:** blind plate solving: given an image of stars with unknown pointing, find where in the sky it is.
**Mechanism (literature, Lang et al. 2010):** detect stars, form "quads" of four stars and compute a scale- and rotation-invariant code from the positions of two of them in the frame defined by the other two; look the code up in a prebuilt index of quads from a star catalog with a k-d tree; verify candidate matches with a Bayesian test, then fit the world coordinate system.
**Use it when:** calibrating astronomical images; geometric hashing as a general technique for matching point patterns.
