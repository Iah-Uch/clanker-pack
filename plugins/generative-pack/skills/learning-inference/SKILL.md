---
name: learning-inference
description: Use when a task involves learned models for creative or perceptual work: diffusion and flow matching, video, music, speech and audio models, Gaussian splatting, NeRF and single-image 3D, monocular depth, segmentation and tracking, super-resolution, OCR, neural cellular automata, embeddings and UMAP, game self-play, robot learning, typed decision engines. A catalog of techniques with mechanisms and formulas, to reason from, not a set of drop-in libraries.
---

# Learning and inference

A catalog of ideas drawn from about 43 open-source projects: how generative, perceptual and decision models work, what they need, and how their code and weights are licensed.

## Read this first

- **These are not drop-in solutions.** A project is an example of a technique. Abstract the idea and adapt it. Recommend a model only when it fits the user's hardware, license and quality bar.
- **Do not assume a model does what its name suggests.** Each entry says what I checked; "literature" marks the published method rather than the project's code. Check the current README and model card before relying on a feature. I did not verify benchmark claims.
- **Code license and weights license are different.** Weights may be non-commercial, gated behind acceptance of terms, or custom (the SAM License). Always read the model card for the checkpoint you will run. Third-party components inside a repo can carry their own terms.
- **Licenses matter when you reuse code.** MIT, BSD, Apache: adapt with notices. AGPL (Ultralytics YOLO, OpenSplat): network use triggers source-sharing; take the technique, or buy the commercial license. Custom (KataGo, SAM): read the text.
- Facts were checked against each repository on 2026-10-15; projects change fast in this field.

## Pick by goal

| You want | Read |
|---|---|
| Image, video, music, speech or audio generation; diffusion and flow matching; transcription | `references/01-generative-models-image-video-audio.md` |
| 3D from photos or one image, Gaussian splatting, depth maps, relighting, layer decomposition, portrait animation | `references/02-3d-reconstruction-splatting-depth-animation.md` |
| Segmentation, tracking, hand landmarks, detection, upscaling, face restoration, OCR | `references/03-perception-restoration-ocr.md` |
| Language model basics, embeddings and UMAP, neural cellular automata, self-play, robot learning, typed decisions | `references/04-learning-foundations-embodied-decisions.md` |

## Ideas that recur

- Learn the inverse of a corruption (noise, blur, occlusion), then sample or apply it.
- Compress first (VAE, tokenizer, voxel latent), then model in the small space.
- Run the expensive encoder once and a light head per query (prompts, frames).
- Put known structure inside the model (differentiable oscillators, rasterizers, filters) to need less data.
- Train on synthetic degradation or in simulation, then transfer.
- Use a classifier over fixed options when you need a decision, not text.

## How to answer with this

1. Match the goal to a reference and read only that file.
2. Explain the technique in terms of the user's problem; name a project as an example with its code and weights licenses.
3. State hardware needs honestly (many models need a large GPU) and offer a hosted or lighter alternative where relevant.
4. Never download models or weights without the user's consent.
