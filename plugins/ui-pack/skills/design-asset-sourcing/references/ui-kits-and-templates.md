# UI Kits, Component Blocks & Templates

**Check the project's own kit first.** Many repos ship an internal UI package (often Radix + cva under `packages/*`). Importing a second component library on top of it is a bug, not a shortcut. Everything below is for *new* projects, or for lifting layout/markup ideas into an existing kit.

## React component libraries

| Library | URL | When |
|---|---|---|
| shadcn/ui | https://ui.shadcn.com/ | Copy-paste Radix + Tailwind components you then own. **Best match for a Radix-based kit** — steal a component's markup and adapt it into your own kit rather than installing anything. |
| Radix Primitives | https://www.radix-ui.com/primitives | Unstyled, accessible behavior. The dependency the kit already wraps. |
| Headless UI | https://headlessui.com/ | Tailwind team's alternative to Radix. |
| Base UI | https://base-ui.com/ | From the Radix/MUI authors; newer, unstyled. |
| Mantine | https://mantine.dev/ | 120+ styled components + hooks. Fast to ship, opinionated. |
| Chakra UI | https://chakra-ui.com/ | Styled, strong a11y defaults. |
| MUI | https://mui.com/ | Material. Heavy, hard to de-Material. |
| Ark UI | https://ark-ui.com/ | Headless, framework-agnostic (React/Vue/Solid). |
| Tremor | https://www.tremor.so/ | **Dashboard/analytics blocks** — KPI cards, charts, tables. Good reference for analytics layout even if you don't install it. |
| Magic UI | https://magicui.design/ | Animated marketing components (shadcn-compatible). |
| Aceternity UI | https://ui.aceternity.com/ | Flashy animated marketing sections. |
| Fancy Components | https://www.fancycomponents.dev/ | Experimental/playful interactions. |
| React Aria | https://react-spectrum.adobe.com/react-aria/ | Adobe's hooks — the most rigorous a11y layer available. |

## Tailwind blocks (copy markup, no install)

- https://www.hyperui.dev/ — free, large, modern
- https://mertjf.github.io/tailblocks/ — ready page sections
- https://flowbite.com/blocks/ — big block library (some paid)
- https://tailwindcomponents.com/ — community-submitted, quality varies
- https://tailwindui.com/components — official, paid, the quality benchmark
- https://daisyui.com/ — semantic class layer over Tailwind (themes for free)
- https://preline.co/ — free Tailwind component set

## Page templates / starters

- https://cruip.com/ — free + paid landing pages (Tailwind/React)
- https://html5up.net/ — free responsive HTML templates (CCA 3.0, attribution)
- https://www.free-css.com/ — large free template archive
- https://preview.tabler.io/ — free Bootstrap admin dashboard, very complete
- https://shuffle.dev/ — visual builder over Tailwind/Bootstrap blocks
- https://www.creative-tim.com/ — mixed free/paid kits
- https://vercel.com/templates — framework starters (Next.js, etc.)

## Classless / minimal CSS — for docs, demos, internal tools

Drop in one stylesheet, write plain HTML, done. Ideal for a quick internal page or a report preview.

- https://picocss.com/ (dark mode built in) · https://simplecss.org/ · https://watercss.kognise.dev/ · https://newcss.net/ · https://andybrewer.github.io/mvp/ · https://concrete.style/
- https://open-props.style/ — CSS custom properties (spacing/color/easing/shadows) with no components. Great for grounding a design system in tokens.
- Index of the rest: https://github.com/dbohdan/classless-css

## Themed / novelty CSS

For demos, retro projects, 404 pages, hackathons: https://www.getpapercss.com/ (hand-drawn) · https://terminalcss.xyz/ · https://github.com/nostalgic-css/NES.css · https://jdan.github.io/98.css/ · https://botoxparty.github.io/XP.css/ · https://khang-nd.github.io/7.css/ · https://sakofchit.github.io/system.css/ · https://latex.now.sh/ (academic paper) · https://arwes.dev/ (cyberpunk)

## Layout references

- https://every-layout.dev/ — the definitive treatment of resilient CSS layout primitives
- https://csslayout.io/ — 100+ common layout patterns as isolated examples
- https://web.dev/patterns/layout/ — modern layout recipes
- https://grid.layoutit.com/ · https://cssgrid-generator.netlify.app/ — visual grid builders
- https://joshwcomeau.com/css/full-bleed/ — full-bleed content inside a constrained column

## Rules

- **Copy the markup and a11y wiring, not the dependency.** A component from shadcn/HyperUI is a starting point to adapt into the existing kit — with the project's tokens, not hardcoded hex.
- Two component libraries in one app = two focus-trap implementations, two portal roots, doubled bundle. Don't.
- Templates are calibrated for marketing pages. A dense analytics view needs tighter spacing and smaller type than any landing-page template ships with.
- Check the license on templates: HTML5 UP is CC-BY (attribution in the footer), most Tailwind block sites are MIT-ish but per-site.
