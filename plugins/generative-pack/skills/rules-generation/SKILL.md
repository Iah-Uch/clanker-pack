---
name: rules-generation
description: "Use when generating content from rules or randomness: noise (Perlin, simplex, Worley), L-systems, grammars, rewrite rules, wave function collapse, cellular automata, Lenia, diffusion-limited aggregation, differential growth, space colonization, slime or agent simulations, fractal flames, procedural art, brush or sketch rendering, aperiodic tilings, procedural maps or puzzle search. A catalog of techniques with mechanisms, to reason from, not a set of drop-in libraries."
---

# Rules and generation

A catalog of ideas drawn from about 35 open-source projects: how structure and variety arise from small rules plus randomness. Each entry gives the principle, the mechanism (formulas or steps), when to use it, and how to build it yourself.

## Read this first

- **These are not drop-in solutions.** A project is an example of a technique. Abstract the idea, adapt it to the task, combine it with others. Recommend a project only when it fits the user's stack, license and constraints.
- **Do not assume a library does what its name suggests.** Each entry says what I checked. "Literature" means the mechanism comes from the published algorithm rather than that project's code. Check current docs before relying on a feature.
- **Licenses matter when you reuse code.** MIT, BSD, ISC, Apache, CC0: adapt with notices. GPL, AGPL, LGPL: take the technique and write your own code. "No license detected": do not copy code. Code licenses do not cover bundled images or data.
- Facts were checked against each repository on 2026-10-15; projects change.

## Pick by goal

| You want | Read |
|---|---|
| Smooth random fields, terrain, clouds, cells, hashing, random numbers | `references/01-noise-and-randomness.md` |
| Output that follows rules: L-systems, grammars, rewrite programs, WFC, constraint generation | `references/02-grammars-rewriting-constraints.md` |
| Growth, branching, aggregation, cellular automata, Lenia, agents, fractal flames, fire | `references/03-growth-aggregation-agents.md` |
| Procedural art, sketchy and painterly rendering, aperiodic tilings, maps, staged puzzle search | `references/04-procedural-art-tilings-maps-search.md` |

## Ideas that recur

- Everything from one seed, so results are reproducible.
- Rewrite locally and repeat; complexity comes from iteration.
- Constraint propagation: remove impossibilities and let it cascade.
- Layered noise (octaves) for natural detail; domain warping for flow.
- A spatial index makes neighbor queries cheap, which makes growth and agents scale.
- Map-based agents: write to a field, diffuse and decay it, read it back.

## How to answer with this

1. Match the goal to a reference and read only that file.
2. Explain the technique first, in terms of the user's problem. Mention a project as an example or possible tool, with its license.
3. If the user wants to build it, give the mechanism and a minimal recipe. Do not paste code from a copyleft project.
4. Combine entries freely: for example WFC output decorated with noise, or an L-system drawn with a sketchy brush.
