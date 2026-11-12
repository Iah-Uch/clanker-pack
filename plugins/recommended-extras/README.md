# recommended-extras

A bundle. It has no code of its own. Installing it installs 9 optional plugins from other authors, through Claude Code plugin dependencies. Each one adds skill descriptions to every session, so install only the ones you use.

| Plugin | Job |
|---|---|
| frontend-design | Anthropic skill for distinctive, production-grade UI. |
| skill-creator | Create, improve and benchmark skills. |
| hookify | Create hooks from plain markdown rules. |
| cache-tax | Keeps the one-hour prompt cache warm during breaks and asks before a cold send. Keep-warm requests cost tokens. Needs Claude Code 2.1.287 or later. |
| caveman | Terse-answer mode that cuts output tokens. It changes how Claude writes to you. |
| taste-skill | Anti-slop skill for landing pages and portfolios, with a real-browser check. Not for dashboards. |
| andrej-karpathy-skills | One skill with four rules that cut common LLM coding mistakes. |
| ui-ux-pro-max | Searchable local database of UI styles, palettes, font pairings, charts and stack guidelines. |
| mattpocock-skills | Engineering skills: grilling, spec, tickets, TDD, bug diagnosis. |

Install:

```
/plugin install recommended-extras@clanker-pack
```

The core set is in `recommended-core`. For the full details and links, see the `recommended-pack` README.
