# Vector animation formats

Verified against each repo on 2026-10-15.

## Principle

Treat an animation as data, not code. A designer authors it once; any runtime plays it.

## Lottie Web (airbnb/lottie-web)

- License and status: MIT, last push Sep 2025, 32k stars.
- Technique: parses After Effects animations exported as JSON through the Bodymovin plugin and renders them natively on the web. Sibling projects cover Android, iOS, React Native and Windows.
- Reach for it when: a designer builds the animation in After Effects and an engineer should ship it without recreating it by hand.
- Mechanism (literature, the Bodymovin JSON format): a composition has a frame rate, an in and out point, and a list of layers (shape, solid, image, precomposition, text). Each animatable property is either a static value or a list of keyframes holding a time, a start value and bezier handles for in and out easing; the player finds the two keyframes around the current time, remaps progress through the handle curve (the same cubic Bezier as CSS easing), and interpolates the value. Shape layers hold paths, fills, strokes and modifiers such as trim paths; transforms (anchor, position, scale, rotation, opacity) nest through parenting.
- Idea: separate authoring from playback with a JSON format. The same file feeds several platforms.
- Watch out: the exporter is the Bodymovin plugin for After Effects (CC 2014 and up per its README); check the docs for what the player supports before promising a design.

## Velato (linebender/velato)

- License and status: Apache-2.0, last push Sep 2026, 163 stars.
- Technique: a Rust library that parses and renders Lottie, with an optional built-in Vello integration, or your own renderer through the `RenderSink` trait.
- Reach for it when: you need Lottie in a native or GPU-rendered interactive graphics app.
- Mechanism: per frame, evaluate every property at the current time and emit drawing commands (fills, strokes, transforms, clips) to a sink; the sink is the only part that knows about the GPU. Evaluating properties and drawing are separate stages, so the same evaluated scene can feed any renderer.
- Idea: a parser plus a render-sink interface keeps the format independent from the renderer.
- Watch out: its README lists missing features (text, image embedding, advanced shapes, most layer effects) and a version table pinning which Vello release each Velato version needs.
