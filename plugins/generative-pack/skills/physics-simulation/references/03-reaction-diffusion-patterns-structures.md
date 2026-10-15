# Reaction-diffusion, pattern formation and structural simulation

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Local update from a stencil.** Each cell's next value depends on its neighbors (a Laplacian is the average of neighbors minus the cell). A fragment shader or compute kernel does this on every cell in parallel, using two buffers that swap each step (ping-pong).
- **Turing patterns:** two substances that react and diffuse at different rates (a fast-spreading inhibitor, a slow activator) spontaneously form spots, stripes and labyrinths.
- **Relaxation toward constraints:** fold, bend or flow a structure by repeatedly nudging it toward satisfying many small constraints at once.
- **Optimize a density field.** Topology optimization starts with a block of material and removes what carries little load.

## Entries

### RDSystem — keijiro/RDSystem
**Status:** Unlicense, pushed Aug 2025. Checked: README only.
**Principle:** reaction-diffusion as a generative texture running on the GPU (Unity Custom Render Texture).
**Mechanism (the Gray-Scott model, literature):** two concentrations A and B per pixel. dA/dt = Da·laplacian(A) − A·B² + f·(1 − A); dB/dt = Db·laplacian(B) + A·B² − (k + f)·B. Feed rate f and kill rate k choose the pattern family (spots, worms, mitosis, coral). Update every frame from the previous frame's texture.
**Use it when:** organic animated textures, skin and coral looks.
**Build it yourself:** a two-channel texture, a 3x3 Laplacian kernel, several small steps per frame.

### Ready — GollyGang/ready
**Status:** GPL-3.0, pushed Sep 2025. Checked: README, src/readybase/stencils.cpp.
**Principle:** a laboratory for continuous and discrete cellular automata, reaction-diffusion and PDEs on grids and arbitrary meshes, using OpenCL.
**Mechanism:** the neighbor stencil is a first-class object (the source defines points and stencils), so the same rule can run on a square grid, a hexagonal grid or an irregular mesh, including surfaces. Copyleft: take the ideas.
**Use it when:** reaction-diffusion on curved surfaces and meshes.

### Turing Patterns — ijmbarr/turing-patterns
**Status:** MIT, pushed 2018. Checked: README, tutils.py.
**Idea:** a notebook that builds reaction-diffusion systems step by step with a small base class for state systems and animation, a clear way to learn how activator-inhibitor models form patterns.

### meanderpy — zsylvester/meanderpy
**Status:** Apache-2.0, pushed Feb 2026. Checked: README, meanderpy.py imports.
**Principle:** a river's centerline migrates; this module implements the numerical model of Howard and Knutson (1984).
**Mechanism (literature):** the migration rate at each point is driven by a weighted sum of the curvature of the channel upstream (the effect of upstream bends decays with distance); move each point along its normal by rate × dt, resample the line, and cut off a loop when two parts touch. The module can also build stratigraphy from the migrating channel.
**Use it when:** river and meander generation, terrain detail.

### Origami Simulator — amandaghassaei/OrigamiSimulator
**Status:** MIT, pushed Oct 2026. Checked: README, dependency file (no algorithm code read).
**Principle:** fold every crease at the same time instead of step by step.
**Mechanism (literature, Ghassaei, Demaine and Gershenfeld 2018):** model the paper as a triangulated mesh of bars (axial constraints that resist stretching) with torsional springs along creases whose target angle comes from the crease pattern; solve small displacements iteratively on the GPU until the structure settles.
**Use it when:** cloth-like folding, kinetic structures, deployable design.

### PyTopo3D — jihoonkim888/PyTopo3D
**Status:** MIT, pushed Jun 2026. Checked: README, pytopo3d/core/optimizer.py.
**Principle:** SIMP topology optimization: find the stiffest shape for a given amount of material.
**Mechanism (literature):** each voxel has a density x between a small minimum and 1. Stiffness is E = Emin + x^p·(E0 − Emin) with a penalty p around 3 so intermediate values are costly. Solve the finite element system K(x)·u = f, compute compliance c = f·u and its sensitivity dc/dx_e = −p·x_e^(p−1)·(E0 − Emin)·(u_e·k0·u_e), smooth the sensitivities with a filter, and update densities with an optimality-criteria rule that keeps the volume fixed. The code assembles the stiffness matrix in sparse form from 24x24 element blocks.
**Use it when:** lightweight structures, generative design for 3D printing.
