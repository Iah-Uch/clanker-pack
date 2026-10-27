# Changelog

## 0.1.1

- Removed the `classic.UserPromptSubmit` and `session.append` hooks. The engine bypasses them and printed a notice into the chat each time. Server-side advisor tracking goes with them.

## 0.1.0

- Forked from Flightdeck 0.5.1.
- Folded in the `cache-keeper` 0.1.0 logic: keep-warm pings, the cold-send guard, `/keepwarm`.
- Cache state shows as one line in the main panel, one piece of the status line and entries in the log.
