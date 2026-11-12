For 2D stacking, start with a physics engine that supports rigid bodies, collision detection, and contact solving. **Box2D** is a strong default for prototypes and commercial games; it uses the **MIT License**, which permits commercial use with attribution and license notice. **Chipmunk2D** is another mature option, also **MIT-licensed**.

If you need deterministic stacking across platforms or rollback networking, test the engine carefully: floating-point physics can vary. Consider a fixed-point engine such as **Velcro Physics** only after checking its current maintenance and license; projects and terms change, so verify before adopting.

For game-specific needs, tune solver iterations, collision shapes, friction, and sleep thresholds, and test tall stacks under your actual frame rates. Avoid implementing a solver from scratch unless you need unusual behavior or can invest in stability testing.

Licenses can change by release or repository, so confirm the exact version’s license file and preserve its notices in your distribution.