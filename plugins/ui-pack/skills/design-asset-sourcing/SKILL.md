---
name: design-asset-sourcing
description: Use when a task needs illustrations, icons, SVG logos, stock photos, placeholder images or fake data, background patterns, fonts, color palettes, UI templates/component blocks, device mockups, or audio - routes to a vetted resource library, gives copy-paste fetch endpoints, and enforces license checks before anything ships.
---

# Design Asset Sourcing

Find, fetch, and transform free design assets. Never hand-draw an SVG or invent a hex palette when a canonical source exists.

## When to invoke

Any of these appear in the task:
- "we need an illustration / empty state / 404 art / hero image"
- "add an icon for X" (and the project has no icon set, or the set lacks the glyph)
- "put a logo for <brand> in the integrations grid"
- "fill this with placeholder images / avatars / fake users"
- "make a nicer background / pattern / gradient / section divider"
- "pick a font" / "pick a palette" / "generate the shade ramp"
- "scaffold a landing page / pricing section / dashboard shell"
- "make a screenshot look good for the README"

## Gate 0 — does this task need an asset at all?

**Run this before the routing table. Skipping it is the most common failure of this skill.**

The trigger is the user asking for an asset, or a task that cannot be completed without one. "This UI looks bare" is **not** a trigger — bare UI is usually a copy, hierarchy, or missing-action problem, and sourcing art papers over it.

| Symptom | Actual defect | Right fix |
|---|---|---|
| Empty state feels weak | Copy doesn't say *why* it's empty; no next action | Two lines of copy (distinguish "no data yet" from "filters matched nothing") + a button. Optional 20–24px icon from the installed set. |
| Page looks plain | Spacing, type scale, hierarchy | Layout work, not decoration |
| Dashboard feels flat | No visual encoding of the data | Better chart/table, not a background pattern |
| Loading looks janky | No skeleton | Skeleton, not a spinner illustration |
| "Needs personality" | Only true for marketing/onboarding surfaces | Ask the user before sourcing |

### Illustration vs icon vs nothing

- **Nothing** — inline validation, toasts, table cells, anything that appears more than once per screen.
- **Icon (20–24px, installed set)** — the default for an empty state inside a component: a filtered list, a panel, a tab, a dropdown, a sidebar section. Cheap, aligned to the grid, no new files.
- **Illustration (120–200px)** — only when the empty state **is the whole screen** and is seen **rarely**: first-run/zero-data onboarding, 404/500 pages, a completed-everything state, a full-page error. One per screen, maximum.

Weight is the tell: an illustration in a paginated list pushes real controls below the fold and re-appears every time a filter misses. That's a regression, not a polish.

### Density check

In dense/professional surfaces — analytics views, data tables, admin panels, reports — the bar is much higher. Decorative art competes with the data and is usually unwanted; many teams ban it outright there. Marketing pages, onboarding, and landing surfaces are where art earns its place. Check the project's own conventions before adding anything.

### If you're unsure

Ask, with the cheap option first: *"Empty state here can be (a) icon + copy + 'clear filters' action, or (b) a full illustration. (a) is 15 lines and no new assets — which do you want?"* Do not source first and present it as a fait accompli.

## Routing table

| Need | Go to | First pick |
|---|---|---|
| Illustrations, empty states, spot art | `references/illustrations.md` | unDraw, Storyset, Open Peeps |
| UI icons | `references/icons-and-logos.md` | Iconify API over Lucide / Phosphor / Tabler |
| Brand logos | `references/icons-and-logos.md` | Simple Icons CDN, SVGL, VectorLogoZone |
| Stock photos & video | `references/photos-and-video.md` | Unsplash, Pexels, Nappy |
| Placeholder images / avatars / fake data | `references/placeholders-and-fake-data.md` | placehold.co, picsum, DiceBear, Faker |
| Patterns, gradients, blobs, dividers | `references/backgrounds-and-patterns.md` | Haikei, MagicPattern, Hero Patterns |
| Fonts & pairings | `references/fonts-and-color.md` | Google Fonts, Fontshare, Fontpair |
| Palettes, ramps, contrast, dataviz colors | `references/fonts-and-color.md` | Leonardo, tints.dev, ColorBrewer |
| UI kits, blocks, page templates, CSS frameworks | `references/ui-kits-and-templates.md` | shadcn/ui, HyperUI, Tailblocks, Cruip |
| Device mockups, screenshot polish, 3D | `references/mockups-and-3d.md` | shots.so, Pika, ShapeFest |
| Sound & music | `references/audio.md` | Freesound, Pixabay Music, YouTube Audio Library |

