# Fluids, PDE solvers, waves and force fields

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **Discretize, then step.** A PDE becomes arithmetic once you choose a grid (finite differences or finite volumes), particles (SPH), or basis functions (spectral), plus a time stepper (explicit, implicit, Crank-Nicolson).
- **Eulerian versus Lagrangian.** Grid methods store fields at fixed points; particle methods carry the quantities with the material.
- **Projection for incompressibility:** advect, add forces, then solve a Poisson equation for pressure and subtract its gradient so the velocity is divergence-free.
- **Conservation form** (finite volume): update each cell by the flux through its faces; what leaves one cell enters its neighbor, so mass and energy are preserved.
- **Fourier tricks:** ocean surfaces and other wave fields are sums of sinusoids; build the spectrum, then one inverse FFT gives the whole surface.
- **Force-directed layout is a physics simulation** of springs and repulsion, cooled until it settles.

## Fluids

### WebGL Fluid Simulation — PavelDoGreat/WebGL-Fluid-Simulation
**Status:** MIT, 17k★, pushed 2024. Checked: README references, script.js.
**Principle:** real-time 2D incompressible fluid on the GPU (it cites GPU Gems chapter 38, fast fluid dynamics).
**Mechanism (literature, stable fluids):** each frame, in fragment shaders: advect velocity by tracing each pixel backward along the velocity (semi-Lagrangian, unconditionally stable); add forces and optional vorticity confinement to keep swirls; compute divergence; solve the pressure Poisson equation with a few Jacobi iterations; subtract the pressure gradient; advect the dye with the final velocity.
**Use it when:** interactive smoke, ink, and swirling visuals.

### SPlisHSPlasH — InteractiveComputerGraphics/SPlisHSPlasH
**Status:** MIT, pushed Oct 2026. Checked: README, SPlisHSPlasH/SPHKernels.h.
**Principle:** smoothed particle hydrodynamics: the fluid is particles; any field is a kernel-weighted sum over neighbors.
**Mechanism:** a smoothing kernel W (the header defines a cubic spline kernel, with AVX variants) gives density rho_i = sum_j m_j·W(|x_i − x_j|, h) over neighbors within radius h; pressure, viscosity and surface tension forces are likewise sums; incompressible variants enforce density constancy iteratively (literature: PCISPH, DFSPH). Also covers deformable solids.
**Use it when:** splashes, free surfaces, particle fluids.

### latticeboltzmann-python — pmocz/latticeboltzmann-python
**Status:** GPL-3.0, pushed 2025. Checked: README, latticeboltzmann.py header.
**Principle:** the lattice Boltzmann method: simulate fluid with particle distributions hopping on a lattice, not with the Navier-Stokes equations directly.
**Mechanism (literature, D2Q9 shown):** nine distribution values f_i per cell, one per lattice direction. Each step: stream (shift each f_i along its direction), then collide: relax toward equilibrium f_eq = w_i·rho·(1 + 3 c_i·u + 4.5 (c_i·u)² − 1.5 u²) with rate 1/tau; density and velocity are moments of f. Obstacles bounce distributions back. The example is flow past a cylinder.
**Use it when:** complex boundaries, simple code that parallelizes well.

### Finite Volume Python — pmocz/finitevolume-python
**Status:** GPL-3.0, pushed 2025. Checked: README, finitevolume.py header.
**Principle:** a finite volume solver for the compressible Euler equations, demonstrated on the Kelvin-Helmholtz instability.
**Mechanism (literature):** store cell averages of density, momentum and energy; reconstruct values at faces with slope limiting; compute flux through each face with an approximate Riemann solver; update each cell by the net flux; step in time with a CFL-limited step. Shear layers roll into vortices.
**Use it when:** shocks, gases, astrophysical-style flows.

### FiPy — usnistgov/fipy
**Status:** NIST terms of use (a US government work; GitHub shows no classification), pushed Oct 2026. Checked: README, LICENSE head, meshVariable.py.
**Idea:** write a PDE as a sum of terms (transient, diffusion, convection, source) and let the library discretize it by finite volume on a mesh and solve the sparse system. Good for phase fields, diffusion and materials models. Read the terms before reuse.

## Waves

