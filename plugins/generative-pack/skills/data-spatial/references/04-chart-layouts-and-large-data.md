# Chart layouts, hierarchy, flow and large-data rendering

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Layout is a function from data to geometry.** A layout takes records and returns positions and sizes (chord angles, treemap rectangles, sankey node heights); drawing is separate and trivial.
- **Hierarchy layouts:** tree (tidy, cluster), partition, pack (nested circles), treemap (nested rectangles whose area is the value). Treemaps use a tiling rule: squarify keeps cells near square, slice-and-dice alternates directions.
- **Flow layouts:** sankey widths proportional to flow, with nodes ordered to reduce crossings and positions relaxed iteratively.
- **Rasterize before you draw.** For millions of points, aggregate into a pixel grid first (count or mean per bin), then map values to color; overplotting disappears and cost no longer depends on the number of points.
- **Text is a layout problem too.** Word clouds place words by trying spiral positions until no overlap; text shaping turns characters into positioned glyphs.

## Entries

### d3-hierarchy — d3/d3-hierarchy
**Status:** ISC, about 1.3k stars, pushed Apr 2025. Checked: README.
**Idea:** layouts for hierarchical data: tree (Reingold-Tilford tidy trees), cluster (dendrogram), partition (icicle or sunburst), pack (circle packing), treemap with several tilings.
**Mechanism (literature):** the squarified treemap fills a rectangle row by row, adding items to the current row while the worst aspect ratio improves; the circle pack uses a front-chain enclosing algorithm.

### d3-voronoi-treemap — Kcnarf/d3-voronoi-treemap
**Status:** BSD-3-Clause, about 225 stars, pushed Sep 2024. Checked: README.
**Principle:** a treemap whose cells are Voronoi polygons: given a convex polygon and nested weighted data, partition it so that each cell's area represents the weight.
**Mechanism (literature):** iterate weighted Voronoi tessellations (power diagrams): move the sites to cell centroids, adjust weights until each cell's area matches its target, recurse per hierarchy level. Organic shapes instead of rectangles.

### d3-sankey — d3/d3-sankey
**Status:** BSD-3-Clause, about 950 stars, pushed Nov 2023. Checked: README.
**Mechanism (literature):** assign nodes to columns by graph depth, scale node heights by flow, order nodes within columns and relax their vertical positions over several iterations to shorten links and reduce overlap; links are drawn as bands along cubic curves with width equal to the flow.

### d3-chord — d3/d3-chord
**Status:** ISC, about 130 stars, pushed Oct 2023. Checked: README.
**Mechanism:** a square flow matrix becomes arcs around a circle (group angle proportional to the row total) and ribbons between arcs (angle proportional to each cell); good for mutual flows among a few categories.

### d3-cloud — jasondavies/d3-cloud
**Status:** BSD-3-Clause, about 4k stars, pushed Mar 2026. Checked: README.
**Mechanism (literature):** sort words by size; for each word, start at a random point and walk an Archimedean or rectangular spiral outward until its bitmap or bounding box does not collide with placed words (a sprite mask and a hierarchical collision check make this fast); optional rotation per word.

### Datashader — holoviz/datashader
**Status:** BSD-3-Clause, about 3.6k stars, pushed Oct 2026. Checked: README.
**Principle:** the rasterization pipeline named in the README: project each record into zero or more bins of a plotting grid, compute reductions per bin (count, mean, any, std), then transform the aggregates (shading, normalization) into an image.
**Mechanism:** aggregation is a single pass over the data (parallelized with Numba), so cost is linear in records and independent of image size; color mapping with equalized histograms (rank-based, so structure at all densities is visible) avoids a saturated blob.
**Use it when:** billions of points, trajectories, time series.

### HarfBuzz — harfbuzz/harfbuzz
**Status:** the "Old MIT" license (the license file says so, with per-part notes; GitHub shows no classification), about 6.2k stars, pushed Oct 2026. Checked: license head, README.
**Principle:** text shaping: given a font and a string, produce the glyph ids and positions, applying OpenType layout tables for ligatures, kerning, contextual forms and complex scripts (Arabic joining, Indic reordering).
**Use it when:** rendering text correctly in any engine you build; never position glyphs by character code alone.
