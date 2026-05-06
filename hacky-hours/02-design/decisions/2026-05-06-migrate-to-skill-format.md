# ADR: Migrate from slash command to SKILL.md format

**Date:** 2026-05-06
**Status:** Accepted (with two-tier model corrected after first real-session test — see Amendments below)
**Relates to:** ARCHITECTURE.md, install.sh, install.ps1, README.md, command prompt
**Research input:** `02-design/research/2026-05-06-skill-vs-slash-command.md`
**Coupled with:** Two-tier design artifacts spike (see BACKLOG)

## Amendments

**2026-05-06 (same day, post-first-test):** First real-session test on a toy tamagotchi project surfaced that the originally-described two-tier model (summary as source of intent, deep doc as expansion) had the polarity inverted: only summary docs got generated, the build worked from those alone, and the deep docs never materialized. Corrected model:

- **Deep dive (`<DOC>-deep.md`) is the source of truth.** Built first via Step 2 questions. Step 4 reads it for build. Implementation Notes live here.
- **Summary (`<DOC>-summary.md`) is a derivative.** Generated from the deep dive after signoff. Never adds new information; never makes new decisions. For quick gut checks and as a navigation onramp for non-technical readers, with cross-links into deep-dive sections.
- If summary and deep dive disagree, the summary is wrong — regenerate it.

This inversion is the correct framing: it's how technical writing actually works (specs come first, executive summaries derive from them), and it gives the deep dive a real forcing function (it's what gets built from). The prior framing left the deep doc with no job, so it never got written.

Templates, Step 2 / Step 4 instructions, audit / optimize / pivot guidance, learn 1, and tools/upgrade Flow A all updated to reflect the corrected model.

## Context

`hacky-hours` ships as a Claude Code slash command at `~/.claude/commands/hacky-hours.md` — a single Markdown file Claude reads when the user types `/hacky-hours`. The file is ~1,500 lines and grows with every step, review mode, and template. All of it loads into context every session, even when only one route is active.

Anthropic has officially merged custom slash commands into skills (Claude Code Skills docs, May 2026). The `SKILL.md` format is documented as the forward-looking shape: skills can be auto-discovered by Claude when relevant, controlled via frontmatter (invocation rules, allowed tools, argument hints), and — critically — **bundled with supporting files** that load only when needed.

The existing `commands/*.md` format continues to work and is not deprecated. But the inability to bundle supporting files is now the binding constraint on two design directions:

1. **The SKILL.md prompt is too large.** Per-step guidance, per-design-doc templates, and per-review-mode logic all inline into one file.
2. **The two-tier artifacts spike** (separate human summaries from deep technical docs for design files) needs a place to put template pairs. With slash commands, these would either bloat the prompt further or live in the user's project. With skills, they live in the skill directory and are read on demand.

The user's reflection on demos (post-v2.1.0) surfaced the underlying motivation: non-engineers experience the framework's outputs as walls of text and rubber-stamp them rather than internalizing them. The two-tier work is the proposed counter — but it needs the skill format to be implementable cleanly.

## Decision

Migrate `hacky-hours` and `hacky-hours-dev` from `commands/*.md` to `skills/*/SKILL.md`. Refactor SKILL.md into an entrypoint plus bundled supporting files. Co-design the bundled file structure with the two-tier artifacts spike. Bump to **v3.0.0** due to install-path change.

### What moves where

```
~/.claude/commands/hacky-hours.md           →  ~/.claude/skills/hacky-hours/SKILL.md
.claude/commands/hacky-hours-dev.md         →  .claude/skills/hacky-hours-dev/SKILL.md
```

### SKILL.md frontmatter

```yaml
---
name: hacky-hours
description: Guide your project through the Hacky Hours framework — five-step LLM-assisted app development (ideate → design → roadmap → build → iterate). Invoke with /hacky-hours [command].
disable-model-invocation: true
argument-hint: [step | review | learn | update | tools | help]
allowed-tools: Read Bash(git status*) Bash(git log*) Bash(git diff*) Bash(gh issue list*) Bash(gh release*)
---
```