Read only the reference file you need. Do not read all of them.

## Workflow

0. **Pass Gate 0.** If the answer is "no asset needed", stop and fix the real defect instead.
1. **Check the project first.** Grep for an existing icon set, illustration folder, palette tokens, or UI kit before opening any reference file:
   ```bash
   grep -rEh '"(lucide-react|@heroicons/react|@phosphor-icons/react|@tabler/icons-react|react-icons)"' --include=package.json .
   grep -rl "from 'lucide-react'" --include=*.tsx src | wc -l   # which one is ACTUALLY used
   ```
   A library in `package.json` with zero imports is a dead dep, not the project's set. Reusing beats sourcing — if the repo ships its own UI package, the answer to "I need a component" is in there, not on the web.
2. **Verify the glyph exists in the installed version** before writing the import — icon sets rename constantly:
   ```bash
   ls node_modules/lucide-react/dist/esm/icons/ | grep -E '^(inbox|file-search)'
   ```
3. **Pick from the reference file**, biased to the "First pick" column unless the task says otherwise.
4. **Fetch programmatically** using the recipes below — don't tell the user to go download a zip.
5. **Transform to fit**: run SVGO (with `removeViewBox` disabled — see below), strip `width`/`height`, map hardcoded hex to `currentColor` or CSS variables so the asset follows the theme.
6. **Record the license** in a header comment on the file, plus an `ASSETS.md` / `CREDITS.md` line when attribution is required. Never skip this.
7. **Lint.** `cd frontend && npx tsc --build`. A new component file is still a code change.

### Where the asset goes

- Icons: import from the installed package. Never commit an icon SVG that the package already ships.
- One-off illustration: a component next to its consumer, or `src/components/illustrations/` if shared. Inline it as JSX **only** if it must react to theme/props; otherwise ship a `.svg` file and `<img>` it so it stays out of the JS bundle.
- Anything used by two apps in a monorepo goes in the shared package, not copied.

## License discipline — non-negotiable

Before an asset ships, know its license. Three buckets:

- **Free, no attribution** — unDraw, Lucide, Heroicons, Tabler, Phosphor, Open Props, Google Fonts, Unsplash/Pexels/Pixabay (their own licenses, still no attribution required). Safest default; prefer these.
- **Free with attribution** — Freepik/Storyset free tier, Noun Project free tier, CC-BY photos, most Freesound clips. Requires a visible credit line. Only use if the user accepts a credits surface.
- **Trap** — brand logos are trademarks, not free art: Simple Icons/SVGL ship the *SVG* under permissive terms but the *mark* is still owned. Use only for genuine identification (integrations grid, "sign in with"), never as decoration or in your own branding.

Additional hard rules:
- **Never** feed user-supplied photos or any regulated data (health, biometric, financial, minors) into a third-party tool (remove.bg, cleanup.pictures, any online editor). Those are for synthetic/marketing assets only.
- Hotlinking a placeholder service in production is a third-party dependency and a privacy leak. Placeholders are for dev/demo; download and self-host for anything shipped.
- Self-host fonts (Google Fonts CDN is a GDPR liability in the EU). `npm i @fontsource/<font>` or download the woff2.

## Programmatic fetch recipes (verified)

Icons — Iconify API covers 200+ sets with one URL shape:
```bash
curl -s "https://api.iconify.design/search?query=calendar&limit=10"      # find
curl -s "https://api.iconify.design/lucide/house.svg" -o house.svg       # fetch
curl -s "https://api.iconify.design/lucide/house.svg?color=%23fff&height=24"
curl -s "https://api.iconify.design/collections"                          # list sets
```

Icons from CDN when you want the raw repo file:
```bash
https://cdn.jsdelivr.net/npm/lucide-static/icons/<name>.svg
https://cdn.jsdelivr.net/npm/@phosphor-icons/core/assets/regular/<name>.svg
https://cdn.jsdelivr.net/npm/heroicons/24/outline/<name>.svg
https://unpkg.com/@tabler/icons/icons/outline/<name>.svg
```

Brand logos:
```bash
curl -s "https://cdn.simpleicons.org/github"            # auto-colored
curl -s "https://cdn.simpleicons.org/github/white"      # forced color
curl -s "https://api.svgl.app" | jq '.[0:3]'            # SVGL catalog JSON
curl -s "https://api.svgl.app/categories"
```

