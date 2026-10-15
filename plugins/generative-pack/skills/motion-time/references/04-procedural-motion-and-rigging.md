# Procedural motion and rigging

Verified against each repo on 2026-10-15.

## Principle

Drive motion from a rule or a solver instead of keyframes. A small chain simulation or a solver gives lifelike results that react to input.

## animal-proc-anim (argonautcode/animal-proc-anim)

- License and status: MIT, 712 stars, last push Jul 2024. README is short; an explanatory video is linked.
- Technique: procedural animation of a fish, a snake and a lizard, using a 2D chain simulation as the rig.
- Reach for it when: you want creatures that move without authored animation.
- Mechanism (literature; the README is short and I did not read the source): the head moves toward the target; for each following joint i, set direction d = normalize(p_i − p_(i−1)) and place p_i = p_(i−1) + d·L, where L is the fixed distance to the previous joint; limit the angle between consecutive segments to a maximum bend; draw the body as an outline made by offsetting each joint perpendicular to the chain by a per-joint radius. Legs use a target that steps when it falls too far from the body.
- Idea: a head that follows a target, with each following segment constrained to a fixed distance and angle from the previous one, produces body motion without keyframes.

## fullik / FABRIK (lo-th/fullik)

- License and status: MIT, 474 stars, last push May 2025.
- Technique: a fast iterative inverse-kinematics solver for three.js, a conversion from the Java Caliko library, which implements the FABRIK algorithm by Dr. Andreas Aristidou. It exposes bones, chains, structures and angle constraints.
- Reach for it when: a chain (arm, tentacle, rope) must reach a target in 3D.
- Mechanism (literature, FABRIK, Aristidou and Lasenby): joints p_0 (root) to p_n (end effector), bone lengths d_i. If the target is farther than the sum of the d_i, stretch the chain straight toward it. Otherwise repeat until |p_n − target| is below a tolerance: backward pass: set p_n = target, then for i = n−1 down to 0 set p_i = p_(i+1) + normalize(p_i − p_(i+1))·d_i; forward pass: set p_0 back to the root, then for i = 0 to n−1 set p_(i+1) = p_i + normalize(p_(i+1) − p_i)·d_i. Joint limits project each direction into an allowed cone after each step. Each iteration costs O(n) and typically converges in a few passes.
- Idea: iterative solvers trade exactness for speed and stability, and handle joint limits easily.
- Watch out: the package was renamed to FIK; older examples use `Fullik.*` names.

## TwistSpline (blurstudio/TwistSpline)

- License and status: MIT, 112 stars, last push Jan 2025.
- Technique: a Bezier spline that smoothly reparameterizes while also interpolating orientations (twist), with controls that can be pinned to values. A header-only C++ template library, with a Maya plugin as the reference implementation.
- Reach for it when: you need a rig or camera path whose orientation, not just position, interpolates smoothly.
- Mechanism (literature; I did not read the code): position follows a cubic Bezier B(t) = (1−t)³P0 + 3(1−t)²t·P1 + 3(1−t)t²·P2 + t³P3. Orientation needs a frame along the curve: the Frenet frame flips at inflection points, so use a rotation-minimizing frame (propagate the previous frame with the smallest rotation to the new tangent, for example the double-reflection method) and add a separately interpolated twist angle on top.
- Idea: treat orientation along a curve as its own interpolated channel next to position.
- Watch out: built for Maya (2022 and later per its README).

## UnityBezierSolution (yasirkula/UnityBezierSolution)

- License and status: MIT, 1.5k stars, last push May 2025.
- Technique: Bezier splines in Unity, editable in the editor or built at runtime, with helpers such as travelling a spline at constant speed or constant time. Built on Catlike Coding's spline tutorial.
- Reach for it when: an object must follow an authored path at a controlled speed.
- Mechanism (literature): sample the curve at N parameter values, accumulate chord lengths into a table s_k; to move at speed v for time T, look up the parameter whose accumulated length equals v·T by binary search and interpolate between table rows. Constant time per segment is simpler but speeds up on long segments.
- Idea: constant speed along a curve needs arc-length parameterization; spline parameter alone does not move at constant speed.

## Mesh2Motion (Mesh2Motion/mesh2motion-app)

- License and status: GitHub reports no classification, 3.5k stars, last push Oct 2026. The LICENSE file only dedicates the models, blend files, rigs and animations to CC0; it states no code license.
- Technique: a web app that imports a GLB/GLTF 3D model, lets you pick and fit a skeleton type, previews bundled animations, and exports the result as GLB/GLTF. Positioned as a flexible, open alternative to Mixamo.
- Reach for it when: you need to quickly rig a static model and apply stock animations.
- Mechanism (literature; I did not read its code): skinned animation uses linear blend skinning: each vertex v moves to v' = sum over bones i of w_i · (B_i · inverse(R_i)) · v, where R_i is the bone's rest transform, B_i its current transform, and the weights w_i sum to 1. Fitting a skeleton means placing the rest transforms inside the mesh and computing weights, for example from distances or heat diffusion.
- Idea: separate the skeleton fitting step from the animation library, so one animation set serves many models.
- Watch out: do not copy its code; the bundled assets are CC0.
