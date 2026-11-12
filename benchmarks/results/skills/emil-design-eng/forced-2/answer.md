Updated [button.css](/tmp/bench2-akuja04q/repo/src/button.css) with a subtle lift and color shift on hover, plus a quick scale-down press state. Transitions now target specific properties with responsive easing; hover is limited to mouse-like pointers, and reduced-motion settings avoid movement.

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms ease-in` | Targeted transitions with a quick custom ease-out | Gives immediate feedback without animating unrelated properties or feeling sluggish. |
| `:hover { transform: scale(0) }` | Subtle hover lift; `:active { transform: scale(0.97) }` | Keeps the button visible while adding a clear press response. |

I didn’t run tests.