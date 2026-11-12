For a commercial product, use **D3’s `d3-ease`** if you want a small, focused set of familiar easing functions. It’s MIT licensed and works independently of D3’s rendering stack.

Other good options:

- **Robert Penner’s easing equations**: widely adapted and available in many languages. Check the license of the specific implementation you choose; “Penner easing” alone doesn’t guarantee a particular license.
- ** easings.net**: a useful catalog and reference for CSS-style curves. Check the license of its code or package before incorporating it.
- **GSAP**: polished easing tools in a larger animation library; its standard license permits commercial use, subject to its terms.

For a commercial product, verify the license in the exact package version you ship, including dependencies. MIT and BSD licenses generally allow commercial use with required notices; GPL-family licenses can impose source-sharing obligations. If you need to match CSS precisely, use cubic Bézier easing and implement the curve’s time-to-progress inversion.