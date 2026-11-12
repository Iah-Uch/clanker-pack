| Before | After | Why |
| --- | --- | --- |
| `transition: all 600ms ease-in` in `src/tooltip.css:1` | Specify `opacity` only, use a responsive ease-out curve, and keep the duration under 300ms | `all` can animate unintended properties; 600ms exceeds the UI budget, and `ease-in` delays the visible response. |

## Verdict

**Feel-breaking regressions:** The tooltip’s 600ms ease-in entrance is sluggish and exceeds the 300ms UI budget.

**Performance:** `transition: all` leaves unrelated properties open to animation.

**Accessibility:** The change adds no reduced-motion handling. If the tooltip moves as part of its entrance, respect `prefers-reduced-motion`.

**Block** — fix the duration and easing and narrow the transition before merging.