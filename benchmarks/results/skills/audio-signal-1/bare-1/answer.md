For browser-native music, start with **Web Audio API** (native, no license cost) for synthesis, sample playback, effects, and precise scheduling. Add **Tone.js** (MIT) for sequencing, instruments, transport, and musical timing.

For generative scores, use **Tonal** (MIT) for music theory utilities, or **abcjs** (MIT) to render and play ABC notation. For richer notation, **Verovio** (LGPL-3.0) renders MusicXML/MEI; check whether its linking and distribution terms fit your product.

For sound design, **RNBO** can export browser-ready patches, but it is commercial software with licensing terms. **Pure Data** is GPL-3.0; embedding or distributing it may impose obligations. **Csound** is LGPL-2.1-or-later and is another option for synthesis and composition.

Practical default: Web Audio API + Tone.js, with your own DSP or permissively licensed libraries. For each dependency, verify the exact package license and any bundled samples, fonts, or assets. “Open source” does not always mean obligation-free for commercial use; GPL-family licenses can require source disclosure when distributing covered software. This is general guidance, not legal advice.