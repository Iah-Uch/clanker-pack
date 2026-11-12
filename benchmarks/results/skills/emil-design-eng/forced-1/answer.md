Updated [button.css](/tmp/bench2-skeds_s6/repo/src/button.css) with a subtle color and shadow change on hover, plus a quick scale-down on press. Hover is limited to mouse-like pointers, and reduced-motion settings disable the transform animation.

| Before | After | Why |
| --- | --- | --- |
| `transform: scale(0)` on hover | Slightly darker background and soft shadow | Keeps the button visible while giving clear hover feedback |
| `transition: all 300ms ease-in` | Specific properties with short transitions | Makes feedback quicker and avoids animating unrelated properties |
| No press state | `transform: scale(0.97)` on `:active` | Gives immediate tactile feedback |