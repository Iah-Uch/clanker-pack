# recommended-core

A bundle. It has no code of its own. Installing it installs 5 plugins from other authors, through Claude Code plugin dependencies. It needs no extra binary.

| Plugin | Job |
|---|---|
| context-mode | Keeps large tool output out of the context. Indexes session events for recall after compaction. |
| superpowers | Brainstorm, plan and test-driven workflow with subagents. |
| security-guidance | Anthropic security review of generated code. |
| context7 | Live, version-correct library docs through an MCP server. |
| code-review | Anthropic review of a PR or a diff. |

Install:

```
/plugin install recommended-core@clanker-pack
```

For the other plugins, see `recommended-extras` and `recommended-memory`. For all 15 in one step, see `recommended-pack`.
