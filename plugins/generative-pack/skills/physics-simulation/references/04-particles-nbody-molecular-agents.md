# N-body, molecular, particle transport, neurons and traffic

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Many interacting entities, one integrator.** Compute the force on each entity from the others, then advance with a stable integrator. Symplectic and velocity Verlet schemes conserve energy over long runs, where plain Euler drifts.
- **Neighbor lists and spatial decomposition** keep short-range interactions O(N): only look at entities within a cutoff, and split space among processors.
- **Monte Carlo transport:** sample random events from probability distributions (distance to next collision) and average many histories.
- **Discretize a continuous structure into compartments** (a neuron into cable segments, a road into cells) so the physics becomes a chain of small ODEs.
- **Precompute what is expensive and look it up in the shader** (black hole light paths, atmosphere scattering).

## Entries

### REBOUND — hannorein/rebound
**Status:** GPL-3.0, pushed Oct 2026. Checked: README, src/rebound.h.
**Principle:** integrate the motion of particles under gravity: planets, rings, moons, star clusters.
**Mechanism (literature):** direct summation of pairwise gravity (or a tree for large N) plus a choice of integrators: a symplectic Wisdom-Holman method that splits the motion into exact Kepler orbits and small perturbations, and an adaptive high-order method (IAS15) for close encounters. Orbital elements convert to and from Cartesian state.
**Use it when:** orbital mechanics, planetary system formation, generative astronomy. Copyleft: reimplement from the literature.

### Galaxy Renderer — beltoforion/Galaxy-Renderer
**Status:** BSD-2-Clause, pushed Jul 2026. Checked: README, GalaxyWnd.cpp.
**Principle:** spiral arms as a density wave, not as rotating material.
**Mechanism (literature, the author's article):** stars move on elliptical orbits; the ellipse's orientation is rotated progressively with radius, so the orbits line up in spiral patterns that persist while the stars themselves keep moving through. The program steps a fixed time interval per frame and draws stars, dust and glowing regions with OpenGL.
**Use it when:** galaxy visuals; any pattern that is a moving wave in stationary material.

### Black Hole Shader — ebruneton/black_hole_shader
**Status:** BSD-3-Clause, pushed 2020. Checked: README, black_hole/preprocess/preprocess_main.cc.
**Principle:** render a non-rotating black hole with an accretion disc and background stars in a WebGL2 shader (the model is in a paper, arXiv 2010.08735).
**Mechanism:** light follows null geodesics of the Schwarzschild metric; the bending depends on how close the ray passes. A command-line tool precomputes textures that tabulate the ray deflection and related quantities, so the shader only does lookups per pixel.
**Use it when:** gravitational lensing effects; a model for precompute-then-shade.

### LAMMPS — lammps/lammps
**Status:** GPL (README says GNU GPL; GitHub reports GPL-2.0), pushed Oct 2026. Checked: README, src/lammps.cpp includes.
**Principle:** massively parallel molecular dynamics of atoms and molecules.
**Mechanism (literature):** integrate Newton's equations with velocity Verlet; forces from pair potentials such as Lennard-Jones, V(r) = 4·eps·((sigma/r)^12 − (sigma/r)^6), found through neighbor lists with a cutoff; space is divided into bricks across processors (the source includes a brick communicator); accelerator packages for Kokkos and OpenMP.
**Use it when:** materials, fluids at the atomic scale. Copyleft: take the techniques.

### Geant4 — Geant4/geant4
**Status:** Geant4 Software License 1.0, a custom permissive license (head read; GitHub shows no classification). Pushed Oct 2026. Checked: README, a build-module check script.
**Principle:** simulate the passage of particles through matter (high-energy, nuclear, medical and space physics).
**Mechanism (literature):** a Monte Carlo transport loop: for each particle, sample the distance to the next interaction from cross sections, move it through a geometry of volumes, apply the sampled interaction, and track the secondary particles it creates. Source is organized into modules.
**Use it when:** radiation shielding, detector and dose simulations.

### NEURON — neuronsimulator/nrn
**Status:** BSD-style copyright notice with per-file exceptions (head read; GitHub shows no classification). Pushed Oct 2026. Checked: README, src/nrnpython/rxd_vol.cpp.
**Principle:** simulate neurons as cables of compartments.
**Mechanism (literature):** each compartment has a membrane equation C·dV/dt = −(sum of ion currents) + injected current, coupled to neighbors through axial resistance; the resulting tree-shaped linear system is solved in linear time. Its reaction-diffusion module handles chemicals in 3D, with tortuous diffusion coefficients and fluxes in x, y and z (seen in the source).
**Use it when:** neural models, biophysical simulation.

### Eclipse SUMO — eclipse-sumo/sumo
**Status:** EPL-2.0 (file-level weak copyleft), pushed Oct 2026. Checked: README, src/netwrite/NWWriter_SUMO.cpp.
**Principle:** microscopic traffic simulation: every vehicle is simulated individually on a road network, across modes of transport.
**Mechanism (literature):** each vehicle follows a car-following model that sets speed from the gap and speed of the leader, plus lane-change decisions and intersection rules; a network format describes lanes and junctions; tools import maps and generate routes.
**Use it when:** traffic flow, emergent congestion, urban mobility.