`disable-model-invocation: true` is intentional: `hacky-hours` is workflow-driven and silent auto-invocation by Claude would be surprising. Users invoke it explicitly with `/hacky-hours`.

`allowed-tools` pre-approves the narrow set of read-only operations the framework uses during sessions, reducing permission prompts.

### Bundled supporting files (target structure)

```
skills/hacky-hours/
├── SKILL.md                       # entrypoint: routing, global values, survey, voice
├── steps/
│   ├── 01-ideate.md
│   ├── 02-design.md
│   ├── 03-roadmap.md
│   ├── 04-build.md
│   └── 05-iterate.md
├── reviews/
│   ├── 01-audit.md
│   ├── 02-optimize.md
│   └── 03-pivot.md
├── learn/
│   ├── 01-tour.md
│   ├── 02-onboard.md
│   └── 03-quiz.md
├── update/
│   ├── 01-version.md
│   └── 02-project.md
├── tools/
│   ├── upgrade.md
│   ├── mode.md
│   └── walkthrough.md
└── templates/
    └── design/
        ├── ARCHITECTURE-summary.md     # two-tier: short, visual, human-facing
        ├── ARCHITECTURE-deep.md        # two-tier: deep technical expansion
        ├── DATA_MODEL-summary.md
        ├── DATA_MODEL-deep.md
        └── ...
```

The exact split between SKILL.md and supporting files is a design exercise — to be done as part of the migration work, not specified up front in this ADR.

### Backward compatibility

Per Anthropic's docs, when a skill and a command share the same name, the skill takes precedence. The slash command surface (`.claude/commands/`) remains supported by Claude Code; this migration affects only how `hacky-hours` itself is shipped. Users who don't upgrade their installation continue to work with v2.x.

Install scripts (`install.sh`, `install.ps1`) detect and remove the old `commands/hacky-hours.md` to avoid duplicate `/hacky-hours` entries in the menu.

## Consequences

**Positive:**
- SKILL.md stays small and stable; per-step content is touched independently
- Two-tier design templates have a natural home (`templates/design/`)
- `allowed-tools` reduces permission prompts during framework sessions
- Aligns with Anthropic's documented forward direction
- Establishes pattern for future bundled assets (e.g., learn-mode site scaffolds, eval fixtures)

**Negative:**
- Major version bump (v3.0.0) — users must re-run install script
- Install script complexity grows (writes a directory tree, not a single file)
- Migration is a large diff that's hard to review as one PR — likely needs to be staged

**Mitigations:**
- README.md updated to document the upgrade path explicitly
- Install scripts handle the migration mechanically (no user steps beyond re-running install)
- Migration work staged into reviewable PRs: (1) skill scaffold + minimal entrypoint, (2) per-step content moves, (3) two-tier templates, (4) install script updates, (5) docs

**Open questions deferred to migration work:**
- Final SKILL.md / supporting-file split (informed by two-tier design pass)
- Whether to use `arguments:` named args or keep manual argument parsing
- Whether sub-routes (`/hh-review`, `/hh-learn`) become standalone skills later — for now, stay routed inside one skill

## Sequencing

1. ADR accepted (this doc)
2. Two-tier artifacts design spike — produce a small prototype on one design doc to test the summary-first pattern; informs the supporting-file structure
3. Migration implementation in staged PRs (see Consequences mitigations)
4. README + runbooks updates
5. Cut v3.0.0 release

The two-tier spike and the migration are co-designed: the spike's prototype lives in the new skill directory structure, validating both the artifact pattern and the file layout simultaneously.

## References

- Research writeup: `02-design/research/2026-05-06-skill-vs-slash-command.md`
- Anthropic Skills docs: https://code.claude.com/docs/en/skills
- Agent Skills open standard: https://agentskills.io
