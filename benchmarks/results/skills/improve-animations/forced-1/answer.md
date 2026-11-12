## Motion audit

The app is a minimal React 18 shell with three CSS motion rules and no shared motion tokens. Based on the code, the UI appears to call for restrained interaction feedback. The most frequent motion is the row hover; the modal and menu are occasional interactions.

| # | Severity | Category | Location | Finding | Fix summary |
|---|---|---|---|---|---|
| 1 | HIGH | Purpose & frequency | [src/list.css:1](/tmp/bench2-uoruv0np/repo/src/list.css:1) | Hover starts an infinite 900ms wiggle, and [line 2](/tmp/bench2-uoruv0np/repo/src/list.css:2) animates `margin-left`. This repeats during a common interaction and triggers layout. | Remove the continuous wiggle. If hover feedback is needed, use a subtle, finite transition on `transform` or `opacity`, gated to fine pointers. |
| 2 | HIGH | Easing & duration; physicality & origin | [src/modal.css:1](/tmp/bench2-uoruv0np/repo/src/modal.css:1) | The modal opens from `scale(0)` with `transition: all 400ms ease-in`. It starts slowly, hides the element at the closed endpoint, and runs longer than the under-300ms budget for ordinary UI transitions. | Use opacity plus a small scale range (`0.9–0.97` to `1`), explicit properties, and `ease-out`. Consider 200–300ms for the modal transition. |
| 3 | HIGH | Easing & duration; performance | [src/menu.css:1](/tmp/bench2-uoruv0np/repo/src/menu.css:1) | The menu animates `width` over 500ms with `ease-in`, delaying response and causing layout work throughout the transition. | Prefer a transform/opacity entrance if the menu can overlay content. If width must change layout, use a deliberate movement transition with `ease-in-out` and a shorter duration. |

**Missed opportunities**

- There’s no reduced-motion handling for any of these motion rules.
- Menu opening has no spatial cue tying it to its trigger; a small transform and opacity entrance could clarify the relationship if the menu is trigger-anchored.

No plans were written yet. The skill’s workflow asks me to stop here and let you choose which findings should become implementation plans.