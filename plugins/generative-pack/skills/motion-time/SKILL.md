---
name: motion-time
description: Use when designing or building animation, motion, easing, interpolation, shape morphing, procedural or IK animation, spline following, programmatic video, crowd movement, object tracking, or live-coded timing, and a vetted open-source tool or a transferable technique would beat inventing it. Gives per-project techniques, licenses and when to reach for each.
---

# Motion and time

Reference for time-based techniques: how values move, how shapes change, how characters and crowds are driven, and how animation becomes video or sound. Each entry names a real open-source project, what technique it embodies, when to use it, and how to lift the idea without the library.

Facts about each project (license, last push, what it does) were checked against its GitHub repo and README on 2026-10-15. Lines marked "idea" are synthesis, not claims the project makes.

## Read this first

- **These are not drop-in solutions.** A project is an example of a technique. Abstract the idea, adapt it, combine it with others. Recommend a project only when it fits the user's stack, license and constraints.
- **"Mechanism" lines are literature unless the entry says I read the code.** They give the formulas and steps so the technique can be rebuilt without the project. Check current docs before relying on a feature.
- For the general pattern behind pattern-as-function-of-time languages, see McLean's 2014 paper "Making Programming Languages to Dance to" rather than any project's source.

## Pick by goal

| You want | Read |
|---|---|
| A custom speed curve, a value blending between two states, a shape turning into another shape | `references/01-easing-and-interpolation.md` |
| To choose an animation library for a web or React app | `references/02-animation-engines.md` |
| To ship an animation a designer made in After Effects | `references/03-vector-animation-formats.md` |
| A creature, a chain, a camera or object following a curve, an auto-rigged character | `references/04-procedural-motion-and-rigging.md` |
| Explanatory or vector animation rendered from code, synced to narration | `references/05-programmatic-video.md` |
| Many agents moving without colliding, or following objects across video frames | `references/06-crowds-and-tracking.md` |
| Music or patterns where timing is the material | `references/07-live-coding-time.md` |
| An end-to-end recipe for AI-generated motion design | `references/08-recipes.md` |

## License rules for this skill

- MIT, BSD, ISC, Apache-2.0: you may adapt code with the notices kept. Check each entry's "Watch out".
- GPL, AGPL, LGPL: take the technique from the paper or docs and write your own code. Do not port the source.
- Tidal Cycles states that ports and projects using its source as a reference for algorithms or types are derivative works under the same license. Treat it as use-as-a-tool only.
- No code license stated (Mesh2Motion code): do not copy code. Its LICENSE file covers only the models, rigs and animations.
- A code license does not cover fonts, demo videos, models or data bundled with a project. Check those separately.

## Maintenance flags

- Flubber: last push Nov 2022.
- d3-ease, d3-interpolate: last push Oct 2023, small and stable by design.
- animal-proc-anim, ByteTrack: last push 2024.
- Tidal Cycles: the GitHub repo is archived; development moved to Codeberg.

## How to answer with this

1. Match the goal to a reference above and read only that file.
2. Offer the tool and the transferable idea. Say which one you would pick and why.
3. State the license and any maintenance flag before recommending code reuse.
4. Do not claim a project supports a feature its entry does not list. Check its docs first.
