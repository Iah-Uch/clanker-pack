# Fonts & Color

## Font sources

| Source | URL | Notes |
|---|---|---|
| Google Fonts | https://fonts.google.com/ | 1500+, all self-hostable via `@fontsource/<name>`. Default choice. |
| Fontshare | https://www.fontshare.com/ | Indian Type Foundry — professional quality, free for commercial use. Where to go when Google Fonts feels generic. |
| Uncut.wtf | https://uncut.wtf/ | Contemporary/experimental typefaces, free. |
| Velvetyne | http://velvetyne.fr/ | Libre experimental type. |
| Fontsource | https://fontsource.org/ | The npm delivery layer for open fonts — `npm i @fontsource-variable/inter`. |
| Beautiful Web Type | https://beautifulwebtype.com/ | Curated shortlist of the good Google fonts. |
| Programming fonts | https://www.programmingfonts.org/ · https://devfonts.gafi.dev/ | Compare monospace fonts live. |

**Reliable picks:** Inter (UI), Geist / IBM Plex Sans (UI, more character), Source Serif / Literata (long-form), JetBrains Mono / IBM Plex Mono (code), Atkinson Hyperlegible (accessibility-first, https://brailleinstitute.org/freefont).

## Pairing

- https://fontpair.co/ — curated pairings
- https://fontjoy.com/ — ML pairing by similarity/contrast slider
- https://www.typewolf.com/ — real-world usage, "site of the day" with type credits
- https://fontsinuse.com/ — historical/editorial usage
- https://modernfontstacks.com/ — **system font stacks with zero download cost**. Consider before adding any webfont.
- https://type-scale.com/ — modular scale generator
- https://fluid-typography.netlify.app/ — `clamp()` fluid type generator

Pairing heuristic: one family with multiple weights beats two families. If you use two, make them maximally distinct (serif + grotesque), never two similar sans.

## Font delivery rules

- **Self-host.** `npm i @fontsource-variable/<font>`. Google's CDN is a GDPR problem in the EU and adds a third-party connection.
- woff2 only. Subset to the scripts you use (`latin`, `latin-ext` for pt-BR) — `glyphhanger` or `subfont` for custom subsets.
- `font-display: swap` + `<link rel="preload" as="font" crossorigin>` on the one font used above the fold.
- Prefer **variable fonts** when you need 3+ weights — one file beats four.
- Set `size-adjust`/`ascent-override` on the fallback to kill layout shift on swap.

## Color palettes

| Tool | URL | Use |
|---|---|---|
| Leonardo | https://leonardocolor.io/ | Adobe's tool — generates palettes by **target contrast ratio**. Use when accessibility is a requirement, not an afterthought. |
| tints.dev | https://www.tints.dev/ | Generate a full 50–950 Tailwind ramp from one hex, with lightness/chroma control. |
| Coolors | https://coolors.co/ | Fast exploratory generator, exports everywhere. |
| Happy Hues | https://www.happyhues.co/ | Palettes shown *in a real UI* with role assignments — solves "which color goes where". |
| Open Color | https://yeun.github.io/open-color/ | Pre-tuned open-source palette; safe defaults for a design system. |
| Radix Colors | https://www.radix-ui.com/colors | 12-step scales with defined semantic roles (backgrounds/borders/text) and automatic dark-mode counterparts. **Best fit for a Radix-based kit.** |
| Atmos | https://atmos.style/ | UI palette toolbox with contrast checks. |
| Adobe Color | https://color.adobe.com/create | Classical harmony rules + accessibility tools. |
| Color Hunt | https://colorhunt.co/ | Browse curated palettes. |
| Palettte App | https://palettte.app/ | Fix an existing ramp's uneven lightness curve. |
| Khroma | http://khroma.co/ | Trains on your likes, generates endlessly. |

## Contrast & accessibility

- https://webaim.org/resources/contrastchecker/ — the reference checker
- https://www.myndex.com/APCA/ — APCA, the perceptual model behind WCAG 3; more accurate than the 4.5:1 ratio for dark UIs
- https://leonardocolor.io/ — design *to* a contrast target instead of checking afterwards
- Targets: 4.5:1 body text, 3:1 large text and UI component boundaries. Where a misread value has real consequences (medical, financial, safety), treat this as a hard requirement, not a guideline.
- **Never encode meaning in hue alone** — pair color with a shape, icon, label, or position.

## Dataviz color

- https://colorbrewer2.org/ — the canonical sequential/diverging/qualitative schemes, with colorblind-safe filters
- https://personal.sron.nl/~pault/ — Paul Tol's colorblind-safe qualitative and sequential schemes
- https://github.com/d3/d3-scale-chromatic — the same schemes as code
- https://www.learnui.design/tools/data-color-picker.html — quick sequential/diverging picker
- https://blog.datawrapper.de/beautifulcolors/ — practical rules for chart color
- Rules: sequential for magnitude, diverging for a meaningful midpoint, qualitative for categories (max ~7 before they stop being distinguishable). Never a rainbow scale for continuous data.

## Dark mode

- Don't invert. Dark surfaces need *desaturated, lifted* colors — pure `#000` + saturated accents vibrate.
- Elevation is expressed by lighter surfaces, not shadows.
- Radix Colors gives you the dark counterpart of every step for free — that's why it's the recommendation here.
- Reference: https://darkmodedesign.xyz/ , https://stripe.com/blog/accessible-color-systems

## Learning

- https://learnui.design/blog/color-in-ui-design-a-practical-framework.html — the best single article on UI color
- https://refactoringui.com/previews/building-your-color-palette/ — building a ramp
- https://practicaltypography.com/ — typography reference
