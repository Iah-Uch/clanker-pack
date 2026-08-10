# Mockups, Screenshots & Motion

For READMEs, release notes, landing pages, decks, changelogs.

## Screenshot beautifiers

| Tool | URL | Notes |
|---|---|---|
| shots.so | https://shots.so/ | Best free one. Backgrounds, device frames, 3D rotation, padding. |
| Pika | https://pika.style/ | Templates for tweets, code, screenshots; browser frames. |
| Screenshot.rocks | https://screenshot.rocks/ | Quick browser/phone mockup from a URL or upload. |
| Screenstab | https://www.screenstab.com/ | Angled 3D perspective shots. |
| Shotsnapp | https://shotsnapp.com/ | Device presentation frames. |
| Brandbird | https://www.brandbird.app/ | Social/marketing image composer. |
| Ray.so | https://ray.so/ | Beautiful code snippet images. |
| Carbon | https://carbon.now.sh/ | The original code-screenshot tool. |

## Device frames

- https://facebook.design/devices — official Apple/Android/desktop frames, free
- https://www.ls.graphics/devices-mockups — free + paid device mockups
- https://deviceshots.com/ — browse by device
- https://rotato.app/ — 3D animated device video (paid, best-in-class)
- https://deviceful.netlify.app/ — free device animation

## Screen recording → shareable

- https://www.screen.studio/ — auto-zoom, smooth cursor, macOS (paid)
- https://github.com/faressoft/terminalizer · https://asciinema.org/ — terminal recordings; asciinema embeds as text, not video
- https://github.com/charmbracelet/vhs — **scripted terminal GIFs from a `.tape` file** — reproducible, diffable, perfect for CLI docs
- `ffmpeg` + `gifski` for a good-quality GIF from any mp4

## Book / product mockups

- https://3dbook.xyz/ · https://3d-book-css.netlify.app/ (CSS-only) · https://diybookcovers.com/3Dmockups/

## Motion & micro-interaction

| Tool | URL | Notes |
|---|---|---|
| Motion (ex Framer Motion) | https://motion.dev/ | The default React animation library. |
| Auto-Animate | https://auto-animate.formkit.com/ | One line, animates list add/remove/reorder. Highest value per effort. |
| Rough Notation | https://roughnotation.com/ | Hand-drawn highlight/underline/circle annotations — great for onboarding callouts. |
| LottieFiles | https://lottiefiles.com/ | Free Lottie animations; big library of loaders and success states. |
| Animate.css | https://animate.style/ | Drop-in CSS keyframes. |
| Transformicons | http://www.transformicons.com/builder.html | Animated icon state transitions (hamburger→X). |
| Loading.io | https://loading.io/ | Spinners and animated backgrounds. |
| Epic Spinners | https://epic-spinners.epicmax.co/ | Free CSS spinners. |

## Rules

- **Always honor `prefers-reduced-motion`.** Non-negotiable, especially in a health app.
- GIFs are enormous. Prefer mp4/webm in a `<video autoplay muted loop playsinline>`, or an animated WebP. GitHub READMEs accept mp4 uploads.
- Redact before publishing a screenshot: no real names, IDs, dates of birth, emails, or tokens. Generate the screenshot from seeded fake data (see `placeholders-and-fake-data.md`), never from a dev DB holding real records.
- A mockup frame that hides UI detail is decoration. For docs, a clean cropped screenshot beats a tilted 3D laptop.
