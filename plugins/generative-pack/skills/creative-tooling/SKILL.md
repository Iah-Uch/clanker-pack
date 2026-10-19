---
name: creative-tooling
description: "Use when choosing or designing the toolchain for creative and generative work: sketch frameworks (p5, canvas-sketch, openFrameworks, Cinder), 2D and 3D rendering libraries (PixiJS, Three.js, React Three Fiber, regl, Babylon.js, Vello), audio DSP languages (Faust, SuperCollider), shader sandboxes, GPU kernels in Python (Taichi), node-graph generation (ComfyUI), voxel and 3D editors, in-browser emulation. A catalog of designs and trade-offs to reason from, not a set of drop-in libraries."
---

# Creative tooling

A catalog of ideas drawn from about 22 open-source projects: how creative-coding frameworks, renderers, audio languages and generation pipelines are built, and what each trades away.

## Read this first

- **These are not drop-in solutions.** A project is an example of a design. Abstract the idea and adapt it. Recommend a tool only when it fits the user's stack, license and constraints.
- **Do not assume a library does what its name suggests.** Each entry says what I checked. Check current docs before relying on a feature.
- **Licenses matter when you reuse code.** MIT, BSD, Apache: adapt with notices. GPL, AGPL, LGPL: take the idea and write your own code (LGPL allows linking; modifying the library has obligations). "No license detected" (OGL): do not copy code.
- Facts were checked against each repository on 2026-10-15; projects change.

## Pick by goal

| You want | Read |
|---|---|
| A sketch framework, 2D or 3D rendering library, GPU command or scene-graph design, native toolkit | `references/01-frameworks-and-graphics-libraries.md` |
| Audio DSP language, synth server, shader sandbox, Python GPU kernels, node-graph generation, voxel and 3D editors, emulation | `references/02-audio-shaders-gpu-and-applications.md` |

## Ideas that recur

- Every framework is a loop with a canvas, a clock and input; they differ in how much state they hide.
- Retained scene graphs batch and diff; immediate mode is simpler and fine below a few thousand objects.
- Describe the draw or the signal flow declaratively and let a compiler or a state cache do the bookkeeping.
- Separate the real-time core from the control layer.

## How to answer with this

1. Match the goal to a reference and read only that file.
2. Compare two or three options by license, platform and what each hides; recommend one.
3. Never install anything without the user's consent.
