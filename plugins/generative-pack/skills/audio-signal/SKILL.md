---
name: audio-signal
description: Use when synthesizing, analyzing or encoding audio and other signals: oscillators, filters, envelopes, FM, effects, Web Audio scheduling, DSP libraries, FFT and spectrograms, MFCCs, onset and pitch detection, music information retrieval, images as audio (SSTV), time-frequency analysis of scientific signals, tomographic reconstruction. A catalog of techniques with mechanisms and formulas, to reason from, not a set of drop-in libraries.
---

# Audio and signal processing

A catalog of ideas drawn from about 12 open-source projects (plus pointers to SuperCollider and Faust in `creative-tooling`): how sound is synthesized and analyzed, and how spectral methods extend to other signals.

## Read this first

- **These are not drop-in solutions.** A project is an example of a technique. Abstract the idea and adapt it. Recommend a library only when it fits the user's platform and license.
- **Do not assume a library does what its name suggests.** Each entry says what I checked; "literature" marks the published technique rather than the project's code. Check current docs before relying on a feature.
- **Licenses matter when you reuse code.** MIT, ISC, BSD: adapt with notices. GPL, AGPL, LGPL (aubio, GWpy, ASTRA, Essentia, Csound): take the algorithm and write your own code, or link where the license allows. "No license detected" (fft.js): do not copy code.
- Facts were checked against each repository on 2026-10-15; projects change.

## Pick by goal

| You want | Read |
|---|---|
| Synthesis, filters, envelopes, effects, a Web Audio framework, a DSP library for embedded or plug-ins, images as sound | `references/01-synthesis-and-audio-frameworks.md` |
| Spectrograms, FFT, MFCC, onset and pitch detection, feature extraction, GPU FFT, scientific time-frequency analysis, tomography | `references/02-analysis-spectra-and-tomography.md` |

## Ideas that recur

- Everything is a loop over samples with a little state.
- Transform to the frequency domain when the problem is a convolution or a question about pitch and timbre.
- Window, overlap, then average: the standard recipe for stable spectra.
- Separate control rate from audio rate.
- Expose the forward operator and its transpose, and solve the inverse problem on top.

## How to answer with this

1. Match the goal to a reference and read only that file.
2. Explain the technique in terms of the user's signal; mention a project as an example with its license.
3. Give the formula and a minimal recipe; do not paste code from a copyleft or unlicensed project.
