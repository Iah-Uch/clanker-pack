**Finding — the transition can animate every changed property.** In [src/tooltip.css](/tmp/bench2-1srlcych/repo/src/tooltip.css:1), `transition: all` applies to any animatable property that changes on `.tooltip`, which can cause unintended or costly animations. Scope it to `opacity`:

```css
.tooltip { opacity: 0; transition: opacity 600ms ease-in; }
```

The `.show` rule changes opacity as expected. I couldn’t verify how the class is applied: the only other source file, `src/App.jsx`, renders an empty `<main />`, and there are no tooltip callers in the repo.