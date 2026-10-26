# cache-keeper

A Claude Code mod that keeps the one-hour prompt cache warm while you are away, and stops you from paying for a cold rewrite by accident.

A cache read costs a fraction of a cache write. On Sonnet 5.5, a 200k-token context costs about $0.02 warm and $0.80 when the cache has gone cold. A short ping every 50 minutes keeps the cache read instead of rewritten.

## What it does

- **Keeps the cache warm.** It sends one small request after 50 idle minutes. It never pings a cache that is already cold, because that would pay the rewrite for nobody.
- **Holds a cold send once.** A prompt that would re-write 50k tokens or more of cold cache is refused once, with the price. Send it again to pay it. Plugin prompts and unattended prompts go through.
- **Reports the cost.** A large write logs as a `cold write` when the cache had expired, or as a `cache break` when the cache was still valid but its prefix changed (for example after a mod reload).
- **Handles compaction.** A compaction resets the state. A compaction that no hook reported is detected from the live context size.

Auto mode is on by default. Every turn renews a 24-hour window, so the cache stays warm for as long as the session is open.

## Commands

| Command | Effect |
|---|---|
| `/keepwarm` or `/keepwarm on` | Turn on auto mode. |
| `/keepwarm off` | Turn off auto mode and stop the pings. |
| `/keepwarm 90m` | Keep warm for a fixed window. This turns auto mode off. |
| `/keepwarm status` | Show warm or cold state, context size, cold and warm cost, and the session tally. |
| `/keepwarm guard warn` | Log the cold-send price and send anyway. |
| `/keepwarm guard refuse` | Refuse a cold send once (default). |

## Requirements

- The one-hour cache. Subscription sessions use it by default. API-key sessions need `promptCacheTtl: "1h"`.
- Prices are built in for `claude-fable-5-1`, `claude-opus-5-5` and `claude-sonnet-5-5`. Other models show no price.
- How pings count against subscription plan limits is not documented. Check `/keepwarm status` against your own usage.

## Reach

A mod runs unsandboxed and sees the whole session. This one calls only `$.clock`, `$.model.fork`, `$.session.model`, `$.session.usage`, `$.ui` and `$.command`. It has no file, process or network access of its own. Read `hooks/register.ts` before you install it.

## Install

```
/plugin marketplace add Iah-Uch/clanker-pack
/plugin install cache-keeper@clanker-pack
```

## Credit

The keep-warm timer, the cold-send guard and the price arithmetic follow the design of [cache-tax](https://github.com/karanb192/cache-tax) by Karan Bansal (MIT). See `NOTICE`.

## License

MIT. See `LICENSE`.
