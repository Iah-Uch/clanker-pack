Use `bezier-easing` for CSS-style curves. Its cubic Bézier function maps normalized time to progress, matching `cubic-bezier(x1, y1, x2, y2)` and fitting canvas, WebGL, and game loops. It’s MIT licensed, so you can use and adapt it in a commercial product while retaining its license notice.

Keep easing separate from interpolation: easing transforms time into progress; interpolation maps progress to a value. For a library of named curves, consider `d3-ease` (BSD-3-Clause). For animating plain JavaScript objects with a tween loop you drive yourself, consider Tween.js (MIT).

The skill’s repository details were checked on 2026-10-15; verify current licenses and notices before shipping.