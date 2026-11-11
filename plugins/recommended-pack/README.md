# recommended-pack

A bundle. It has no code of its own. Installing it installs 14 plugins from other authors, through Claude Code plugin dependencies. Every one has 15k or more GitHub stars, or comes from Anthropic's own marketplace.

## What it installs

| Plugin | Marketplace | Job |
|---|---|---|
| [context-mode](https://github.com/mksglu/context-mode) | `context-mode` | Keeps large tool output out of the context. Indexes session events for recall after compaction. |
| [ai-memory](https://github.com/akitaonrails/ai-memory) | `ai-memory` | Long-term memory across sessions and agents, with a handoff at the end of each session. |
| [superpowers](https://github.com/obra/superpowers) | `claude-plugins-official` | Brainstorm, plan and test-driven workflow with subagents. |
| frontend-design | `claude-plugins-official` | Anthropic skill for distinctive, production-grade UI. |
| code-review | `claude-plugins-official` | Anthropic review of a PR or a diff. |
| security-guidance | `claude-plugins-official` | Anthropic security review of generated code. |
| [context7](https://github.com/upstash/context7) | `claude-plugins-official` | Live, version-correct library docs through an MCP server. |
| skill-creator | `claude-plugins-official` | Create, improve and benchmark skills. |
| hookify | `claude-plugins-official` | Create hooks from plain markdown rules. |
| [caveman](https://github.com/JuliusBrussee/caveman) | `caveman` | Terse-answer mode that cuts output tokens. |
| [taste-skill](https://github.com/Leonxlnx/taste-skill) | `taste-skill` | Anti-slop skill for landing pages and portfolios, with a real-browser check. Not for dashboards. |
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | `karpathy-skills` | One skill with four rules that cut common LLM coding mistakes. |
| [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `ui-ux-pro-max-skill` | Searchable local database of UI styles, palettes, font pairings, charts and stack guidelines. |
| [mattpocock-skills](https://github.com/mattpocock/skills) | `mattpocock` | Engineering skills: grilling, spec, tickets, TDD, bug diagnosis. |

## Install

1. Install the bundle. This marketplace lists the third-party plugins itself, so you add no other marketplace. `claude-plugins-official` is set up by Claude Code.

   ```
   /plugin marketplace add Iah-Uch/clanker-pack
   /plugin install recommended-pack@clanker-pack
   ```

2. Install the ai-memory binary. The plugin does not contain it. Without the binary, ai-memory captures nothing. See the [ai-memory install guide](https://github.com/akitaonrails/ai-memory#install).

## Not in the bundle

[TokenEconomizer](https://github.com/microsoft/TokenEconomizer) from Microsoft is not a dependency. Its installed plugin runs from a local clone of the repository, so a bundle cannot install it. Install it by hand from its README.

If you install it next to this bundle, set `toolprune_protect` to `mcp__plugin_context-mode_context-mode__*`. Without it, TokenEconomizer can add context-mode's tools to a project deny list after a few sessions without use. Nobody has tested the combination.

## Notes

- The marketplace lists each third-party plugin as its own entry, pinned to a full commit that was reviewed. An upstream push changes nothing for you. A new version of this bundle moves the pin.
- Anthropic's plugins come from `claude-plugins-official`. Each one follows the latest release of that marketplace.
- If you already installed one of these plugins from its own marketplace, such as `context-mode@context-mode`, uninstall it first. Two copies run their hooks twice.
- Fourteen plugins add to every session's context. MCP servers cost the most: context7. Run `/context` to see what each one costs.
- superpowers, code-review, security-guidance and mattpocock-skills overlap in places. Disable the one you do not use.
- ui-ux-pro-max ships an unpinned `npx -y` MCP config in `stack/.mcp.json`. Claude Code does not load it, because it is not at the plugin root. Do not copy it into a project.
- The karpathy repository has no license file on GitHub. Its `plugin.json` says MIT.
- Each plugin adds hooks to your sessions. Read what they store before you use them on a repository with sensitive data.
- Claude Code refuses to disable a plugin that another enabled plugin still needs. To remove one, run `/plugin uninstall recommended-pack` first.
