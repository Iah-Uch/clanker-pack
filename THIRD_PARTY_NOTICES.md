# Third-party notices

Four skills and one mod in this repository come from other projects. All upstream repositories use the MIT license. Their copyright notices and the MIT permission notice follow.

| Skill | Upstream repository | Upstream path | Relation to upstream |
|-------|---------------------|---------------|----------------------|
| `stack-pack/docker-expert` | [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | `cli-tool/components/skills/development/docker-expert/SKILL.md` | Identical |
| `tools-pack/mermaid-diagrams` | [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | `cli-tool/components/skills/creative-design/mermaid-diagrams/SKILL.md` | Identical. [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) publishes a near-identical copy. |
| `stack-pack/python-patterns` | [vudovn/ag-kit](https://github.com/vudovn/ag-kit) | `.agents/skills/python-patterns/SKILL.md` | Near-identical. Small differences. |
| `ui-pack/tailwind-patterns` | [vudovn/ag-kit](https://github.com/vudovn/ag-kit) | `.agents/skills/tailwind-patterns/SKILL.md` | Near-identical. Small differences. |
| `cache-keeper` (mod) | [karanb192/cache-tax](https://github.com/karanb192/cache-tax) | `hooks/register.ts` | Rewritten. The keep-warm timer, the cold-send guard and the price arithmetic follow its design. It adds auto mode, cache-break detection and compaction handling, and drops the store, the band and the images. |

Each skill row was checked on 2026-10-18 by comparing the file in this repository with the file in the upstream repository.

The `generative-pack` skills, `ui-pack/design-asset-sourcing` and the `reread-guard` mod were written for this repository. The `generative-pack` references name open-source projects as examples of each technique. They do not vendor those projects.

## Copyright notices

Copyright (c) 2025 Daniel (San) Ávila  
Copyright (c) 2026 VUDOVN  
Copyright (c) 2026 Leonardo Flores  
Copyright (c) 2026 Karan Bansal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
