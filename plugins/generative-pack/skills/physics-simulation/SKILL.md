---
name: physics-simulation
description: "Use when simulating or rendering physical systems: rigid bodies, joints, cloth and position-based dynamics, springs, fluids (grid, SPH, lattice Boltzmann), PDE and finite volume solvers, waves, reaction-diffusion, structural or topology optimization, N-body, molecular dynamics, particle transport, traffic, path tracing, optics, atmosphere or pigment color mixing. A catalog of techniques with mechanisms and formulas, to reason from, not a set of drop-in libraries."
---

# Physics and numerical simulation

A catalog of ideas drawn from about 51 open-source projects: how physical systems are modeled, discretized and stepped, and how light is simulated. Each entry gives the principle, the mechanism (formulas or steps), when to use it, and how to build it yourself.

## Read this first

- **These are not drop-in solutions.** A project is an example of a technique. Abstract the idea, adapt it to the task, combine it with others. Recommend a project only when it fits the user's stack, license and constraints.
- **Do not assume a library does what its name suggests.** Each entry says what I checked. "Literature" means the mechanism comes from the published algorithm rather than that project's code. Check current docs before relying on a feature.
- **Licenses matter when you reuse code.** MIT, BSD, ISC, Apache, CC0, zlib: adapt with notices. GPL, AGPL, LGPL: take the technique and write your own code. EPL is file-level copyleft. "No license detected": do not copy code. Several large projects have custom or mixed terms (FiPy, Geant4, NEURON); the entry says so.
- Facts were checked against each repository on 2026-10-15; projects change.

## Pick by goal

| You want | Read |
|---|---|
| Rigid bodies, joints, collision, cloth, ropes, springs and smoothing, falling sand | `references/01-rigid-bodies-constraints-springs.md` |
| Fluids, PDE solvers, ocean and electromagnetic waves, seismic waves, force-directed layout, quantum states | `references/02-fluids-pdes-waves-fields.md` |
| Reaction-diffusion, Turing patterns, river meanders, origami folding, topology optimization | `references/03-reaction-diffusion-patterns-structures.md` |
| Orbits, galaxies, black hole lensing, molecular dynamics, particle transport, neurons, traffic | `references/04-particles-nbody-molecular-agents.md` |
| Path tracing, differentiable rendering, optics, sky and atmosphere, realistic color mixing | `references/05-light-transport-optics-color.md` |

## Ideas that recur

- Step a state forward with a stable integrator (velocity Verlet, symplectic or implicit schemes) and constrain it (impulses, projections, pressure solves).
- Local stencils on grids or neighbor sums over particles, plus a spatial index.
- Conserve what must be conserved: finite volume fluxes, symplectic integrators, divergence-free projection.
- Exact solutions (damped springs) beat tuning a time step.
- Precompute and look up what is expensive; accumulate Monte Carlo samples over frames.
- Match the model to the question: a stylized approximation is often the right answer for graphics.

## How to answer with this

1. Match the goal to a reference and read only that file.
2. Explain the technique first, in terms of the user's problem. Mention a project as an example or possible tool, with its license.
3. If the user wants to build it, give the mechanism and a minimal recipe. Do not paste code from a copyleft project.
4. Combine entries freely: reaction-diffusion as a texture for a fluid surface, springs on top of a rigid-body engine, a path tracer with a precomputed sky.
