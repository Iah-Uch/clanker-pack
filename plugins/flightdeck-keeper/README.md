# flightdeck-keeper

[Flightdeck](https://github.com/scasella/claude-flightdeck) by Stephen Casella (MIT), with the prompt-cache keeper from `cache-keeper` built in. One mod replaces both: one status line entry, one log, and one cache line in the main panel instead of a second mod.

## What changed from Flightdeck

- The main panel shows one cache line: warm time left, or cold with the price of a rewrite.
- The status line shows `cache 42m` or `cache cold` next to the context fill.
- Cache events (`cold write`, `cache break`, a cold send that went through) go to the Flightdeck log.
- `/keepwarm` works as in `cache-keeper`: `on`, `off`, a window such as `90m`, `status`, `guard warn|refuse`.
- A cold send of 50k tokens or more is held once with its price. Send it again to pay it.

- Two Flightdeck hooks are removed: `classic.UserPromptSubmit` and `session.append`. A security plugin that runs above mods bypasses both, and each bypass printed a notice into the chat. The permission mode still comes from `turn.start`. The server-side `advisor` tool is no longer tracked; a subagent architect still is.

Everything else is Flightdeck 0.5.1. Its commands and settings are unchanged. See its README for the panels.

## Install

```
/plugin marketplace add Iah-Uch/clanker-pack
/plugin install flightdeck-keeper@clanker-pack
```

Remove `flightdeck` and `cache-keeper` first. Running them together draws two panes and sends two pings.

## Credit

Flightdeck: Stephen Casella, MIT. The keep-warm timer, the cold-send guard and the price arithmetic follow [cache-tax](https://github.com/karanb192/cache-tax) by Karan Bansal, MIT. See `LICENSE` and `NOTICE`.
