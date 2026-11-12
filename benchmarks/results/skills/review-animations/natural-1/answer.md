| Before | After | Why |
| --- | --- | --- |
| `transition: all 600ms ease-in` in [tooltip.css](/tmp/bench2-p6mgq5e8/repo/src/tooltip.css:1) | `transition: opacity 150ms ease-out` | `all` can animate unintended properties, and `ease-in` makes the tooltip appear sluggish. At 600ms, it also exceeds the 300ms UI budget. |

## Verdict

**Feel-breaking regressions:** The 600ms `ease-in` fade is slow for a tooltip and delays its appearance.

**Accessibility:** The new transition has no reduced-motion handling. Consider honoring `prefers-reduced-motion`.

**Block** — the easing and duration violate the review criteria.