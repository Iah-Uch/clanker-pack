# Audio analysis, spectra, FFT and reconstruction from projections

A catalog of ideas. The projects are examples of each technique, not drop-in solutions. "Checked" says what I read; "literature" marks the published technique, not this project's code.

## Cross-cutting ideas

- **The Fourier transform.** X[k] = sum_n x[n]·exp(−2·pi·i·k·n / N). The FFT computes it in O(N log N) by splitting into even and odd halves recursively (Cooley-Tukey radix-2) and combining with "butterfly" operations using twiddle factors exp(−2·pi·i·k/N). Radix-4 does the same with fewer multiplications.
- **STFT and the spectrogram.** Cut the signal into overlapping windows (Hann, 50 to 75 percent overlap), FFT each, and stack magnitudes into a time-frequency image. The window length trades time resolution against frequency resolution.
- **Perceptual frequency scales.** Mel: m = 2595·log10(1 + f/700). A mel filter bank summed over FFT bins, a log, and a discrete cosine transform give **MFCCs**, a compact timbre descriptor.
- **Onset detection.** Spectral flux: sum over bins of max(0, |X_t[k]| − |X_{t−1}[k]|); peaks mark attacks. Beat tracking aligns a tempo hypothesis to onsets.
- **Pitch detection.** Autocorrelation or the YIN difference function d(tau) = sum (x[n] − x[n+tau])², normalized, with the first dip below a threshold giving the period; the pitch is fs / tau.
- **Power spectral density.** Welch's method: average the squared FFT of many windowed segments to estimate noise floors.
- **Time-frequency with constant Q.** The Q-transform uses logarithmically spaced bins with a window length inversely proportional to frequency, matching musical pitch and chirping signals.
- **Reconstruction from projections.** Tomography measures line integrals of an object (the Radon transform); filtered back projection applies a ramp filter in the frequency domain to each projection and smears it back along its rays; iterative methods (SIRT, SART, CGLS) solve the linear system A·x = b by repeated forward and backward projection.
- **Many tools, same GPU trick.** Spectral transforms map well to GPU: butterflies run as ping-pong passes between two textures.

## Entries

### librosa — librosa/librosa
**Status:** ISC, about 8.7k stars, pushed Oct 2026. Checked: README.
**Idea:** the standard Python library for music information retrieval: STFT, mel spectrograms, MFCCs, chroma, onset and beat tracking, pitch estimation (YIN and pYIN), harmonic and percussive separation, time stretching and pitch shifting. A readable reference for how the descriptors are computed.
**Use it when:** feature extraction, audio-reactive visuals, ML preprocessing.

### aubio — aubio/aubio
**Status:** GPL-3.0, about 3.8k stars, pushed Apr 2026. Checked: README.
**Idea:** a library that labels sounds: onset detection, pitch detection, beat tracking, and MIDI stream output, with a Python module. Copyleft: take the algorithms (spectral flux onset, YIN pitch), write your own code.

### Essentia — MTG/essentia
**Status:** AGPL-3.0 (the README says Affero GPLv3), about 3.8k stars, pushed Oct 2026. Checked: README.
**Idea:** a large C++ library of audio analysis algorithms (spectral, temporal, tonal, rhythmic descriptors, standard extractors) with Python bindings; also hosts pretrained models. AGPL: network use triggers source sharing; commercial licenses exist from the lab (check the project).

### fft.js — indutny/fft.js
**Status:** no license detected on GitHub (the field is empty), about 360 stars, pushed Mar 2023. Checked: metadata only. **Do not copy code**; the algorithm is classical.
**Idea:** a fast JavaScript radix-4 and radix-2 FFT. Precomputed twiddle tables, in-place bit-reversal, and typed arrays are the performance tricks to remember.
**Build it yourself:** an iterative radix-2 FFT is about thirty lines: bit-reverse the input, then for each stage double the butterfly span and combine with precomputed twiddles.

### glsl-fft — rreusser/glsl-fft
**Status:** MIT (license text read; GitHub shows no classification), about 90 stars, pushed Dec 2018. Checked: LICENSE head, README.
**Principle:** the FFT of complex matrices in fragment shaders.
**Mechanism (literature):** log2(N) passes alternating between two textures; each pass is a butterfly stage where a pixel reads two source texels determined by its index and stage, multiplies one by a twiddle factor and adds or subtracts; a 2D FFT does rows then columns.
**Use it when:** convolution and spectral effects on the GPU, ocean wave synthesis, Fourier optics.

### GWpy — gwpy/gwpy
**Status:** GPL-3.0 or later (the README says so), about 380 stars, pushed Aug 2026. Checked: README.
**Idea:** time-series and frequency-series containers for gravitational-wave detector data with units and metadata: filtering, spectrograms, Q-transforms to reveal chirps, and Welch PSD estimates. A good example of wrapping signal processing in unit-aware data types. Copyleft: reuse ideas only.

### ASTRA Toolbox — astra-toolbox/astra-toolbox
**Status:** GPL-3.0, about 640 stars, pushed Aug 2026. Checked: README.
**Idea:** GPU primitives for 2D and 3D tomography: parallel, fan and cone beam geometries with flexible source and detector positions, forward projection and back projection callable from Python and MATLAB, and algorithms built on them (FBP, SIRT, SART, CGLS). The design lesson: expose the two operators A and A^T and let algorithms be a few lines on top. Copyleft: reuse the method.
**Use it when:** CT reconstruction; any inverse problem of the form A·x = b with a sparse linear operator.
