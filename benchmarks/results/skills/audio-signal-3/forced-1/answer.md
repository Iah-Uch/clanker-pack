For all three, start with the same building block: a GPU FFT. A 2D FFT runs row and column transforms; convolution becomes FFT → multiply spectra → inverse FFT. For time-varying audio effects, use overlapping windowed FFT frames (STFT), process each frame, then overlap-add.

`glsl-fft` is a small MIT-licensed example of FFT butterflies in fragment shaders, suitable to study for GPU spectral effects, ocean synthesis, and Fourier optics. Verify its fit for your target GPU API before adopting it.

For ocean waves, evolve a frequency-domain wave spectrum over time and inverse-transform it into a height field. For Fourier optics, propagate a complex field with FFT-based transforms and phase factors. These are technique patterns; adapt them to your physics and precision needs.

MIT, ISC, and BSD licenses generally fit commercial use with required notices. Copyleft projects such as GPL or AGPL may impose obligations depending on how you use and distribute them. Keep implementation separate or get legal review before incorporating copyleft code.