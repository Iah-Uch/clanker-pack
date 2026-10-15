# Generative models: diffusion, flow matching, video, audio, speech and music

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published method, not this project's code. **Code license and weights license are separate things**: for every model, read the model card on the hub before shipping.

## Cross-cutting ideas

- **Diffusion = learn to denoise.** Forward: x_t = sqrt(a_t)·x_0 + sqrt(1 − a_t)·eps, with a_t decreasing from 1 to about 0 (the noise schedule). A network predicts the noise eps (or x_0, or a velocity v) from x_t and t. Sampling starts from pure noise and applies the network repeatedly; the **scheduler** (DDPM, DDIM, DPM-Solver, UniPC) decides the step sequence, and fewer steps trade quality for speed.
- **Flow matching.** Learn a velocity field v(x, t) that carries noise to data along straight-ish paths: with x_t = (1 − t)·x_0 + t·x_1, the regression target is x_1 − x_0, and sampling integrates dx/dt = v with an ODE solver. Simulation-free training, simple loss, fewer steps.
- **Latent diffusion.** Compress with an autoencoder (VAE) first, run diffusion in the small latent space, decode at the end. Video and audio models use the same trick with spatiotemporal compression.
- **Conditioning.** Text (a T5 or CLIP embedding injected by cross-attention or concatenation), images (as extra channels or tokens), keyframes, LoRA adapters for style. **Classifier-free guidance:** eps = eps_uncond + w·(eps_cond − eps_uncond), with w around 3 to 8; larger w follows the prompt harder and reduces diversity.
- **Transformers over patches (DiT).** Cut the latent into patches, treat them as tokens, apply attention; scales better than convolutional U-Nets.
- **Memory tricks.** Half precision, attention slicing, CPU offload and quantization make large models fit consumer GPUs; they change speed, not the method.

## Frameworks

### Diffusers — huggingface/diffusers
**Status:** Apache-2.0, about 35k stars, pushed Oct 2026. Checked: README, src/diffusers/training_utils.py head.
**Idea:** the modular split is the lesson: a **pipeline** wires a text encoder, a denoiser model (UNet or transformer), a **scheduler** and a VAE; each piece is swappable. The README's loop shows the whole algorithm: start from `torch.randn`, for each timestep call the model for the noisy residual, let `scheduler.step` produce the previous sample.
**Use it when:** you want to run, swap, fine-tune (LoRA) or study diffusion models without writing the sampler.
**Build it yourself:** the sampler is a loop of about ten lines around a scheduler; the effort is in the model.

### TorchCFM — atong01/conditional-flow-matching
**Status:** MIT, about 2.6k stars, pushed Jul 2026. Checked: README.
**Principle:** conditional flow matching: a simulation-free objective for continuous normalizing flows, closing the gap to diffusion.
**Mechanism:** sample a data point x_1 and a noise (or source) point x_0, a time t, form x_t on the interpolation path, and regress the network onto the path velocity (x_1 − x_0 for linear paths). Variants pair x_0 and x_1 by optimal transport so paths do not cross, and the library applies it to images, single-cell dynamics and tabular data.
**Use it when:** a small, clear codebase to learn or prototype flow-based generation on your own data.

## Video

### CogVideoX — zai-org/CogVideo
**Status:** code Apache-2.0, about 13k stars, pushed Nov 2025. Checked: README, tools/load_cogvideox_lora.py. The README says the 2B model moved to Apache-2.0 and has a separate Model-License section for other weights; read it.
**Principle:** a transformer-based text-and-image-to-video diffusion model.
**Mechanism (literature):** a 3D causal VAE compresses video in space and time; an expert transformer processes text and video tokens together; the repo ships DDIM and DPM schedulers, DDIM inversion (run the sampler backward to recover noise for editing), and LoRA fine-tuning.
**Use it when:** generating short clips, fine-tuning a style with LoRA on one GPU.

### Wan 2.2 — Wan-Video/Wan2.2
**Status:** Apache-2.0, about 18k stars, pushed Sep 2026. Checked: README, wan/utils/fm_solvers_unipc.py.
**Principle:** mixture-of-experts diffusion for video.
**Mechanism:** separate expert models handle different noise levels (a high-noise expert lays out structure, a low-noise expert refines detail), so capacity grows while compute per step stays the same; a VAE with 16×16×4 compression allows a 5B model to produce 720p at 24 fps on one consumer GPU. The solver file is a flow-matching UniPC multistep scheduler: a predictor-corrector ODE solver for fast sampling.
**Use it when:** text-to-video and image-to-video with strong motion; reading a flow-matching solver.

