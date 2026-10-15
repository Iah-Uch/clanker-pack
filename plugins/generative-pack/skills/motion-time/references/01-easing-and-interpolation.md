# Easing and interpolation

Verified against each repo on 2026-10-15.

## Principle

Easing distorts time so motion reads as natural; interpolation blends between two values. Keep them separate: one function maps time to progress, another maps progress to a value. Swapping either does not touch the other.

## bezier-easing (gre/bezier-easing)

- License and status: MIT, last push Oct 2026, 1.8k stars.
- Technique: a cubic Bezier curve defined by four numbers maps normalized time to progress, exactly like CSS `cubic-bezier(...)`. The hard part is projecting x onto the curve; it uses fast heuristics (bisection, Newton-Raphson, sampling) for speed and precision.
- Reach for it when: you need CSS-style easing in canvas, WebGL, game loops, or any code outside CSS.
- Mechanism (literature): the curve runs from (0,0) to (1,1) with control points (x1,y1) and (x2,y2); for parameter s, x(s) = 3(1−s)²·s·x1 + 3(1−s)·s²·x2 + s³ and y(s) the same with y1 and y2. To ease time t, solve x(s) = t for s (Newton-Raphson using the derivative x'(s), with bisection as a fallback where the slope is near zero) and return y(s).
- Idea: store easing as four numbers, not as code. A design tool, a config file and the runtime can all share the same curve.
- Watch out: x is clamped to 0..1.

## d3-ease (d3/d3-ease)

- License and status: BSD-3-Clause, last push Oct 2023.
- Technique: named easing functions (slow-in, slow-out and relatives) as plain functions of time.
- Reach for it when: you want a library of standard curves with no animation engine attached.
- Mechanism (literature): the families are polynomials and their mirrors. Ease-in is f(t); ease-out is 1 − f(1 − t); ease-in-out is f(2t)/2 on the first half and 1 − f(2(1 − t))/2 on the second. With f(t) = t³ you get the cubic family; sine uses 1 − cos(πt/2); exponential uses 2^(10(t−1)); back overshoots with f(t) = t²((s+1)t − s); bounce stitches parabolas.
- Idea: an easing is just `t -> t'`. You can compose them, for example ease the time, then ease the result.

## d3-interpolate (d3/d3-interpolate)

- License and status: ISC, last push Oct 2023.
- Technique: interpolators for numbers, colors, strings, arrays, objects and nested objects.
- Reach for it when: you animate something that is not a plain number, such as colors or nested state.
- Mechanism (literature): numbers use a(1 − t) + b·t. Strings are split into numeric and non-numeric runs; the numbers are interpolated and the text between them is kept, which is how "10px 20px" becomes any intermediate string. Arrays and objects interpolate per element or key. Colors are blended per channel in the chosen space; interpolating in a perceptual space such as Lab or HCL avoids the muddy mid-tones of RGB.
- Idea: an interpolator is a function from 0..1 to a value. Build compound interpolators out of simple ones and the structure carries through.

## Flubber (veltman/flubber)

- License and status: MIT, 6.9k stars, last push Nov 2022 (unmaintained since).
- Technique: best-guess interpolation between arbitrary 2D shapes, including shapes that do not correspond point for point, where plain coordinate interpolation gives inversions and jumps. Inputs are an SVG path string or an array of `[x, y]` points; methods return interpolator functions.
- Reach for it when: morphing between unrelated SVG icons or outlines.
- Mechanism (literature, not read in the code): resample both outlines to the same number of points by splitting the longest segments; rotate the starting index of one outline to the offset that minimizes the sum of squared distances between paired points; then interpolate each pair linearly. Shapes with holes or several pieces need a triangulation step so pieces can be mapped to each other.
- Idea: when two shapes lack correspondence, create the correspondence first (resample and match points), then interpolate.
- Watch out: unmaintained; test with your actual shapes.

## Tween.js (tweenjs/tween.js)

- License and status: MIT (LICENSE read; GitHub shows no classification because of the extra easing-equation notice), last push Oct 2026, 10k stars.
- Technique: a tween engine that animates plain JavaScript objects with Robert Penner's easing equations; you drive it by calling `update(time)` each frame.
- Reach for it when: you want the smallest tween core, usually in canvas or three.js work.
- Mechanism (literature): each frame, progress = clamp((now − start) / duration, 0, 1); every animated property becomes start + (end − start)·easing(progress). The engine only holds the start values, the end values, and the easing function; chaining and repeating are bookkeeping on start times.
- Idea: animate a plain state object and render from it. The renderer never knows about the animation.
- Watch out: you own the animation loop.
