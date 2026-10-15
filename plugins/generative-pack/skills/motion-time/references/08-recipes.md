# Recipes

## Motion design with an AI coding agent: three stages

Source: a short video by the creator `raycfu`, checked against its on-screen recap slide. It describes a method, not a benchmark; results are the author's claim.

The idea: do not ask a model for a video file. Have it write code that paints each frame, render the frames, then encode them.

1. Render engine. A headless pipeline with Node, ffmpeg and Playwright. The agent writes a `renderFrame(t)` function; Playwright evaluates it at exact time steps and screenshots each frame in Chrome; ffmpeg stitches the PNG sequence into an MP4. The video runs the model at its highest reasoning setting.
2. Reference and assets. Feed real design references and assets, since left alone the model produces generic layouts. Ban basic CSS easing (`transition: all .3s ease`) in the prompt and require closed-form spring equations with damping and stiffness. Synthesize audio in code (oscillators plus noise, no sample files). Lock every cut to the beat (for example every two beats at 120 BPM).
3. Self-critique. Have the agent look at its own rendered frames, flag dead frames where nothing on screen moves, re-render the weak scenes, and loop until every scene scores at least 8 out of 10.

Related tools in this skill: easing and springs in `01` and `02`; code-driven scenes in `05`.
