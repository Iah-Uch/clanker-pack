# Backgrounds, Patterns, Gradients, Shapes

Most of these are **generators** — configure in-browser, export SVG/CSS, self-host. Never hotlink.

## The workhorses

| Tool | URL | Output |
|---|---|---|
| Haikei | https://haikei.app/ | The single most useful one. Blobs, waves, layered peaks, stacked steps, low-poly grids, mesh gradients. Exports SVG/PNG. |
| MagicPattern | https://www.magicpattern.design/tools | Pattern, mesh gradient, blob, and CSS background generators in one place. |
| Hero Patterns | https://heropatterns.com/ | 100+ tileable SVG patterns, color + opacity configurable, outputs a CSS data-URI. |
| SVG Backgrounds | https://www.svgbackgrounds.com/ | Configurable SVG backgrounds + CSS snippets. |
| Transparent Textures | https://www.transparenttextures.com/ | Tiny tileable overlay textures (noise, paper, fabric). Layer over a solid color. |
| Cool Backgrounds | https://coolbackgrounds.io/ | Gradients, particles, triangles, topography. |
| Pattern Monster | https://pattern.monster/ | 180+ searchable SVG patterns with live params. |
| BGJar | https://bgjar.app/ | Organic shapes and abstract SVG backgrounds. |
| Trianglify | https://trianglify.io/ | Low-poly triangle meshes (also an npm lib for build-time generation). |
| Doodad | https://doodad.dev/pattern-generator/ | Parametric pattern generator. |
| CSS Doodle | https://css-doodle.com/ | Generative patterns via a web component — animatable, no image files. |
| Toptal Subtle Patterns | https://www.toptal.com/designers/subtlepatterns/ | The classic subtle tiled texture archive. |

## Section dividers / waves

- https://www.shapedivider.app/ — the standard tool for angled/curved/wave section transitions. Exports the SVG + positioning CSS.
- https://getwaves.io/ — layered SVG waves.
- https://svgwave.in/ — waves with gradients.
- https://wweb.dev/resources/css-separator-generator — pure-CSS separators.

## Gradients

| Tool | URL | Notes |
|---|---|---|
| Josh Comeau's gradient generator | https://www.joshwcomeau.com/gradient-generator/ | Interpolates in better color spaces (HSL/LCH) — avoids the muddy gray midpoint that naive RGB gradients get. Use this one. |
| Learn UI gradient tool | https://www.learnui.design/tools/gradient-generator.html | Same principle, different UI. |
| Mesh Gradient | https://meshgradient.com/ | Apple-style multi-point mesh blobs. |
| CSS Gradient | https://cssgradient.io/ | Plain linear/radial builder. |
| UI Gradients | https://uigradients.com/ · WebGradients https://webgradients.com/ | Pre-made two-stop palettes to copy. |
| Hypercolor | https://hypercolor.dev/ | Tailwind gradient classes. |
| Gradient Magic | https://www.gradientmagic.com/ | Exotic CSS-only gradient effects. |
| Conic.style | https://www.conic.style/ | Conic gradient examples. |

**Gradient rule:** interpolate in `oklch`/`lch`, not sRGB. Modern CSS: `linear-gradient(in oklch, #06f, #f06)`. Otherwise a blue→pink gradient passes through gray.

## 3D & advanced

- https://www.shapefest.com/ — 160k+ rendered 3D shape PNGs, free
- https://spline.design/ — interactive 3D scenes for the web (watch the bundle size)
- https://www.handz.design/ — 3D hands
- https://polygonrunway.com/ — learning Blender for low-poly scenes

## Implementation rules

- Inline generated SVG patterns as a CSS `data:` URI (URL-encode `#` as `%23`) — one fewer request, and CSS variables can drive the color if you inline the SVG into the DOM instead.
- Keep decorative backgrounds behind `aria-hidden` and out of the tab order.
- Respect `prefers-reduced-motion` for any animated background — animated gradients are a real vestibular trigger.
- A 4MB mesh-gradient PNG hero is a performance bug. Generate SVG, or export at ≤1600px and let CSS scale it.
- In a data-dense app (charts, tables), a busy background destroys readability. Patterns belong on marketing surfaces, not on an analysis view.
