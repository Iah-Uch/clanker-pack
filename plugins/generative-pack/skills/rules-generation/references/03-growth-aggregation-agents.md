# Growth, aggregation, cellular automata and agent systems

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Local rules, global form.** Each element reacts only to nearby neighbors (repel, attract, stick, sense); structure emerges.
- **A spatial index is the performance trick.** Nearly every growth system asks "what is near me?" thousands of times; a grid or tree makes that cheap.
- **Growth plus constraint.** Add elements, but refuse placements that cross or crowd existing ones, and you get non-overlapping branching networks.
- **Reaction and diffusion of a field.** Agents write to a map, the map diffuses and decays, agents read it: this is how trails and chemical patterns form.
- **Continuous automata:** replace discrete cell states with real numbers and neighbor counts with a smooth kernel convolution.

## Branching and non-overlapping growth

### space-colonization — nicknikolov/space-colonization
**Status:** no license detected (do not copy code), pushed 2016. Checked: README, index.js (options).
**Principle:** grow tree-like and bush-like forms toward a cloud of attractors (Runions et al. 2007).
**Mechanism (literature):** scatter attractor points in the volume the tree should fill. Each step, every attractor influences its nearest branch tip within an influence radius; each tip grows a segment in the normalized average direction to its attractors; attractors within a kill distance of a tip are deleted. Repeat until no attractors remain. The shape of the attractor cloud becomes the crown. Inputs are `buds` (start positions) and `hormones` (attractors).
**Use it when:** trees, veins, roots, lightning, any branching that fills a shape.

### Hyphae — inconvergent/hyphae
**Status:** MIT, archived, pushed 2014. Checked: README, hyphae.py.
**Principle:** root-like networks where no edges overlap.
**Mechanism:** nodes extend by small random-angle steps and sometimes branch; a candidate node is rejected if it lands within a radius of existing nodes (found through a spatial index), so growth stops where space is taken.
**Use it when:** leaf veins, river deltas, cracks.

### Differential Mesh — inconvergent/differential-mesh
**Status:** MIT, archived, pushed 2016. Checked: README, main_sources.py constants.
**Principle:** an extension of Hyphae that mimics lichen growth: a triangle mesh that grows at its outer edge without crossing itself.
**Mechanism:** vertices repel others within a near distance and attract within a far distance (the source defines both as radii and an attract strength), new triangles are appended on outside edges, and edges that stretch past a limit are split. Small triangles give a crystalline or biological look.

### differential-line — inconvergent/differential-line
**Status:** MIT, archived, pushed 2018. Checked: README, main_line_ani.py.
**Principle:** differential growth of a curve: the model behind coral, brain folds and many plants (README cites Nervous System's Floraform and a differential-growth paper from Toronto).
**Mechanism (standard form):** nodes along a curve are joined by springs to their neighbors, repel every node within a near radius, and a new node is inserted in any edge that grows too long. The curve must fold to fit, producing wrinkles.
**Use it when:** organic outlines, maze-like folding, generative lace.

## Aggregation and agents

### dlaf — fogleman/dlaf
**Status:** MIT, pushed 2020. Checked: README, dlaf.cpp parameters.
**Principle:** diffusion-limited aggregation: random walkers stick to a growing cluster, producing fractal dendrites.
**Mechanism:** release a particle far away; move it by random steps; when it comes within the attraction distance of the cluster it joins (with stickiness as a probability and stubbornness as how many touches before sticking), recording its parent. A spatial index (Boost R-tree) makes the nearest-neighbor test fast: about 35 seconds for a million points on one core in 2D or 3D. Parameters in the source: particle spacing, attraction distance, minimum move distance, stubbornness, stickiness.
**Use it when:** frost, lightning, coral, mineral growth.

### Slime-Simulation — SebLague/Slime-Simulation
**Status:** GPL-3.0, pushed 2023. Checked: README, Assets/Scripts/Slime/Simulation.cs.
**Principle:** Physarum-style agents that follow and reinforce trails (based on a published slime-mould model).
**Mechanism:** each agent has a position and heading; it samples the trail map at three sensor points ahead, turns toward the strongest, moves, and deposits trail. Each frame the map is blurred (diffused) and decayed. The Unity compute shader has separate kernels for agent update, map diffusion and coloring. Spawn modes include random, point, and circle layouts.
**Use it when:** organic networks, vein-like patterns, GPU particle art. Copyleft: reimplement.

### Lenia — Chakazul/Lenia
**Status:** MIT, pushed 2024. Checked: README, Python/old/Lenia.py imports.
**Principle:** continuous cellular automata that produce lifelike, moving creatures.
**Mechanism:** cell values are real numbers in [0, 1]. Each step: convolve the grid with a smooth ring-shaped kernel K to get a neighborhood potential U; map it with a growth function G (a bump around a target value mu with width sigma, positive near mu and negative elsewhere); update A = clip(A + dt × G(U), 0, 1). The code does the convolution with FFT. Later versions add multiple kernels and channels.
**Use it when:** artificial life, organic animation.
**Build it yourself:** FFT convolution, a Gaussian bump growth function, a small time step (around 0.1).

### sandspiel — MaxBittker/sandspiel
**Status:** MIT, pushed Sep 2026. Checked: README; the file I read was backend glue, not the simulation.
**Idea:** a falling-sand cellular automaton in Rust compiled to WebAssembly with WebGL drawing, where each cell holds a material and updates by simple neighbor rules; it supports sharing and forking of creations. In falling-sand games the typical trick is updating cells in a scan order that alternates direction so motion has no bias.

## Fractal and fire effects

### flam3 — scottdraves/flam3
**Status:** GPL-3.0, pushed Sep 2026. Checked: README, flam3-genome.c.
**Principle:** fractal flames: iterated function systems with nonlinear variations, rendered by density.
**Mechanism (literature, Draves and Reckase):** the chaos game: keep a point; repeatedly pick a transform at random by weight; apply an affine map then a weighted sum of nonlinear variation functions (sinusoidal, spherical and many others), then an optional final transform; plot the point into a histogram, with a color value blended toward the transform's color. Render with log-density tone mapping, so sparse areas stay visible, and gamma. Genomes (parameter sets) can be mutated and mated, hence the "genetic language"; tools: render, animate, genome. Copyleft: reimplement from the paper.
**Use it when:** fractal art, evolving parameter sets.

### doom-fire-algorithm — filipedeschamps/doom-fire-algorithm
**Status:** MIT, pushed Oct 2026. Checked: README, playground/.../fire.js.
**Principle:** fire as a heat field on a pixel grid, using a palette lookup.
**Mechanism:** each pixel holds an intensity index into a palette (the source has a 37-color ramp from near black to white). The bottom row is set to the maximum. Each frame, every pixel copies the intensity of the pixel below it minus a small random decay, written to a slightly randomized horizontal position; this makes flames flicker and taper upward.
**Use it when:** cheap fire, smoke or glow effects; any "propagate and decay" effect.
