# Placeholders & Fake Data

All endpoints below were verified live. **Dev and demo only** — download and self-host, or generate locally, before anything ships.

## Placeholder images

| Service | Pattern | Notes |
|---|---|---|
| placehold.co | `https://placehold.co/600x400` | Solid blocks with a size label. Full control: `https://placehold.co/600x400/1f2937/f9fafb.png?text=Hello&font=inter`. Formats: `.svg` `.png` `.jpg` `.webp`. SVG is inlineable and weightless. |
| Lorem Picsum | `https://picsum.photos/400/300` | Real photos (Unsplash-sourced). **Use a seed for stability**: `https://picsum.photos/seed/user-1/400/300` — otherwise every render is a different image and screenshots/tests churn. Also `?grayscale`, `?blur=2`. Listing JSON: `https://picsum.photos/v2/list?page=1&limit=10`. |
| DummyImage | `https://dummyimage.com/600x400/000/fff&text=x` | Old reliable, plain. |
| LoremFlickr | `https://loremflickr.com/320/240/dog` | Keyword-matched photos. |
| Cataas | `https://cataas.com/cat` | Cats. Demo decks only. |

Prefer `placehold.co` SVG for layout work (zero network in a data URI) and seeded `picsum` when you need something photo-shaped.

## Placeholder avatars

| Service | Pattern | Notes |
|---|---|---|
| DiceBear | `https://api.dicebear.com/9.x/<style>/svg?seed=<name>` | The best option. Deterministic from the seed, 30+ styles (`initials`, `identicon`, `shapes`, `notionists`, `avataaars`, `bottts`, `glass`). Params: `&size=64&backgroundColor=b6e3f4&radius=50`. Also an npm package for offline generation: `@dicebear/core` + `@dicebear/collection`. |
| UI Avatars | `https://ui-avatars.com/api/?name=Ana+Silva` | Initials on a colored circle. `&background=random&color=fff&size=128&rounded=true&bold=true`. |
| Robohash | `https://robohash.org/<seed>` | Robots/monsters, deterministic. |
| Avataaars | https://getavataaars.com/ | Sketch-style avatar builder; also `avataaars` npm / a DiceBear style. Configure and export SVG. |
| Personas | https://personas.draftbit.com/ | Draftbit's avatar builder, flat illustrated style, free SVG export. |
| Gravatar | `https://gravatar.com/avatar/<sha256-of-email>?d=identicon` | Real service — sends a hash of a real email to a third party. Don't point it at real user emails in a privacy-sensitive product. |

In a product handling real people's records, prefer `initials` or `shapes` styles: a fake human face rendered next to real personal data reads as a real photo of that person.

## Fake structured data

| Tool | Use |
|---|---|
| `@faker-js/faker` | **Default.** `npm i -D @faker-js/faker`. Runs locally (no network, no leak), seedable (`faker.seed(42)`) so fixtures are reproducible, and has pt-BR locale (`import { fakerPT_BR as faker }`) matching this app's copy language. |
| `factory_boy` / Django factories | Backend fixtures. Already the convention for model instances here — use it over hand-rolled objects. |
| https://dummyjson.com/ | Read-only REST API: products, users, carts, posts, todos. Good for wiring a UI before the real endpoint exists. |
| https://jsonplaceholder.typicode.com/ | The classic: posts/comments/todos/users. |
| https://randomuser.me/api/?results=10 | Realistic user records with avatars and locales. |
| https://mockaroo.com/ | Schema-driven CSV/JSON/SQL generation for larger seed sets. |
| MSW (https://mswjs.io/) | Intercept at the network layer instead of stubbing the client. This is the project convention for frontend tests. |

## Lorem ipsum & copy

- `faker.lorem.paragraphs(3)` — no network needed.
- https://loripsum.net/api/5/medium/link/ul — returns real HTML markup (headings, lists, links), better than bare paragraphs for testing prose styles.
- For pt-BR UI, don't ship latin lorem into a design review — generate plausible Portuguese with `fakerPT_BR`, or the layout lies about real text lengths.

## Rules

1. **Seed everything.** Unseeded placeholders make screenshots, visual diffs, and snapshot tests flap.
2. **Never in production.** A placeholder domain in a shipped build is an outage waiting to happen and leaks referrer data. Download the asset, or render a local SVG.
3. **Never as a fallback for missing real data.** A random face where a real avatar failed to load is a correctness bug, not a nicety — it attributes a stranger's likeness to a real record. Render initials or a neutral glyph.
4. **Test realistic extremes**, not just the happy medium: an empty string, a 200-char name, an RTL name, a name with combining accents. `faker` defaults are all comfortably average and hide layout bugs.

## Dead — do not suggest

`via.placeholder.com`, `placekitten.com`, `source.boringavatars.com`, `source.unsplash.com`. All were standard suggestions once; all are dead now. (Boring Avatars still exists as an npm package: `boring-avatars` — the hosted endpoint is what died.)

`joeschmoe.io` (a once-popular avatar API) **expired and was re-registered by a spam operator**. Never hotlink an avatar service that hasn't been checked this year — a dead placeholder domain becomes someone else's content inside your app.
