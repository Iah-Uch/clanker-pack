Updated [sidebar.css](/tmp/bench2-6f0cyc3e/repo/src/sidebar.css): the sidebar now opens with `transform: translateX()` instead of animating `left`, avoiding layout work on each frame. The transition is limited to `transform` rather than `all`.

Verified the change in code; smoothness still needs a recording on a real phone to confirm.