Use a portable DSP core written in C or C++, with thin adapters for each target. Keep the core free of host APIs, allocation in the audio callback, and platform-specific code.

For plugins, JUCE offers broad format and platform support, but its dual licensing matters: its AGPL option can require you to release your product’s source, while commercial distribution requires a paid license. For a more permissive route, consider iPlug2 (often used under permissive licensing; check its current terms) or implement formats with Steinberg’s VST3 SDK, which has its own license terms.

For web audio, compile the same C/C++ core to WebAssembly with Emscripten, then connect it through the Web Audio API or an AudioWorklet. Keep browser-specific code in that adapter.

For embedded firmware, use the same core with a small hardware/DSP adapter; projects such as DaisySP can help on Daisy hardware, while CMSIS-DSP is useful on supported ARM targets. Their licenses and any dependencies need review.

For a commercial product, prefer a permissive core license such as MIT or BSD-2-Clause, and track licenses for every dependency. Confirm current license texts and obligations before shipping; licensing can vary by version and distribution model.