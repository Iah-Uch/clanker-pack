Use Box2D as the default for a commercial 2D game: it is purpose-built for this use, with collision detection and a solver designed for stable rigid-body contact and stacking. It is MIT licensed, so commercial use is allowed; include its copyright and license notice with distributions.

For browser-based prototypes, Matter.js is another MIT-licensed option. If your game uses Rust, consider Rapier, licensed Apache-2.0.

For robust stacking, use a fixed timestep, enable the engine’s substepping or solver features where available, and tune body mass, friction, and collision shapes. Test with your actual stack sizes and frame rates; solver settings and game scale affect stability.

Before shipping, confirm the license and notices for the exact version you bundle.