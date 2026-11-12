Updated [.claude/settings.json](/tmp/bench2-0b9baazx/repo/.claude/settings.json) for shorter, cheaper, faster sessions:

- Defaults to the `haiku` model.
- Sets effort to `low` and caps it there.
- Lowers the auto-compaction window from 800,000 to 100,000 tokens.

The JSON parses successfully. Anthropic documents Haiku as its fastest and most cost-efficient model family, and low effort for short, latency-sensitive tasks. [Model overview](https://docs.anthropic.com/en/docs/about-claude/models/overview) · [Claude Code settings reference](https://code.claude.com/docs/en/settings-reference)