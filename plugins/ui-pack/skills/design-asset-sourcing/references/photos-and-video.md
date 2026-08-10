# Stock Photos & Video

## General photo libraries

| Source | URL | License | Notes |
|---|---|---|---|
| Unsplash | https://unsplash.com/ | Unsplash License, no attribution required | Highest quality. Has an official API (needs a free key) — `https://api.unsplash.com/photos/random?client_id=KEY`. |
| Pexels | https://www.pexels.com/ | Pexels License | Photos + video in one place. Free API with key. |
| Pixabay | https://pixabay.com/ | Pixabay License | Photos, video, vectors, music. Free API with key. |
| Burst (Shopify) | https://burst.shopify.com/ | Free, mostly CC0 | Commerce/product-oriented shots. |
| Gratisography | https://gratisography.com/ | Free | Deliberately weird — good when generic stock feels lifeless. |
| PicJumbo | https://picjumbo.com/ | Free | Broad general library. |
| ISO Republic | https://isorepublic.com/ | Free | Minimalist, lots of negative space for text overlay. |
| Negative Space | https://negativespace.co/ | CC0 | Same use case, name says it. |
| Life of Pix | https://www.lifeofpix.com/ | Free | High-res, editorial feel. |
| StockSnap | https://stocksnap.io/ | CC0 | Large searchable CC0 pool. |
| Visual Hunt | https://visualhunt.com/ | CC search | Aggregates 350m+ CC photos — verify each license. |
| AllTheFreeStock | https://allthefreestock.com/ | Aggregator | Directory of free sources; start here when nothing else fits. |
| Flickr Commons | https://www.flickr.com/creativecommons/ | Per-photo CC | Filter by license explicitly; attribution usually required. |

## Representation & niche

- **Nappy** https://www.nappy.co/ — high-res photos of Black and brown people. Use it; default stock is not diverse.
- **Startup Stock Photos** https://startupstockphotos.com/ — the laptop-and-coffee genre, if you must.
- **Artvee** https://artvee.com/ — public-domain fine art, posters, illustrations. Excellent for editorial/blog headers.
- **Free Nature Stock** https://freenaturestock.com/ · **Visuals of Earth** https://visualsofearth.com/ — nature/landscape.
- **NASA Image Library** https://images.nasa.gov/ — public domain, space/earth imagery.
- **Smithsonian Open Access** https://www.si.edu/openaccess — 4M+ CC0 items.
- **Old Book Illustrations** https://www.oldbookillustrations.com/ — PD engravings.

## AI-generated / synthetic

- https://generated.photos/ — AI faces, model-released. Useful for avatars where a real person's likeness is a legal problem.
- https://photos.icons8.com/creator/ — compose stock scenes from parts.

Synthetic faces avoid likeness/consent issues. Never use a real stock photo of a person in a way that implies they are a real customer, user, or subject of your product.

## Video & motion

| Source | URL | Notes |
|---|---|---|
| Pexels Video | https://www.pexels.com/videos/ | Free, no attribution. |
| Pixabay Video | https://pixabay.com/videos/ | Free. |
| Mixkit | https://mixkit.co/ | Free video, music, SFX, and art. |
| Coverr | https://coverr.co/ | Hero background loops specifically. |
| Videvo | https://www.videvo.net/ | Mixed free/paid, check per clip. |

## Image tools

- Background removal: https://www.remove.bg/ · https://www.photoroom.com/background-remover · https://pixian.ai/ · offline/browser: https://github.com/imgly/background-removal-js
- Object removal: https://cleanup.pictures/
- Colorize B&W: https://palette.fm/
- Video/GIF background removal: https://www.unscreen.com/
- Compression: `squoosh` CLI, `sharp`, or https://squoosh.app/

**Hard rule:** never upload user-supplied photos or anything containing regulated/personal data to these services — they are third-party processors, and in most compliance regimes that upload is a disclosure. Browser-local tools (imgly) or local `sharp`/ImageMagick only, for anything real.

## Delivery rules

- Serve AVIF/WebP with a JPEG fallback; `<picture>` or a framework image component.
- Always set `width`/`height` (or `aspect-ratio`) to prevent CLS.
- `loading="lazy"` below the fold, `fetchpriority="high"` on the LCP image only.
- Blur-up placeholder: generate a BlurHash (https://blurha.sh/) or a 20px base64 thumbnail at build time.
- Self-host. Hotlinking Unsplash in production is slow and can break.

## Dead

- `source.unsplash.com` (random-image endpoint) — retired. Use the API with a key, or picsum for placeholders.