### GodotOceanWaves — 2Retr0/GodotOceanWaves
**Status:** MIT, pushed 2025. Checked: README, an addon header.
**Principle:** ocean surface from the inverse Fourier transform of a directional wave spectrum.
**Mechanism (literature, Tessendorf):** for each wave vector k build a random complex amplitude scaled by a spectrum (Phillips or JONSWAP type) with wind direction; advance each in time by e^(i·omega·t) with the deep-water dispersion omega = sqrt(g·|k|); an inverse FFT gives the height field, and further FFTs give horizontal displacement (choppy waves) and normals. Several scales (cascades) cover large and small waves.
**Use it when:** oceans, lakes and any tiling wave surface.

### Meep — NanoComp/meep
**Status:** GPL-2.0, pushed Oct 2026. Checked: README, src/meepgeom.hpp.
**Principle:** FDTD electromagnetics: step Maxwell's equations on a grid.
**Mechanism (literature):** a staggered (Yee) grid holds E and H components half a cell and half a step apart; leapfrog updates of E from the curl of H and H from the curl of E; absorbing boundary layers. Scriptable in Python and Scheme; 1D, 2D, 3D and cylindrical coordinates; distributed memory.
**Use it when:** photonics, antennas, waveguides.

### SPECFEM2D — SPECFEM/specfem2d
**Status:** GPL-3.0, pushed Oct 2026. Checked: README, a CPML utility file.
**Principle:** the spectral-element method for seismic waves in acoustic, elastic, viscoelastic and poroelastic media, with adjoint calculations for waveform tomography.
**Mechanism (literature):** high-order polynomials on Gauss-Lobatto-Legendre points make the mass matrix diagonal, so time stepping is explicit and cheap; convolutional perfectly matched layers (CPML) absorb outgoing waves at the edges.

### Pink Trombone C++ — kaiidams/pinktrombone_cpp
**Status:** MIT, pushed 2024. Checked: README, csrc/noise.cpp.
**Principle:** a vocal tract synthesizer (a port of Neil Thapen's web instrument).
**Mechanism (literature):** a glottal source drives a one-dimensional waveguide of tube segments whose cross-section can be edited to shape vowels and consonants; noise shapes breath and fricatives (the port includes a gradient-noise implementation).
**Use it when:** speech and instrument synthesis from physical models.

### QMsolve — quantum-visualizations/qmsolve
**Status:** BSD-3-Clause, pushed 2025. Checked: README, time_dependent_solver/crank_nicolson.py.
**Principle:** solve the Schrodinger equation for one or two particles on a grid and visualize it.
**Mechanism:** discretize the Hamiltonian H = −hbar²/2m ∇² + V with finite differences into a sparse matrix; eigenstates come from a sparse eigen solver; time evolution uses Crank-Nicolson, (I + i·dt·H/2hbar)·psi(t+dt) = (I − i·dt·H/2hbar)·psi(t), which preserves the norm.
**Use it when:** teaching and exploring quantum states in 1D, 2D and 3D.

## Force fields and numerics

### d3-force — d3/d3-force
**Status:** ISC, pushed 2023. Checked: README, src/simulation.js.
**Principle:** a velocity Verlet simulation of particles under pluggable forces, used for network layout.
**Mechanism:** forces (links as springs, many-body repulsion computed with a Barnes-Hut quadtree, centering, collision) adjust velocities each tick; positions advance; a cooling parameter alpha decays toward a target so the system settles; velocity decay acts as friction. Initial positions follow a golden-angle spiral (the source sets the angle to pi·(3 − sqrt(5))), with a seeded linear congruential random generator.
**Use it when:** graphs, bubble clustering, collision-avoiding layouts.

### ngraph.forcelayout — anvaka/ngraph.forcelayout
**Status:** BSD-3-Clause, pushed Aug 2026. Checked: README, lib/createPhysicsSimulator.js.
**Idea:** force-directed layout in any dimension, with a quad tree (octree in 3D) approximating long-distance forces, and code generation that specializes the simulator to the dimension count for speed.

### Numeric.js — sloisel/numeric
**Status:** MIT-style license text (LICENSE read; GitHub shows no classification), pushed 2018. Checked: README, src/quadprog.js.
**Idea:** numerical analysis in the browser: linear algebra, quadratic programming (seen), and an adaptive Runge-Kutta ODE solver per its documentation (not read here). Old, but a compact reference for what a numeric toolkit needs.
