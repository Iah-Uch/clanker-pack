# Graphs, networks and pathfinding

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Separate the model from the view.** A graph data structure (nodes, edges, attributes, events) is one library; layout is another; rendering is a third. Graphology, ngraph and Sigma.js follow this split, so each part is swappable.
- **Force-directed layout.** Treat nodes as charged particles and edges as springs: repulsion F_r = k²/d between all pairs, attraction F_a = d²/k along edges (Fruchterman-Reingold), or springs with rest length. Integrate with damping until the energy settles. Naive repulsion is O(n²); a Barnes-Hut tree (quadtree or octree) approximates distant groups by their center of mass and brings it to O(n log n).
- **Shortest paths.** Dijkstra relaxes edges from a priority queue; A* adds a heuristic h(n) (admissible, never overestimating) and expands by f = g + h; on grids the Manhattan, octile or Euclidean distance serves as h.
- **Preprocess for fast queries.** Road networks use contraction hierarchies: order nodes by importance, contract them one by one adding shortcut edges that preserve shortest-path distances, then answer queries with a bidirectional search that only climbs the hierarchy.
- **Rendering at scale.** Draw nodes and edges with WebGL instanced primitives; hide labels by priority and zoom; use a spatial index for hit testing.

## Entries

### 3D Force Graph — vasturiano/3d-force-graph
**Status:** MIT, about 6.5k stars, pushed Sep 2026. Checked: README.
**Idea:** a web component that lays a graph out in 3D with a force simulation and renders it with Three.js; the physics engine is swappable between d3-force-3d and ngraph's 3D layout. 2D, VR and AR siblings share the same data model.
**Use it when:** exploring a network in an immersive view.

### Cytoscape.js — cytoscape/cytoscape.js
**Status:** MIT, about 11k stars, pushed Oct 2026. Checked: README.
**Idea:** graph theory and visualization in one library: selectors to style and query elements, a layout extension system (force, hierarchical, concentric, grid), and built-in algorithms (BFS, DFS, Dijkstra, A*, PageRank, centrality, components). Style by data via a CSS-like language.
**Use it when:** analysis plus display in one package, biological and knowledge-graph tools.

### Graphology — graphology/graphology
**Status:** MIT, about 1.8k stars, pushed Sep 2026. Checked: README.
**Idea:** one `Graph` object that supports directed, undirected and mixed graphs, self-loops, parallel edges, and events, plus a standard library of metrics, layouts, generators and traversals. The unified interface is the design lesson.

### Sigma.js — jacomyal/sigma.js
**Status:** MIT, about 12k stars, pushed Oct 2026. Checked: README.
**Idea:** WebGL rendering for thousands of nodes and edges on top of Graphology; node and edge programs are small shader pairs you can replace to change shapes.
**Use it when:** large graphs in the browser.

### ngraph — anvaka/ngraph
**Status:** MIT, about 1.5k stars, pushed Jun 2026. Checked: README.
**Idea:** a family of small modules (graph structure, force layout, path finding, generators, centrality) that compose into renderers such as VivaGraph. Read it for how to keep each concern in its own package.
**Mechanism (literature, ngraph.forcelayout):** Barnes-Hut tree for repulsion plus spring forces integrated with a velocity-Verlet-like step and drag.

### ngraph.path — anvaka/ngraph.path
**Status:** MIT, about 3.1k stars, pushed Jul 2026. Checked: README.
**Idea:** A* and Dijkstra over an ngraph graph with pluggable distance and heuristic callbacks, and a bidirectional variant (NBA*) that searches from both ends.

### PathFinding.js — qiao/PathFinding.js
**Status:** no license detected on GitHub (the field is empty), about 8.7k stars, pushed Jun 2024. Checked: metadata only. **Do not copy code**; the algorithms are textbook.
**Idea:** a grid pathfinding library: A*, Dijkstra, breadth-first, Jump Point Search, with options for diagonal movement and corner cutting.
**Mechanism (literature):** Jump Point Search prunes symmetric paths on uniform-cost grids by jumping along straight lines until a forced neighbor appears, which cuts expansions a lot.

### RoutingKit — RoutingKit/RoutingKit
**Status:** BSD-2-Clause, about 480 stars, pushed Apr 2026. Checked: README.
**Idea:** research-grade route planning from KIT: **Customizable Contraction Hierarchies** split preprocessing into a metric-independent ordering and a fast "customization" step that applies new arc weights (traffic, profiles), answering continental shortest-path queries in milliseconds; includes OpenStreetMap import and nearest-neighbor tools.
**Use it when:** routing on large road graphs with changing costs.

### PythonRobotics — AtsushiSakai/PythonRobotics
**Status:** MIT (the LICENSE head is the MIT text; GitHub shows no classification), about 31k stars, pushed Oct 2026. Checked: README.
**Idea:** a textbook with short, readable implementations of localization (extended Kalman filter, particle filter, histogram filter), mapping, SLAM, path planning (A*, RRT, potential fields, state lattice), path tracking and control. The mechanism of an algorithm is usually a page of NumPy.
**Mechanism (literature):** Kalman filter predict x' = F·x, P' = F·P·F^T + Q, update K = P·H^T·(H·P·H^T + R)^-1, x = x' + K·(z − H·x'); particle filter weights samples by measurement likelihood then resamples.
**Use it when:** learning or prototyping navigation, tracking and planning.
