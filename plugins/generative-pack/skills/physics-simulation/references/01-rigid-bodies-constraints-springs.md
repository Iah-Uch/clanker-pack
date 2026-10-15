# Rigid bodies, constraints, springs and position-based dynamics

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published algorithm, not this project's code.

## Cross-cutting ideas

- **The physics pipeline:** integrate velocities, find potentially touching pairs (broad phase, usually a bounding-box tree or grid), compute exact contacts (narrow phase, GJK/EPA for convex shapes), solve constraints, integrate positions. Nearly every engine below is this loop.
- **Impulse-based solving:** treat contacts and joints as constraints and apply impulses sequentially, several iterations, until they agree.
- **Position-based dynamics (PBD):** skip forces; predict positions, then push positions to satisfy constraints, and derive velocity from the displacement. Simple, stable, and good for cloth, soft bodies and fluids.
- **Springs have exact solutions.** A damped spring can be evaluated in closed form, so it is stable at any time step, unlike naive force integration.
- **Substeps beat iterations.** Many small steps with few solver iterations is often better than few steps with many iterations.

## Rigid-body engines

### Box2D — erincatto/box2d
**Status:** MIT, 10k★, pushed Oct 2026. Checked: README features, math_functions.h.
**Principle:** the reference 2D game physics engine.
**Mechanism:** features listed: continuous collision detection (so fast objects do not tunnel), convex polygons, capsules, circles, segments and chains, sensors and contact events, ray and shape casts, and a "Soft Step" rigid body solver, a substepped solver with soft constraints (literature: the author's Solver2D write-up).
**Use it when:** 2D games and prototypes that need robust stacking.

### Matter.js — liabru/matter-js
**Status:** MIT, 18k★, pushed Sep 2026. Checked: README demo list, src/core/Matter.js.
**Idea:** 2D rigid bodies on the web with compound and concave bodies (concave SVG paths, terrain), constraints (Newton's cradle, wrecking ball, slingshot) and a plugin system. Easy to learn from.

### cannon.js — schteppe/cannon.js
**Status:** MIT, pushed 2023 (little recent activity). Checked: README, src/Cannon.js index.
**Idea:** a small 3D rigid body engine for the web: simple collision detection, several shapes, contacts with friction, and constraints.

### Bullet Physics — bulletphysics/bullet3
**Status:** zlib license except the Extras and third-party example folders (LICENSE head read; GitHub shows no classification), 15k★, pushed Oct 2026. Checked: README, b3ConvexHullComputer.cpp.
**Mechanism (literature):** a dynamic bounding-box tree for broad phase, GJK and EPA for convex narrow phase, a sequential-impulse solver. The README points users to PyBullet for robotics and machine learning.
**Use it when:** games, robotics simulation, ML environments.

### Jolt Physics — jrouwe/JoltPhysics
**Status:** MIT, 12k★, pushed Oct 2026. Checked: README, Jolt/Geometry/GJKClosestPoint.h.
**Principle:** a multi-core-friendly rigid body and collision library, used in shipped AAA games.
**Mechanism:** the geometry layer contains a GJK closest-point routine (support-function based distance between convex shapes) that the narrow phase builds on.
**Use it when:** many bodies with multithreading, VR and games.

### PhysX — NVIDIA-Omniverse/PhysX
**Status:** BSD-3-Clause, pushed Oct 2026. Checked: README, a snippet file.
**Idea:** the industry SDK; its snippets show a capture format (OmniPVD) that records every geometry type for a viewer, a useful pattern for debugging physics.

### Rapier — dimforge/rapier
**Status:** Apache-2.0, pushed Oct 2026. Checked: README, crates/rapier3d-urdf/src/lib.rs.
**Idea:** 2D and 3D engines in Rust (including f64 variants), with impulse joints and multibody joints, and a URDF loader so robot descriptions load directly.

### MuJoCo — google-deepmind/mujoco
**Status:** Apache-2.0, pushed Oct 2026. Checked: README, python/mujoco/sysid trajectory module.
**Principle:** fast, accurate simulation of articulated bodies with contact, for robotics, biomechanics and learning.
**Mechanism (literature):** generalized coordinates and soft contact solved as a convex optimization problem. The Python package includes rollouts and a system-identification toolkit that fits model parameters to recorded trajectories.
**Use it when:** control and reinforcement learning research.

### Simbody — simbody/simbody
**Status:** Apache-2.0, pushed Oct 2026. Checked: README, SimbodyMainpage.h.
**Principle:** science-grade multibody dynamics for skeletons, robots and vehicles.
**Mechanism (literature):** generalized coordinates with recursive articulated-body algorithms, so cost grows linearly with the number of joints.

### myPhysicsLab — myphysicslab/myphysicslab
**Status:** Apache-2.0, pushed 2024. Checked: README, src/sims/springs/MoleculeSim.ts.
**Idea:** simulation classes built on an ODE-solver interface and a collision interface, with the math derived on its website. A good reference when you need to derive the equations of motion yourself.

## Position-based and spring dynamics

### PositionBasedDynamics — InteractiveComputerGraphics/PositionBasedDynamics
**Status:** MIT, pushed Sep 2026. Checked: README, MathFunctions.cpp.
**Principle:** simulate rigid bodies, deformable solids and fluids by projecting positions onto constraints.
**Mechanism (literature):** predict x* = x + dt·v + dt²·a. For each constraint C(x) = 0, move the involved particles along the constraint gradient: dx_i = −lambda·w_i·grad_i C, lambda = C / sum_j (w_j·|grad_j C|²), with w the inverse mass. Repeat for a few iterations, then set v = (x_new − x_old)/dt.
**Use it when:** cloth, ropes, soft bodies, interactive effects.

### Ten Minute Physics (PBD tutorials) — matthias-research/pages
**Status:** no repository license; the files I saw carry an MIT-style permission notice, check per file. Pushed Oct 2026. Checked: one tutorial script header (GPU cloth).
**Idea:** short, runnable demos of position-based methods (including cloth on the GPU) that teach by minimal code.

### Spring-It-On — orangeduck/Spring-It-On
**Status:** MIT, pushed Mar 2026. Checked: README, timedspring.c.
**Principle:** exact spring-damper formulas for character and camera motion, stable at any frame time.
**Mechanism (literature, the accompanying article):** parameterize a damped spring by its half-life (the time to close half the distance) instead of stiffness and damping, and evaluate the exact solution each frame; there are variants that reach a goal at a specified time (the source has a timed spring function) and variants that track a target velocity.
**Use it when:** smoothing, follow cameras, animation blending.

## Cellular physics

### The Powder Toy — The-Powder-Toy/The-Powder-Toy
**Status:** GPL-3.0, 5k★, pushed Oct 2026. Checked: README only.
**Idea:** a falling-sand sandbox where particles with material properties interact, coupled with simulated air pressure and velocity, and heat. Shows how a cellular automaton can host many "elements" through lookup tables of reactions. Copyleft: study the ideas.
