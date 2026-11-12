Use Faust as the first prototype: describe DSP as a signal graph, then compile the same core to C/C++, WebAssembly, and embedded targets. Build thin platform adapters around it for plugin formats, Web Audio, and each device’s audio and control APIs; test performance and sound on every target, since “write once” still needs platform-specific integration.

Faust’s compiler is LGPL-2.1-or-later. That can fit a commercial product, but review the exact license and notices for every compiler component, library, and architecture file you ship. Keep your proprietary DSP and product code separate, and get legal review before distribution.

If Faust’s model doesn’t fit, another route is a portable C++ DSP core with separate plugin, browser, and firmware wrappers. JUCE is a common option for plugins and desktop audio, but check its current commercial licensing and whether its platform support covers your targets.

Avoid starting from GPL or AGPL synthesis code for a closed product unless you’re prepared to meet its obligations.