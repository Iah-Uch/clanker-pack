### Part 1 — Findings

| Before | After | Why |
| --- | --- | --- |
| `transition: all 600ms ease-in` at [tooltip.css:1](/tmp/bench2-pyqaw20o/repo/src/tooltip.css:1) | `transition: opacity 150ms cubic-bezier(0.23, 1, 0.32, 1)` | `all` can animate unintended properties. The 600ms duration exceeds the 300ms UI budget and the 125–200ms tooltip range; `ease-in` makes the entrance feel slow to respond. |
| No reduced-motion handling at [tooltip.css:1](/tmp/bench2-pyqaw20o/repo/src/tooltip.css:1) | Add a `prefers-reduced-motion` rule that removes or shortens the transition | The tooltip’s opacity transition currently runs unchanged when reduced motion is requested. |

### Part 2 — Verdict

**Feel-breaking regressions:** The 600ms `ease-in` makes a small, frequently seen tooltip feel sluggish.

**Accessibility:** The transition does not honor reduced-motion preferences.

**Verdict: Block.** The duration and easing violate the review bar for UI motion.