# Illustrations

Spot art, 404 pages, zero-data onboarding, hero art, marketing sections.

**Before picking one, confirm the surface deserves it (SKILL.md Gate 0).** An illustration is a full-screen, seen-rarely element: first-run onboarding, 404/500, an all-done state, a full-page error. An empty state *inside* a component — a filtered list, a panel, a tab — gets a 20–24px icon from the installed set and better copy. If you're about to add art to a paginated list or a data table, you're solving the wrong problem.

## First picks

| Source | URL | License | Why / when |
|---|---|---|---|
| unDraw | https://undraw.co/illustrations | Open, no attribution | The default. Pick an accent color on the site before download and the SVG comes out themed. Huge, generic, business-safe. |
| Storyset | https://storyset.com/ | Free w/ attribution (Freepik) | Best when you need animation — exports animated SVG/Lottie. Requires a credit line. |
| Open Peeps | https://openpeeps.com/ | CC0 | Hand-drawn people, mix-and-match parts. No attribution. |
| Humaaans | https://www.humaaans.com/ | Free, attribution appreciated | Mix-and-match human figures, diverse. Good for "people using the product" scenes. |
| DrawKit | https://www.drawkit.com/ | Free packs MIT, others paid | Clean vector packs by theme. Check per-pack license. |
| ManyPixels | https://www.manypixels.co/gallery | Free, CC-BY-ish | unDraw alternative, multiple styles, color customization in-browser. |
| Open Doodles | https://www.opendoodles.com/ | CC0 | Loose sketch style, free generator for poses. |
| Blush | https://blush.design/ | Mixed free/paid | Collections by named illustrators; composable. Figma/Sketch plugins. |
| Absurd Design | https://absurd.design/ | Free tier | Surreal hand-drawn. Strong personality — use when generic corporate art would feel dead. |
| Glaze | https://www.glazestock.com/ | Free | Curated illustration collection. |
| Illlustrations.co | https://illlustrations.co/ | MIT | 100-illustration pack from a 100-day challenge. |
| Lukasz Adam | https://lukaszadam.com/illustrations | Free | Icons + illustrations, consistent style. |
| Icons8 Ouch | https://icons8.com/illustrations | Free w/ link attribution | Many styles, editable in-browser. |
| Woobro | https://woobro.design/ | Free | Small set, very detailed, niche scenes. |
| Fresh Folk | https://fresh-folk.com/ | Free | Humaaans-alike, different style, composable people. |
| Pimp My Drawing | https://pimpmydrawing.com/ | Free | Vector packs, character/scene oriented. |
| Game Icons | https://game-icons.net/ | CC-BY 3.0 | 4000+ game/fantasy/RPG glyphs. Attribution required. |
| Pixeltrue | https://www.pixeltrue.com/ | Free | Includes animated illustrations. |
| Delesign | https://delesign.com/free-designs/graphics/ | Free | General graphics library. |
| Freepik | https://www.freepik.com/ | Free w/ attribution / paid | Enormous. Attribution required on free tier — easy to violate accidentally. |
| Vecteezy | https://www.vecteezy.com/ | Mixed | Same caveat as Freepik. |
| Open Clip Art | https://openclipart.org/ | Public domain | Old-school, unpolished, but genuinely PD. |
| OpenGameArt | https://opengameart.org/ | Mixed OSS | Game sprites/tiles/assets. |
| SVG Repo | https://www.svgrepo.com/ | Per-asset | 500k+ vectors, license shown per item — check it, it varies. |

## Style-specific

- **Isometric**: https://isometric.online/ (searchable) , https://www.isometriclove.com/ , https://isoflat.com/
- **Buildings/scenery**: https://www.veila.me/freebies/scandinavian-houses-free-vector-images
- **3D objects/shapes**: https://www.shapefest.com/ (160k+ PNGs), https://www.handz.design/ (hands), https://powerpeopleplatform.com/ (3D avatars)
- **Abstract/backgrounds**: see `backgrounds-and-patterns.md`
- **Doodles**: https://github.com/MariaLetta/mega-doodles-pack (CC0)
- **Composable scenes**: https://usesmash.com/ , https://www.storyset.com/

## Representation

Default illustration libraries skew heavily white/able-bodied. When the product shows users:
- https://www.blackillustrations.com/ — free, Black representation
- https://fresh-folk.com/ — diverse people library
- Open Peeps / Humaaans — skin tone and hair are parameters; set them, don't ship the default.

## Fetching unDraw programmatically

The site has no documented API, but the one its own search box uses works and returns direct CDN URLs:

```bash
curl -s "https://undraw.co/api/search?q=empty"          # q=, minimum 3 characters
```
Returns `{"results":[{"title","newSlug","media"}]}` where `media` is the SVG URL. Both `cdn.undraw.co/illustration/<slug>.svg` and `.../illustrations/<slug>.svg` appear in results — use the exact string from `media`; the 4-char slug suffix is random and cannot be guessed.

Useful queries for empty/error surfaces: `no data`, `empty`, `not found`, `void`, `searching`.

## Working notes

- Optimize with SVGO, but **disable `removeViewBox`** — the default preset strips it and the illustration stops scaling. See the SKILL.md config block.
- unDraw's palette is always the same five values: `#6c63ff` accent, `#3f3d56` ink, `#f2f2f2` / `#e6e6e6` surfaces, `#fff` highlights. On a dark UI, mapping only the accent leaves glaring white paper — map all five to CSS variables.
- Don't inline a 200KB illustration into a JS bundle. `<img src>` it; inline as JSX only when it must respond to theme or props.
- Cap the rendered size (~120–200px). unDraw files carry 600×600+ intrinsic dimensions and will dominate a layout if unconstrained.
- `aria-hidden="true"` — decorative art must not be announced; the adjacent copy carries the meaning.

## Dead (do not suggest)

Frequently recommended in old listicles and Reddit threads, verified dead 2026-08:

- `iradesign.io` — no longer resolves
- `error404.fun` — no longer resolves
- `drawkit.io` — dead; the live domain is `drawkit.com`
- `karthiksrinivas.in/charco` — 410 Gone
- `konpa.github.io/devicon` — 404; Devicon lives at `devicon.dev`
- `joeschmoe.io` — **domain expired and re-registered as spam.** Do not link or hotlink it.

Anything from a listicle older than ~2 years: `curl -o /dev/null -w "%{http_code}"` it before recommending.
