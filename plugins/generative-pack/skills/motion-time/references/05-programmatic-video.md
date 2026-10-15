# Programmatic video

Verified against each repo on 2026-10-15.

## Principle

Describe the animation in code, render frames deterministically, then encode. The same source can be re-rendered at any resolution or edited by changing text.

## ManimGL (3b1b/manim)

- License and status: MIT, 95k stars, last push Sep 2026.
- Technique: an engine for precise programmatic animation, built for explanatory math videos. A scene is a Python class: create objects, then call play.
- Reach for it when: you need exact, equation-driven or geometry-driven animation.
- Mechanism (literature; I did not read the source): an animation has a run time; each frame computes alpha = rate_func(elapsed / run_time) and calls interpolate(alpha) on the mobjects; a Transform linearly interpolates the points of two shapes after padding them to the same number of points. Frames are rendered and piped to FFmpeg, so the output is deterministic.
- Idea: model each video as scene classes with named steps, so edits are text diffs.
- Watch out: there are two versions. This repo is ManimGL (package `manimgl`, not `manim`); the community edition is a separate fork (`ManimCommunity/manim`) with different install instructions. ManimGL needs Python 3.10 or higher, FFmpeg and OpenGL, and LaTeX if you use it.

## Motion Canvas (motion-canvas/motion-canvas)

- License and status: MIT, 19k stars, last push Jul 2026.
- Technique: a TypeScript library that uses generators to program animations, plus an editor with real-time preview. Designed for informative vector animations synchronized with voice-overs.
- Reach for it when: you want timeline-style animation written as sequential code, with a live preview.
- Mechanism (literature; the README describes generators): a scene is a generator function; each `yield` hands control back after one frame, and helpers such as `waitFor(seconds)` yield until enough frames have passed; because time advances only by frame count, rendering is deterministic and can run faster or slower than real time, and scrubbing replays the generator.
- Idea: generator functions turn "do this, wait, then do that" into straight-line code, which is easier to read than callbacks or timelines.
- Watch out: the repo is a monorepo (`core`, `2d`, `create` and others); use the `create` package to bootstrap.