### LTX-Video — Lightricks/LTX-Video
**Status:** Apache-2.0, about 11k stars, pushed Jan 2026. Checked: README, ltx_video/inference.py head.
**Principle:** a DiT video model with a causal video autoencoder and a symmetric patchifier, supporting multiple keyframes, extension in both directions and video-to-video.
**Mechanism:** conditioning items attach given frames at chosen positions, the T5 text encoder drives the transformer, and a latent upsampler enables multiscale pipelines. The README now points to LTX-2 (joint audio and video).
**Use it when:** fast, controllable video generation with keyframes.

## Audio, speech and music

### Stable Audio Tools — Stability-AI/stable-audio-tools
**Status:** code MIT, about 3.9k stars, pushed Oct 2026. Checked: README, training/factory.py. The pretrained model needs you to accept its terms on the hub.
**Idea:** a config-driven trainer: a model config names a `model_type` (autoencoder, diffusion, conditioned diffusion) and a training wrapper is built from it, so one codebase trains the audio autoencoder and the diffusion model on top of its latents.

### ACE-Step — ace-step/ACE-Step
**Status:** Apache-2.0, about 4.9k stars, pushed Feb 2026. Checked: README, acestep/text2music_dataset.py.
**Principle:** fast long-form music generation by combining diffusion with a deep-compression autoencoder and a lightweight linear transformer.
**Mechanism:** semantic alignment (REPA) with pretrained music and speech encoders (MERT, mHuBERT) during training speeds convergence; the model supports lyric editing, remixing, voice cloning and track generation; the dataset code drops near-silent clips (a threshold on the fraction of silent samples).
**Use it when:** song generation with lyrics; ideas for data hygiene in audio training.

### Qwen3-TTS — QwenLM/Qwen3-TTS
**Status:** Apache-2.0, about 14k stars, pushed Mar 2026. Checked: README.
**Idea:** a speech-generation family built on a 12 Hz speech tokenizer, supporting voice cloning from a short sample, voice design from a text description, and natural-language control of style.
**Mechanism (literature):** audio is turned into discrete tokens at a low frame rate, a language model predicts the tokens conditioned on text and a speaker prompt, a decoder turns tokens back into a waveform.

### DDSP — magenta/ddsp
**Status:** Apache-2.0, about 3.4k stars, pushed Oct 2026. Checked: README.
**Principle:** put classic signal-processing blocks inside a neural network as differentiable layers.
**Mechanism (literature):** a network predicts the controls (fundamental frequency, loudness, harmonic amplitudes, noise filter) and fixed differentiable modules render sound: an additive harmonic oscillator bank, y(t) = sum_k A_k(t)·sin(k·phi(t)) with phi the integral of 2·pi·f0, plus filtered noise and a reverb; training uses a multi-scale spectral loss. Gives small, interpretable models and timbre transfer.
**Use it when:** instrument modeling with little data; any task where the structure of the signal is known.

### Magenta — magenta/magenta
**Status:** Apache-2.0, about 20k stars, pushed Jan 2026; the README says the repository is archived and kept as supplement to papers. Checked: README.
**Idea:** a research collection for music and art generation with machine learning; browse for historical models and the browser port (Magenta.js).

### MT3 — magenta/mt3
**Status:** Apache-2.0, about 1.8k stars, pushed Oct 2026. Checked: README.
**Principle:** multi-instrument music transcription as sequence-to-sequence translation.
**Mechanism (literature):** a T5 transformer reads spectrogram frames and emits a token stream of note events (program, onset time, pitch, velocity); one model handles many instruments by emitting the instrument as a token. Training is not made easy by the repo; use the checkpoints.

### Whisper — openai/whisper
**Status:** MIT for code and weights (the README says so), about 110k stars, pushed Aug 2026. Checked: README.
**Principle:** robust speech recognition from large weakly supervised training.
**Mechanism (literature):** log-Mel spectrogram of a 30-second window goes through an encoder-decoder transformer; special tokens select task (transcribe or translate), language and timestamps, so one model does multilingual recognition, translation and language ID.
**Use it when:** transcription and subtitles. Cost note: run locally, it is free; hosted APIs are paid.
