For a commercial product, choose based on the look and scale you need:

- For real-time oceans, use a GPU FFT/Tessendorf spectrum. It produces convincing large-scale waves efficiently, but needs custom implementation or integration.
- For lakes or stylized water, use layered scrolling normal maps or Gerstner waves. They’re simpler, tile cleanly, and are easier to tune.
- For detailed near-shore water, combine either approach with shallow-water simulation or local displacement.

Open-source options include Godot’s built-in water features (MIT-licensed engine), Blender’s Ocean modifier (GPL-licensed Blender; check whether its code or assets fit your integration), and projects such as Crest Ocean System for Unity (MIT). Verify each project’s current license and dependencies before shipping, and review asset licenses separately.

My default: start with Gerstner waves plus scrolling normals; move to FFT only if you need a realistic open ocean. Choose a permissive license such as MIT or Apache-2.0 for reusable code, and keep attribution/notices required by dependencies. This is general guidance, not legal advice.