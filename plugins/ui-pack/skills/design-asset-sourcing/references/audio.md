# Sound & Music

Rarely needed in an app UI — mostly for demos, videos, and onboarding.

## Sound effects

| Source | URL | License |
|---|---|---|
| Freesound | https://freesound.org/ | Per-clip CC (CC0 / CC-BY). Check each one; attribution often required. |
| Mixkit | https://mixkit.co/free-sound-effects/ | Free, no attribution. |
| Zapsplat | https://www.zapsplat.com/ | Free with attribution, paid tier removes it. |
| Pixabay SFX | https://pixabay.com/sound-effects/ | Pixabay license, no attribution. |
| Kenney | https://kenney.nl/assets?q=audio | CC0 game audio packs. |

## Music

| Source | URL | Notes |
|---|---|---|
| YouTube Audio Library | https://studio.youtube.com/ (Audio Library) | Free, clearly licensed, huge. Requires a Google account. |
| Pixabay Music | https://pixabay.com/music/ | Free, no attribution. |
| Free Music Archive | https://freemusicarchive.org/ | Per-track CC. |
| CC Hound | https://cchound.com/ | Curated CC audio. |
| Loyalty Freak Music | https://loyaltyfreakmusic.com/ | CC0 albums. |
| Epidemic Sound / Soundstripe / Artlist | https://www.epidemicsound.com/ | Paid subscriptions — the safe answer for anything commercial and public. |

## Tools

- https://www.audacityteam.org/ — editing
- `ffmpeg` — normalize, trim, convert (`-af loudnorm` for consistent levels)
- https://use-sound.vercel.app/ — React hook for UI sound (`use-sound`)
- https://sfxr.me/ — generate retro 8-bit SFX in-browser

## Rules

- **Never autoplay audio.** Browsers block it and users hate it.
- UI sound is opt-in, off by default, and must respect the OS mute. In a professional or operational tool, default to silence.
- YouTube/Instagram will content-ID a track even if a random site called it "free" — for anything published, use a source with a written license page and save a copy of it.
- Normalize levels across clips. Uneven loudness is the most common amateur tell.
