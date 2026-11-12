For “almost any browser 3D,” start with **Three.js (MIT)**. It has a scene graph, WebGL/WebGPU rendering, and a large example and community ecosystem. MIT permits commercial use; keep its license and notices with distributions.

If your product uses React, choose **React Three Fiber (MIT)** for declarative scene composition. It uses Three.js underneath, so Three.js knowledge still applies.

Consider **Babylon.js (Apache-2.0)** if you want a fuller engine with built-in tools for games and interactive apps. It also allows commercial use; preserve notices and review Apache’s patent terms.

For custom shaders or GPU effects without a scene graph, **regl (MIT)** is a smaller, lower-level option.

Avoid copying code from projects with no confirmed license. Before shipping, check the exact versions and licenses of dependencies, plugins, and assets; their terms can differ from the main library.