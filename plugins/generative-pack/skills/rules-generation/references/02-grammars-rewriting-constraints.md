# Grammars, rewrite rules and constraint-based generation

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Generate by rewriting.** Start with a seed (an axiom, a pixel, a shape) and repeatedly apply local rules. Complexity comes from repetition, not from a complicated rule.
- **Parallel versus sequential rewriting.** L-systems rewrite every symbol at once each step; Markov-style programs pick one place at a time.
- **Constraint propagation.** Give every cell a set of possible values; each decision removes impossible values from its neighbors, which cascades. Contradiction means backtrack or restart.
- **Learn the rules from an example.** Count which small patterns occur in a sample image, then generate output made only of those patterns.
- **Stochastic choice** (weighted random rule selection) turns one grammar into endless variations.

## Entries

### WaveFunctionCollapse — mxgmn/WaveFunctionCollapse
**Status:** MIT (LICENSE head read; GitHub shows no classification), 25k★, pushed Oct 2026. Checked: README, SimpleTiledModel.cs.
**Principle:** produce output locally similar to a sample: every NxN window in the output occurs in the input (C1), and pattern frequencies are similar (weak C2).
**Mechanism:** (1) extract all NxN patterns from the sample (optionally with rotations and reflections) with counts as weights. (2) Give each output cell the full set of patterns as possible. (3) Repeat: pick the undecided cell with the lowest entropy (the fewest weighted options, with tiny noise to break ties) and collapse it to one pattern chosen by weight; then propagate: any pattern that does not overlap-match a neighbor's remaining options is removed, and removals cascade until stable. (4) On contradiction (a cell with no options), restart. A simple tiled model uses explicit adjacency rules between named tiles instead of overlapping patterns.
**Use it when:** textures, levels, maps and structures that must look like a sample.
**Build it yourself:** the loop above, using a stack for propagation; entropy H = log(sum w) − (sum w·log w)/(sum w).
**Pitfalls:** contradictions are common with sparse samples; larger N gives more fidelity but fewer variations.

### NDWFC — LingDong-/ndwfc
**Status:** MIT, pushed 2020. Checked: README, ndwfc-tools.js.
**Idea:** the same algorithm abstracted to any number of dimensions, with a canvas that expands on demand and web-worker threading; the core makes no assumption about content, and a separate tools file builds tile prototypes, symmetry transforms and weights for 2D and 3D.
**Use it when:** 3D structures, endless worlds.

### MarkovJunior — mxgmn/MarkovJunior
**Status:** MIT, 8k★, pushed Mar 2026. Checked: README, source/Field.cs.
**Principle:** a program is an ordered list of rewrite rules on a grid; rules are applied wherever they match, and inference by constraint propagation can steer toward goals.
**Mechanism:** a rule such as `RBB=GGR` replaces a red-black-black pattern with green-green-red; the interpreter repeatedly picks a random match of the first applicable rule (MazeBacktracker is just two such rules). "Fields" (the source defines recompute, inverse and essential options) are distance potentials used to bias where rules fire, so a program can grow toward a target. It ships many example programs.
**Use it when:** mazes, dungeons, growth patterns and structures from tiny rule lists.

### ConvChain — mxgmn/ConvChain
**Status:** mostly MIT, check individual files; sample images are not part of the software (LICENSE head read). Pushed 2022. Checked: README, ConvChainFast.cs header.
**Principle:** a Markov chain of images that converges to a distribution matching the sample's NxN patterns.
**Mechanism:** weight each NxN pattern by its count in the sample; repeatedly flip a random pixel and accept or reject the change by the Metropolis rule using the ratio of the weights of the affected windows, so the final probability of a pattern is proportional to its weight. Typical N is 3.
**Use it when:** organic bitmap patterns, as a statistical alternative to WFC with no hard constraints.

### Lindenmayer — nylki/lindenmayer
**Status:** MIT, pushed Jun 2025. Checked: README, lindenmayer.js.
**Principle:** L-systems: an axiom string and productions applied in parallel to every symbol each iteration, then interpreted as drawing commands.
**Mechanism:** supports branching with `[` and `]`, context-sensitive and parametric productions, stochastic choice, and JavaScript functions as productions; it parses the classic syntax from The Algorithmic Beauty of Plants. Turtle interpretation (literature): `F` draws forward, `+` and `-` turn, `[` pushes position and heading, `]` pops them. Example: axiom `F`, rule `F -> F[+F]F[-F]F` yields a branching plant after a few iterations.
**Use it when:** plants, fractals, branching structures.

### Context Free — MtnViewJohn/context-free
**Status:** GPL-2.0, pushed Oct 2026. Checked: README, a GUI source file.
**Principle:** a grammar describes shapes and rules; the renderer expands it into images with millions of shapes.
**Mechanism (literature on CFDG):** a rule names a shape and lists the shapes it produces, each with geometric and color adjustments (rotate, scale, move, hue); multiple rules for one shape carry weights; recursion continues until shapes are smaller than a pixel. Includes the Anti-Grain Geometry rasterizer. Copyleft: reimplement from the idea.
**Use it when:** self-similar art, trees, spirals and fractals from short rule sets.

### Orca — hundredrabbits/Orca
**Status:** MIT, pushed Nov 2025. Checked: README, desktop/sources/scripts/core/orca.js.
**Principle:** a two-dimensional esoteric language: each letter on a grid is an operator, lowercase letters operate on bang, uppercase letters run every frame.
**Mechanism:** a frame counter drives a parse then operate loop over the grid; operators send MIDI, OSC or UDP to external instruments. It is a livecoding environment, not a synthesizer.
**Use it when:** procedural sequencers; a model of grids as programs.