Placeholder images (dev only):
```bash
https://placehold.co/600x400/1f2937/f9fafb.png?text=Chart      # solid, labeled
https://picsum.photos/seed/<stable-seed>/400/300               # real photos, deterministic
https://api.dicebear.com/9.x/<style>/svg?seed=<name>           # avatars, deterministic
https://ui-avatars.com/api/?name=Ana+Silva&background=random   # initials avatars
```

Fake data:
```bash
npm i -D @faker-js/faker            # local generation, no network, seedable
curl -s https://randomuser.me/api/?results=5
curl -s https://dummyjson.com/products?limit=5
```

Illustrations — unDraw has an undocumented but working search API returning direct CDN URLs:
```bash
curl -s "https://undraw.co/api/search?q=no%20data"     # NOTE: q= (not query=), min 3 chars
# -> {"results":[{"title":"No data","newSlug":"no-data_ig65",
#                "media":"https://cdn.undraw.co/illustrations/no-data_ig65.svg"}, ...]}
curl -s "https://cdn.undraw.co/illustrations/no-data_ig65.svg" -o art.svg
```
Slugs carry a random 4-char suffix — always discover them via the search endpoint, never construct a CDN URL by hand.

SVG cleanup after any download — **the default SVGO preset deletes `viewBox`**, which breaks responsive scaling. Always override it:
```bash
cat > svgo.config.mjs <<'EOF'
export default {
  multipass: true,
  plugins: [
    { name: 'preset-default', params: { overrides: { removeViewBox: false } } },
    { name: 'removeDimensions' },   // drops width/height, keeps viewBox
  ],
};
EOF
npx svgo --config svgo.config.mjs --input in.svg --output out.svg
```
Then map the palette. unDraw's accent is always `#6c63ff`; the rest are `#3f3d56` (ink), `#f2f2f2`/`#e6e6e6` (surfaces), `#fff` (highlight). On a dark UI the surfaces and white **glare**, so map all five, not just the accent:
```bash
sed -e 's/#6c63ff/var(--illo-accent)/g'   -e 's/#3f3d56/var(--illo-ink)/g' \
    -e 's/#f2f2f2/var(--illo-surface-2)/g' -e 's/#e6e6e6/var(--illo-surface-1)/g' \
    -e 's/#fff/var(--illo-highlight)/g' out.svg > tokens.svg
grep -oE '#[0-9a-fA-F]{3,6}' tokens.svg   # must print nothing
```

## Shell wrappers can break these recipes

Some setups put a token-saving proxy in front of the shell (RTK and similar hooks). Two symptoms, both easy to misread as a broken API:

- **A JSON response comes back as a type schema** (`{"name": string, "total": int}`) instead of values — the body is being summarized, not returned. Re-run the call in raw/passthrough mode (`rtk proxy curl ...`) before concluding the endpoint changed.
- **`npx <pkg>` gets rewritten to `npm`** and fails with `Unknown command: "svgo@3"`. Same fix: raw passthrough.
- Binary/SVG downloads and status-code checks normally pass through untouched.

## Dead — do not suggest

Verified dead or defunct as of 2026-08: `source.unsplash.com` (retired), `via.placeholder.com`, `placekitten.com`, `source.boringavatars.com`, `iradesign.io`, `error404.fun`. If a URL from a reference file 404s, note it and move to the next pick rather than improvising a lookalike domain.

## Keeping this current

Library seeded from swyx's spark-joy (https://github.com/swyxio/spark-joy) plus the r/webdev free-SVG-illustrations thread, then link-checked. Design-resource domains rot fast and expired ones get bought by spammers — before recommending anything not in these files, verify it:

```bash
curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" -L --max-time 10 "<url>"
```
`403`/`429`/`455` = bot-blocked but alive. `000`/`404`/`410` = dead; add it to the "Dead" list in the relevant reference file instead of silently dropping it.

## Anti-patterns

- **Sourcing an asset the task never asked for.** The top failure mode. See Gate 0.
- **Illustration where an icon belongs** — inside a list, panel, tab, or anything repeated.
- Hand-writing SVG path data for a common glyph. Fetch it.
- Mixing icon sets in one UI — stroke widths and grids clash. One set per surface.
- Illustrations in a hardcoded brand color that ignores dark mode. unDraw/Storyset let you set the accent; do that, or edit the fills to CSS variables.
- Shipping a placeholder domain to production.
- Grabbing a "free" asset from a Google Images result with no license page.
