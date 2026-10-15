# Audio, shader and GPU tools, and creative applications

A catalog of ideas. The projects are examples, not drop-in solutions. "Checked" says what I read; "literature" marks general knowledge of the technique, not this project's code.

## Cross-cutting ideas

- **Describe the signal flow, let a compiler produce the loop.** Audio DSP and GPU kernels are both "a small function applied to many samples or elements", and both benefit from a language that makes the dataflow explicit and compiles it to tight code (Faust, Taichi).
- **Client and server split.** SuperCollider separates a real-time synthesis server from a control language that sends it messages, so a crash or a slow script never glitches the audio.
- **Fast feedback loops.** A shader sandbox that watches the file and re-runs on save (glslViewer) turns shader work into a live conversation.
- **Graphs as programs.** ComfyUI represents a generative pipeline as a node graph that is also a serialized, replayable, shareable file.
- **Local models.** Heavy generative models can run on the user's machine behind a small server; the application is a UI plus job queue.

## Audio and shader languages

### Faust — grame-cncm/faust
**Status:** LGPL-2.1 or later for the compiler (stated in the license head; GitHub shows no classification, and libraries and architecture files carry their own notices, so read the file you reuse). About 3.2k stars, pushed Oct 2026. Checked: README, license head, embedded/faustgen sources.
**Principle:** a functional language for signal processing that is compiled, not interpreted.
**Mechanism:** a program is a block diagram built from composition operators: `:` sequential, `,` parallel, `<:` split, `:>` merge, `~` feedback with an implicit one-sample delay. The compiler lowers it to sample-level code and emits C++, C, Rust, WebAssembly, LLVM IR and others, wrapped in an "architecture" file that adds the plugin, standalone or web shell. Example: a one-pole lowpass is `process = + ~ *(a)` style feedback. Embedded tools such as `faustgen~` for Max compile Faust at runtime.
**Use it when:** writing effects and synths once and shipping them as plugins, web audio and embedded firmware.
**Pitfalls:** feedback needs at least one delay; the block-diagram thinking takes a day to learn.

### SuperCollider — supercollider/supercollider
**Status:** GPL-3.0, about 6.8k stars, pushed 2026. Checked: README.
**Principle:** an audio server (scsynth), a language (sclang) and an IDE.
**Mechanism (literature):** sclang compiles a `SynthDef`, a graph of unit generators (oscillators, filters, envelopes), and sends it to scsynth over OSC; scsynth runs a tree of synth nodes processed in blocks (typically 64 samples), with control-rate and audio-rate signals; patterns schedule events on a clock.
**Use it when:** algorithmic composition, live coding, research-grade synthesis.
**Pitfalls:** copyleft: take the architecture (server plus OSC plus synth graph), not code.

### glslViewer — patriciogonzalezvivo/glslViewer
**Status:** BSD-3-Clause, about 5.3k stars, pushed 2026. Checked: README.
**Principle:** a console GLSL sandbox: point it at a fragment or vertex shader file, it renders and reloads on save.
**Mechanism:** the viewer supplies standard uniforms (time, resolution, mouse, textures) and a command line to set more; shaders can include other files; output can be saved as images or frames.
**Use it when:** shader prototyping without a web page, scripted frame export, a teaching setup.

### Taichi — taichi-dev/taichi
**Status:** Apache-2.0, about 28k stars, pushed Oct 2026. Checked: README.
**Principle:** write parallel kernels in Python syntax, compile them to GPU or CPU.
**Mechanism:** a `@ti.kernel` function is traced at call time and compiled through an intermediate representation to CUDA, Vulkan, Metal, OpenGL or CPU back ends; the outermost loops are parallelized automatically; data lives in `ti.field` layouts, which can be sparse (hierarchical, pointer and bitmasked nodes); autodiff builds a tape of kernel invocations for gradients (differentiable simulation).
**Use it when:** particle, fluid and cloth simulations, image kernels and optimization in Python at GPU speed.
**Pitfalls:** only the code inside kernels is compiled; Python objects and recursion are limited there.

## Applications worth knowing as techniques

### Blender — blender/blender
**Status:** GPL (the license file states Blender is available only under the GNU GPL; GitHub shows no classification). Checked: license text.
**Idea:** a full DCC suite with a Python API (`bpy`) that exposes almost every operation, node-based shaders and procedural Geometry Nodes, headless rendering from the command line. As a tool, script it freely: scripts written against the API are your own. As code, copyleft: take ideas only.

### Goxel — guillaumechereau/goxel
**Status:** GPL-3.0, about 3.2k stars, pushed 2026. Checked: README.
**Idea:** a voxel editor: a sparse grid of colored cubes edited with tools, rendered with a simple lit shader, exported to formats such as OBJ and glTF. Useful as a model of a minimal editor.

### ComfyUI — Comfy-Org/ComfyUI
**Status:** GPL-3.0, about 137k stars, pushed 2026. Checked: README.
**Principle:** a diffusion-model backend and GUI where a pipeline is a node graph.
**Mechanism (literature):** nodes are functions with typed inputs and outputs; the server walks the graph from the outputs back, executes only nodes whose inputs changed (cached otherwise), and exposes the same graph over an HTTP and WebSocket API, so a UI-built workflow can be driven as a service.
**Use it when:** reproducible image and video generation pipelines, batch jobs, an app that needs a swappable model backend.

### VoiceStudio — debpalash/VoiceStudio
**Status:** AGPL-3.0, about 68k stars, pushed Oct 2026. Checked: README.
**Idea:** a local-first application for voice cloning, text-to-speech and dubbing with models running on the user's machine. AGPL: network use triggers the source-sharing obligation; take the architecture, not the code, for a proprietary service.

### v86 — copy/v86
**Status:** BSD-2-Clause, about 23.5k stars, pushed 2026. Checked: README.
**Principle:** an x86 PC emulator in the browser.
**Mechanism (literature):** a CPU interpreter plus a just-in-time compiler that translates hot x86 basic blocks into WebAssembly modules, with emulated devices (disk, VGA, network) around it.
**Use it when:** running old software or a Linux in a web page; a model of dynamic binary translation.

### DIY NAS — hyun2xyz/DIY_nas
**Status:** MIT, 1 star. Not a creative or generative technique, and the repository is a template for a personal NAS build. Left out of the technique set; listed so the ledger is complete.
