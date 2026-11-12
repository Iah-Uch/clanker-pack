For a commercial, tiling surface, start with a spectral ocean: sample a directional wave spectrum, evolve Fourier amplitudes over time, then inverse-FFT to get height, displacement and normals. Use several frequency bands for detail and choppiness. It’s fast, tileable, and well suited to rendered oceans and lakes; it does not simulate shorelines or breaking waves in detail.

GodotOceanWaves is a practical MIT-licensed reference implementation. You can adapt its code in a commercial product while retaining the required copyright and license notices. If you want only the method, implement the published Tessendorf approach independently.

For shallow water, shore interaction, or physically driven wave propagation, use a grid-based shallow-water solver; expect more complexity and cost. Particle fluid methods such as SPH are better for localized splashes than an endless tiled surface. SPlisHSPlasH is MIT-licensed, but likely excessive for the base surface.

Recommendation: build the ocean with spectral waves, then layer local interaction effects as needed. Check the repository’s license and dependencies before shipping, and have counsel review obligations for your distribution model.