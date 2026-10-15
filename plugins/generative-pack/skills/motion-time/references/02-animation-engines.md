# Animation engines for the web

Verified against each repo on 2026-10-15.

## Choosing

| Need | Pick |
|---|---|
| React or Vue app, gestures, layout transitions, scroll-linked effects | Motion |
| Framework-free animation of CSS, SVG, DOM attributes and plain objects | Anime.js |
| React app where motion should feel physical and interruptible | React Spring |
| Smallest possible tween core, you drive the loop | Tween.js (see 01) |

## Motion (motiondivision/motion)

- License and status: MIT, last push Oct 2026, 34k stars. Framer Motion is now Motion; import from `motion/react`.
- Technique: a hybrid engine that combines JavaScript with native browser animation APIs for GPU-accelerated animation. Batteries included: gestures, springs, layout transitions, scroll-linked effects, timelines. Packages for React, vanilla JavaScript and Vue.
- Reach for it when: the app is React or Vue and needs more than simple tweens.
- Mechanism (literature): a spring is the ODE m·x'' = −k(x − target) − c·x'. With natural frequency w0 = sqrt(k/m) and damping ratio z = c / (2·sqrt(k·m)): z < 1 oscillates (underdamped), z = 1 is critical, z > 1 creeps (overdamped). The underdamped solution is x(t) = target − e^(−z·w0·t)·(A·cos(wd·t) + B·sin(wd·t)) with wd = w0·sqrt(1 − z²), where A and B come from the initial offset and velocity. An engine can evaluate the closed form for any t, which is exact at any frame rate; Motion's docs describe spring and duration-based configurations.
- Idea: let the browser run what it can natively and fall back to JavaScript only where needed.
- Watch out: the project also sells "Motion+" (premium APIs, examples, editor); the open-source library itself is MIT. It publishes a free, MIT-licensed agent skill (`npx motion-ai`) and a free docs MCP server, which are candidates to install directly instead of rewriting.

## Anime.js (juliangarnier/anime)

- License and status: MIT, last push Aug 2026, 73k stars.
- Technique: a lightweight engine that animates CSS properties, SVG, DOM attributes and JavaScript objects with one API. Version 4 uses ES modules (`animate`, `stagger`).
- Reach for it when: you want staggered, looping, sequenced animation without a framework.
- Mechanism (literature): a stagger gives item i the start delay i·step; "from center" uses |i − center|·step, and on a grid the Euclidean or Manhattan distance from an origin cell. Timelines place animations at absolute or relative offsets on one clock, so scrubbing is just setting that clock.
- Idea: staggering is a function of index (and origin, such as from the center) that returns a delay. It generalizes to any per-item parameter.
- Watch out: the v3 to v4 migration changed the API; check which version an example uses.

## React Spring (pmndrs/react-spring)

- License and status: MIT, last push Oct 2026, 29k stars.
- Technique: spring physics first. Animations are springs by default for fluid interactivity; durations with easings are supported too. Works with react-dom and react-three-fiber, declaratively or imperatively.
- Reach for it when: interactions get interrupted mid-animation and should stay smooth.
- Mechanism (literature): integrate the spring ODE numerically each frame: a = (−k(x − target) − c·v) / m, then v += a·dt and x += v·dt (semi-implicit Euler, stable for moderate stiffness; sub-step when dt is large). The animation is done when both |v| and |x − target| fall below a precision threshold. Because the state includes velocity, changing the target mid-flight just changes the force.
- Idea (general property of springs): a spring carries velocity, so retargeting mid-flight continues smoothly, where a fixed-duration tween restarts from a standstill.
- Watch out: web and three.js use different packages (`@react-spring/web`, `@react-spring/three`).
