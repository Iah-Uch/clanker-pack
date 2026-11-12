For a commercial product, start with vendor GPU libraries: NVIDIA cuFFT/cuDNN, AMD rocFFT/hipFFT, or Intel oneMKL for FFTs and convolution. Their terms are proprietary, so review each vendor’s current license and redistribution rules before shipping.

For portable, open-source GPU FFTs, consider VkFFT (MIT), clFFT (Apache 2.0, but development is inactive), or heFFTe (BSD 3-Clause). Prefer a maintained project and verify its current status and license before adoption.

For ocean waves, Tessendorf’s spectral method is a widely used technique; it is an algorithm, not a library license. You can implement it yourself using an FFT library. For Fourier optics, look at open-source wave-optics packages such as POPPY (BSD 3-Clause), though it is primarily Python/NumPy and may not suit a GPU runtime.

A practical path: prototype the math in Python, then implement GPU kernels around a portable FFT library. Track licenses for dependencies and bundled assets separately. This is general guidance, not a substitute for checking the exact license texts and obligations before commercial distribution.