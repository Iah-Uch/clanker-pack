# Icons & Brand Logos

## UI icon sets — pick ONE per product surface

| Set | URL | Count | License | Character |
|---|---|---|---|---|
| Lucide | https://lucide.dev/ | 1500+ | ISC | Actively maintained Feather fork. The safe default for React/Vue/Svelte — first-party packages. |
| Heroicons | https://heroicons.com/ | 300+ | MIT | Tailwind team. Outline/solid/mini/micro. Pairs perfectly with Tailwind sizing. |
| Phosphor | https://phosphoricons.com/ | 9000+ | MIT | Six weights (thin→fill). Best when you need weight variation as a design device. |
| Tabler | https://tabler.io/icons | 5800+ | MIT | Largest consistent stroke set. Great coverage of obscure glyphs. |
| Radix Icons | https://www.radix-ui.com/icons | 300+ | MIT | 15×15 grid, crisp at small sizes. Natural fit next to Radix primitives. |
| Iconoir | https://iconoir.com/ | 1500+ | MIT | 24×24 grid, open source, no tracking. |
| Material Symbols | https://fonts.google.com/icons | 2500+ | Apache 2.0 | Variable font: weight/fill/grade/optical-size are axes. Use when the design is Material. |
| Bootstrap Icons | https://icons.getbootstrap.com/ | 2000+ | MIT | Fine standalone, no Bootstrap needed. |
| Remix Icon | https://remixicon.com/ | 2800+ | Apache 2.0 | Line + fill pairs. |
| CSS.gg | https://css.gg/ | 700+ | MIT | Icons rendered in pure CSS — zero image requests, but hard to tweak. |
| Teeny Icons | https://teenyicons.com/ | — | MIT | 1px minimal, for dense UIs. |
| System UI Icons | https://systemuicons.com/ | — | Free | Consistent, understated. |
| IconMonstr | https://iconmonstr.com/ | 4500+ | Free | Older, broad, organized in collections. |
| Flaticon | https://www.flaticon.com/ | huge | Free w/ attribution | Enormous but attribution-required and ad-heavy. Use only when nothing MIT covers the glyph. |
| Icons8 | https://icons8.com/ | huge | Free w/ link attribution | Many styles incl. colored/3D/emoji (`/icons/set/emoji`). Attribution required on free tier. |

### Domain-specific glyphs

- **Dev/tech stack logos**: https://devicon.dev/ (600+ language/tool icons, font + SVG)
- **Game/fantasy/RPG**: https://game-icons.net/ (4000+, CC-BY 3.0)
- **Emoji as icons**: https://icons8.com/emoji · https://openmoji.org/ (CC-BY-SA) · https://github.com/twitter/twemoji (CC-BY 4.0)

## Metasearch — use these to FIND, then fetch from the set's own CDN

- **Iconify** https://icon-sets.iconify.design/ — 200k+ icons across 150+ sets, plus a free HTTP API (see recipes). The single most useful entry point.
- **Icônes** https://icones.js.org/ — nicer UI over Iconify; bulk-select and export.
- **Icon Duck** https://iconduck.com/ — 100k+ open-source icons, license shown per item.
- **SVG Repo** https://www.svgrepo.com/ — 500k+, mixed licenses.
- **Icon Search** https://iconsear.ch/ — searches SVGs on GitHub/GitLab.
- **The Noun Project** https://thenounproject.com/ — 20m+, but free tier demands attribution. Last resort.

### Empty-state / status glyphs worth knowing (lucide names)

`inbox` · `file-search` · `folder-search` · `folder-open` · `search-x` · `archive` · `clipboard-list` · `database` · `chart-no-axes-column` · `circle-off` · `filter-x` · `wifi-off` · `triangle-alert` · `circle-check-big`

Pick by *why* it's empty: `file-search` / `search-x` / `filter-x` = a query matched nothing; `inbox` / `folder-open` = nothing exists yet; `wifi-off` / `triangle-alert` = it failed to load. Using the same glyph for all three throws away the only signal the user gets.

### Iconify API (no key, CORS-open)
```bash
curl -s "https://api.iconify.design/search?query=stethoscope&limit=20" | jq '.icons'
curl -s "https://api.iconify.design/tabler/stethoscope.svg" -o icon.svg
curl -s "https://api.iconify.design/lucide/activity.svg?color=%23ef4444&height=32"
curl -s "https://api.iconify.design/collections" | jq 'keys'
```
Query returns `prefix:name` pairs — the prefix is the set (`lucide`, `tabler`, `ph`, `mdi`, `heroicons`).

Caveats:
- Search matches **names, not concepts** — `query=empty` returns almost nothing useful. Search the object you want to draw (`folder`, `file`, `inbox`), then scan the returned list.
- Iconify tracks upstream, so a name it returns may not exist in your *installed* version. Confirm before importing: `ls node_modules/lucide-react/dist/esm/icons/ | grep '^file-search'`.
- If a shell proxy is summarizing JSON bodies (see SKILL.md), re-run the call in raw passthrough mode.

## Brand logos

| Source | URL | Notes |
|---|---|---|
| Simple Icons | https://simpleicons.org/ | 3000+ brand marks, CC0 *files*. CDN: `https://cdn.simpleicons.org/<slug>` and `https://cdn.simpleicons.org/<slug>/<color>`. |
| SVGL | https://svgl.app/ | Modern logo search, includes wordmarks and dark variants. API: `https://api.svgl.app`, `https://api.svgl.app/categories`. |
| VectorLogoZone | https://www.vectorlogo.zone/ | Consistently formatted, predictable URL scheme, good for tech stack grids. |
| LogoSearch | https://logosear.ch/ | Metasearch over ~200k SVG logos on GitHub. |
| World Vector Logo | https://worldvectorlogo.com/ | Broad but ad-heavy. |
| Seek Logo | https://seeklogo.com/ | Legacy brands. |
| AWS Icons | https://awsicons.dev/ · Azure: https://az-icons.com/ · macOS: https://macosicons.com/ | Cloud/architecture diagrams. |

**Trademark rule:** the SVG file may be CC0, the mark is not. Use logos only to identify the real thing (integration lists, "Sign in with X", tech-stack pages). Never recolor a brand mark arbitrarily, never use it as decoration, never imply partnership.

## Implementation rules

- **Never use icon fonts.** They break with `font-display`, are unreadable to screen readers, and fail on font-blocking. SVG only.
- **One set per surface.** Mixed stroke widths and grids look broken. If a glyph is missing from your set, check that set's GitHub issues before importing a foreign one — or draw the missing one to match the grid.
- **`currentColor`**: strip `fill="#000"` / `stroke="#000"` so CSS drives the color. Keep `viewBox`, drop `width`/`height`.
- **Decorative vs meaningful**: decorative icon → `aria-hidden="true"`; icon-only button → `aria-label`.
- **Tree-shake**: `import { Home } from "lucide-react"` (per-icon), never a barrel import of the whole set.
- **Optical sizing**: a 24px-grid icon at 16px looks mushy. Use the set's small variant (Heroicons mini/micro, Material's optical size axis).
