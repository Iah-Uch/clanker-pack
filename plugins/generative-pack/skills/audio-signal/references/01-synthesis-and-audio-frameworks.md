# Synthesis, DSP libraries and audio frameworks

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published technique, not this project's code.

## Cross-cutting ideas

- **A sample-rate loop.** Audio is a stream of numbers at 44.1 or 48 kHz. Everything is a function from input samples (and state) to output samples, run once per sample or per block of 64 to 512.
- **Oscillators.** A phase accumulator: phase += 2·pi·f / fs, wrapped; output = waveform(phase). Naive saw and square waves alias (energy above fs/2 folds back), so band-limit them (PolyBLEP, wavetables) when the pitch is high.
- **Envelopes.** ADSR: attack, decay, sustain level, release; applied as a gain, usually exponential segments.
- **Filters.** The biquad: y[n] = b0·x[n] + b1·x[n−1] + b2·x[n−2] − a1·y[n−1] − a2·y[n−2]; coefficients derive from cutoff and Q (the Audio EQ Cookbook gives formulas for lowpass, highpass, bandpass, peaking, shelving).
- **Modulation synthesis.** FM: y = sin(2·pi·fc·t + I·sin(2·pi·fm·t)), with sidebands at fc ± k·fm whose strength follows Bessel functions of index I; AM and ring modulation multiply signals.
- **Delay-line effects.** Delay, chorus, flanger, reverb (comb and all-pass networks) all store past samples in a ring buffer and read at a fixed or modulated offset.
- **Scheduling.** Music is events on a clock: a transport with a tempo and a look-ahead scheduler fires notes slightly early so timing is sample-accurate despite jittery timers.
- **Block-diagram compilers.** Describing the signal graph in a language lets a compiler fuse and optimize it (Faust does this; see creative-tooling).

## Entries

### Tone.js — Tonejs/Tone.js
**Status:** MIT, about 14.8k stars, pushed Oct 2026. Checked: README.
**Principle:** a Web Audio framework with DAW concepts: a global **Transport** (tempo, time signature, loop) to schedule events, prebuilt synths and effects, and low-level building blocks and control signals for custom instruments.
**Mechanism (literature):** time values accept musical notation ("4n", "8t"); scheduling uses a look-ahead window over the Web Audio clock; signals can be connected to parameters, so an LFO can modulate a filter cutoff at audio rate.
**Use it when:** interactive music in the browser, generative scores, sound design for web pages.
**Pitfalls:** browsers require a user gesture before audio starts.

### Maximilian — micknoise/Maximilian
**Status:** MIT, about 1.7k stars, pushed Jan 2025. Checked: README.
**Idea:** a self-contained C++ library for synthesis and signal processing with JavaScript bindings (so the same DSP code runs natively and in the browser through AudioWorklet): oscillators, filters, envelopes, delays, granular synthesis, sample playback, and real-time analysis (spectrum, spectral features, octave and Bark analysis, MFCCs).

### DaisySP — electro-smith/DaisySP
**Status:** MIT (license text read; GitHub shows no classification), about 1.3k stars, pushed Sep 2026. Checked: README, LICENSE head.
**Idea:** a modular DSP component library (oscillators, filters, envelopes, drums, effects, control generators) written for embedded hardware: no dynamic allocation, one `Process()` per sample, small enough for a microcontroller, and reusable in plug-ins. A model for allocation-free audio code.

### Csound — csound/csound
**Status:** LGPL-2.1, about 1.5k stars, pushed Oct 2026. Checked: README (the develop branch is Csound 7).
**Principle:** one of the oldest music languages: an **orchestra** defines instruments as graphs of opcodes, a **score** triggers them; control rate (k-rate) and audio rate (a-rate) signals run at different speeds for efficiency.
**Mechanism (literature):** instruments are compiled to an instance graph per note; opcodes cover oscillators, physical models, granular, spectral processing and more; an API embeds Csound in other programs.
**Use it when:** research-grade synthesis, algorithmic composition. LGPL: linking is fine; changes to the library must be shared.

### SuperCollider and Faust
See the `creative-tooling` skill: SuperCollider (a real-time server controlled by messages) and Faust (a block-diagram language compiled to many targets).

### PySSTV — dnet/pySSTV
**Status:** MIT, about 190 stars, pushed Jul 2026. Checked: README.
**Principle:** slow-scan television: send an image as audio by frequency modulation.
**Mechanism (literature and README):** every pixel's brightness becomes a tone, commonly 1500 Hz for black to 2300 Hz for white, with sync pulses at 1200 Hz and a header (VIS code) that identifies the mode; lines are sent sequentially, color modes send separate channels (Martin, Scottie, Robot, PD families, all selectable). The README says the code favors readability over speed.
**Use it when:** a teaching example of images as signals; encoding images in audio for radio or art.
