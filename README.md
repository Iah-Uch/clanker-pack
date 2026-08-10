# clanker-pack

A personal Claude Code plugin marketplace — 23 skills across 5 focused packs. Each pack is a plugin you install independently; each skill loads only when its triggers match, so you carry the capability without paying the context cost until you need it.

## Install

```
/plugin marketplace add Iah-Uch/clanker-pack

/plugin install senior-pack@clanker-pack    # role-level engineering depth
/plugin install ui-pack@clanker-pack         # design systems, theming, perf
/plugin install quality-pack@clanker-pack    # review, debugging, git, guidelines
/plugin install tools-pack@clanker-pack      # diagrams, PDFs, testing, file org
/plugin install stack-pack@clanker-pack      # Docker, Python, security & compliance
```

Update after new skills land:

```
/plugin marketplace update clanker-pack
```

## At a glance

| Pack | Skills | Focus |
|------|:------:|-------|
| **senior-pack** | 6 | Senior-role engineering: architecture, backend, frontend, fullstack, QA, security |
| **quality-pack** | 5 | How the work gets done well: code review, debugging, git discipline, guidelines, writing |
| **ui-pack** | 5 | Design systems, Tailwind v4, theming, asset sourcing, web performance |
| **tools-pack** | 4 | Diagrams, PDF processing, web-app testing, file organization |
| **stack-pack** | 3 | Stack-specific depth: Docker, Python, security & compliance |

## Packs

### senior-pack — role-level engineering
Skills that behave like a senior engineer in a given discipline: opinionated, trade-off-aware, stack-specific.

- **senior-architect** — system design, architecture diagrams, tech-stack decision frameworks, dependency analysis, integration patterns.
- **senior-backend** — API scaffolding, database optimization, auth, business logic, performance tuning (Node, Express, Go, Python, Postgres, GraphQL, REST).
- **senior-frontend** — component scaffolding, performance/bundle optimization, state management, UI best practices (React, Next.js, TypeScript, Tailwind).
- **senior-fullstack** — end-to-end project scaffolding, code-quality analysis, architecture patterns, dev-workflow setup.
- **senior-qa** — test strategy, suite generation, coverage analysis, E2E setup, quality metrics.
- **senior-security** — security architecture, penetration testing, threat modeling, crypto implementation, audits.

### quality-pack — how the work gets done
The discipline layer: process skills that keep output correct, reviewable, and honestly reported.

- **code-reviewer** — automated analysis, best-practice and security scanning, review checklists (TS/JS, Python, Swift, Kotlin, Go).
- **coding-guidelines** — behavioral guardrails that cut common LLM coding mistakes during implementation.
- **git-workflow** — atomic commits, why-focused conventional messages, the human-approval gate before committing, feature-branch flow, `--no-ff` merges, human-only authorship.
- **systematic-debugging** — reproduce → read the error → hypothesize → test → fix at root cause, before proposing changes.
- **content-research-writer** — research-backed writing with citations, hooks, outline iteration, and section-level feedback.

### ui-pack — design & front-of-house
- **ui-design-system** — design tokens, component docs, responsive calculations, design→dev handoff.
- **tailwind-patterns** — Tailwind v4 CSS-first config, container queries, design-token architecture.
- **theme-factory** — apply one of 10 preset themes (or generate one) to slides, docs, reports, landing pages.
- **design-asset-sourcing** — vetted library of free illustrations, icons, SVG logos, stock photos, placeholders, patterns, fonts, palettes, UI blocks and mockup tools, with verified fetch endpoints, license rules, and a gate on whether the task needs an asset at all.
- **web-performance-optimization** — Core Web Vitals, loading speed, bundle size, caching, runtime performance.

### tools-pack — utilities
- **mermaid-diagrams** — class, sequence, flowchart, ERD, C4, state, git-graph, gantt diagrams from plain requests.
- **pdf-processing-pro** — production PDF workflows: forms, tables, OCR, validation, batch operations.
- **webapp-testing** — drive and test local web apps with Playwright: verify UI, capture screenshots, read browser logs.
- **file-organizer** — context-aware cleanup: dedupe, restructure, and reorganize directories.

### stack-pack — stack-specific depth
- **docker-expert** — multi-stage builds, image-size optimization, container security, Compose orchestration, prod deployment.
- **python-patterns** — framework selection, async patterns, type hints, project structure — teaches the decision, not a copy-paste.
- **security-compliance** — defense-in-depth architecture, SOC2/ISO27001/GDPR/HIPAA compliance, threat modeling, incident response, secure SDLC.

## Design heuristics

The packs share a point of view:

- **Skills teach judgment, not recipes.** The Python and Tailwind skills explicitly teach *how to decide*, not snippets to paste.
- **Trigger-scoped loading.** A skill's description is a precise "use when…" so Claude loads it exactly when relevant and ignores it otherwise — keeping context lean.
- **Process before implementation.** Debugging, review, and git skills gate *how* work happens; they run before the domain skills that do it.
- **The human owns and approves the work.** Nothing commits without explicit approval, and work is never attributed to the AI.
- **One capability per skill.** Small, composable, independently installable — pick the packs you want.

## Attribution

Not everything here is mine. This repo is a mix of skills I built and ones I found useful around the web and collected into one place. Credit for the latter belongs to their original authors.

## License

MIT
