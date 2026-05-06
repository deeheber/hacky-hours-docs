# CHANGELOG

All notable changes to hacky-hours-docs are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] — 2026-05-06

**Breaking install path change.** The `hacky-hours` framework now ships as a Claude Code Skill (`SKILL.md` format) instead of a single slash command file. `/hacky-hours` continues to work exactly the same — only the install location changes, from `~/.claude/commands/hacky-hours.md` to `~/.claude/skills/hacky-hours/`. The installer handles the migration automatically (downloads new structure, removes old file).

> **To upgrade:** Re-run the install script from the README. The installer detects and removes the v2.x file. **Restart Claude Code** after install for the new top-level `.claude/skills/` directory to be watched.

### Added

- **SKILL.md skill format** — `hacky-hours` is now a Claude Code Skill with bundled supporting files. SKILL.md is a small entrypoint (~600 lines, down from 1500); per-step / per-review / per-tool guidance lives in `steps/`, `reviews/`, `learn/`, `update/`, `tools/` subdirectories under `${CLAUDE_SKILL_DIR}` and is loaded only when invoked. Pre-approves a narrow set of read-only Bash + Read tools via `allowed-tools` to reduce permission prompts during sessions. See [ADR: Migrate to SKILL.md format](hacky-hours/02-design/decisions/2026-05-06-migrate-to-skill-format.md).
- **Two-tier design templates** — Each design doc is now a deep dive (`<DOC>-deep.md` — the actual blueprint, source of truth, what Step 4 builds from) plus a one-screen summary (`<DOC>-summary.md` — a faithful condensation for quick gut-checks and as an onramp for non-technical readers). The deep dive is built first; the summary is generated from it and never adds new information. Prototype currently exists for ARCHITECTURE only; DATA_MODEL, USER_JOURNEYS, SECURITY_PRIVACY, etc. follow in a v3.x release once the pattern is validated in real sessions. See `${CLAUDE_SKILL_DIR}/templates/design/README.md` for the pattern.

### Changed

- **Install path:** `~/.claude/commands/hacky-hours.md` → `~/.claude/skills/hacky-hours/` (a directory)
- **Install script:** now downloads the GitHub repo tarball (instead of a single file), extracts the skill directory tree, transforms SKILL.md frontmatter from dev shape to installed shape, and removes the old v2.x slash command file if present
- **`tools upgrade` Flow A:** drafts both `<DOC>-summary.md` and `<DOC>-deep.md` for inferred design docs; reads `templates/design/README.md` first to follow the two-tier pattern
- **`tools upgrade` Flow C:** scaffold table adds row for two-tier templates (v3.0.0 introduction)
- **`review 1` audit:** design-doc scorecard handles both single-tier (legacy) and two-tier docs; flags summary-vs-deep staleness
- **`review 2` optimize, `review 3` pivot:** updated to handle two-tier docs (summary as source of intent)
- **`learn 1` tour:** starts with summaries; offers deep docs only on request
- **`tools walkthrough`:** Step 2 description mentions the two-tier shape

### Backward compatibility

- Slash command surface (`.claude/commands/`) remains supported by Claude Code; this migration affects only how `hacky-hours` itself ships
- Existing user projects with single-tier design docs continue to work without modification — `tools upgrade` Flow C will surface the two-tier templates as a v3.0.0 scaffold gap users can opt into
- Users on v2.x continue working until they re-run the installer

---

## [2.1.0] — 2026-04-18

`tools upgrade` now detects and fixes stale framework-authored boilerplate in existing `hacky-hours/` docs.

### Added

- **`tools upgrade` Flow C — Step 2b: Boilerplate migration** — scans all files under `hacky-hours/` (plus `.claudeignore` and `CLAUDE.md`) for pre-v2.0.0 patterns: "Level X" headers and old command names (`/hacky-hours audit`, `sync`, `upgrade`, `mode`, `onboard`, `link`, etc.). Reports findings grouped by file with suggested replacements. `/hacky-hours link` references are flagged for manual review rather than auto-replaced (command was removed in v2.0.0). Confirms before writing anything.

### Fixed

- **Self-documentation sweep** — applied the new boilerplate migration to this repo's own `hacky-hours/` artifacts: Level → Step headers in `PRODUCT_OVERVIEW.md`, `BACKLOG.md`, `02-design/README.md`, `ACCESSIBILITY.md`, `LICENSING.md`, `TESTING.md`; old command names in `ACCESSIBILITY.md`, `TESTING.md`, `ARCHITECTURE.md`, `SECURITY_PRIVACY.md`, and `PRODUCT_OVERVIEW.md`; removed dead Risk #4 (`link` command) from `SECURITY_PRIVACY.md` and renumbered remaining risks

---

## [2.0.2] — 2026-04-18

Fix hardcoded version strings in the `tools upgrade` skill prompt.

### Fixed

- **Version string in skill prompt** — `description`, help message, version marker written to users' `CLAUDE.md`, and completion report all hardcoded `v2.0.0`; now correctly reflects the current release

---

## [2.0.1] — 2026-04-18

Documentation sweep: all template docs, runbooks, and the README brought up to date with v2.0.0 terminology and command surface.

### Fixed

- **Level → Step language** — all template docs (`01-ideate/`, `02-design/`, `03-roadmap/`, `04-build/`), step READMEs, and runbooks now consistently use "step" instead of "level"
- **Stale v1.x command references** — `install-as-command.md` command table, `cross-tool-usage.md`, `github-action-sync.md`, `document-hygiene.md`, and `04-build/README.md` updated to v2.0.0 command surface (`step`, `review`, `learn`, `update`, `tools`)
- **"four-level" → "five-step"** in README, FAQ, `import-as-resource.md`, and `cross-tool-usage.md`
- **Removed `/hacky-hours link` reference** from `02-design/README.md` Claude Guidance — command was removed in v2.0.0
- **Removed `/hacky-hours checklist` reference** from `02-design/TESTING.md` — now points to `/hacky-hours help step 4`

### Added

- **README: Command Reference section** — full command breakdown organized by the five parent groups, added after the install section
- **README: Step 5 — Iterate in the diagram** — Mermaid diagram now shows all five steps with the loop-back arrow from Step 5 to Step 4
- **README: Five Steps table** — replaces the old Four Levels table, includes Step 5

### Changed

- **README: "paralyzed" → "stuck in endless planning"** — inclusive language follow-up to PR #2
- **README: Diagram labels** — subgraph labels updated from `L1–L4 "Level N"` to `S1–S5 "Step N"`

---

## [2.0.0] — 2026-04-11

**MAJOR VERSION — breaking changes to all command entry points.** See [ADR: v2.0.0 Command Surface Redesign](hacky-hours/02-design/decisions/2026-04-11-v2-command-surface-redesign.md) for the full rationale and migration table.

Users upgrading from v1.x: run `/hacky-hours tools upgrade` after installing to update CLAUDE.md references. All v1.x commands still exist as guidance sections — only the entry point syntax changed.

### Breaking Changes

- **Command surface fully reorganized** into five parent groups: `step`, `review`, `learn`, `update`, `tools`
- **`/hacky-hours ideate|design|roadmap|build`** → `/hacky-hours step 1|2|3|4` (named aliases still work: `step ideate`, `step build`, etc.)
- **`/hacky-hours iterate`** → `/hacky-hours step 5` (or `step iterate`) — iteration is now a first-class step
- **`/hacky-hours dry-run`** → `/hacky-hours step 0` — dry-run is step zero
- **`/hacky-hours audit`** → `/hacky-hours review 1` (or `review audit`)
- **`/hacky-hours optimize`** → `/hacky-hours review 2` (or `review optimize`)
- **`/hacky-hours pivot`** → `/hacky-hours review 3` (or `review pivot`)
- **`/hacky-hours learn [tour|onboard|quiz]`** → `/hacky-hours learn [1|2|3]` (named aliases still work)
- **`/hacky-hours sync`** → `/hacky-hours update 1` (or `update version`)
- **`/hacky-hours sync --issues`** → `/hacky-hours update 2` (or `update project`)
- **`/hacky-hours upgrade|migrate|adopt`** → `/hacky-hours tools upgrade` (detects context)
- **`/hacky-hours mode`** → `/hacky-hours tools mode`
- **`/hacky-hours mode default`** → `/hacky-hours tools mode 1` (or `tools mode builder`)
- **`/hacky-hours mode engineer`** → `/hacky-hours tools mode 2`
- **`/hacky-hours status`** → bare `/hacky-hours` (surveys and reports)
- **`/hacky-hours version`** → listed in `/hacky-hours help` header
- **`/hacky-hours checklist`** → documented in `/hacky-hours help step 4`
- **`/hacky-hours link` and `link --sync`** → **removed** (use monorepo + `--root` instead)
- **"Level" language replaced with "Step"** throughout the command prompt, CLAUDE.md, and all scaffold templates

### Added

- **Global Values section** in the command prompt — the framework's first-class values (human as driver, free before paid, privacy-first, accessible by default, licensing hygiene) declared once at the top and governing all commands
- **`/hacky-hours tools walkthrough`** — new command: narrative overview of how all commands work together, designed for framework adopters
- **`step 0`** — dry-run mode, lives naturally before step 1
- **`step 5`** — iteration promoted as a first-class step in the cycle
- **Numbered aliases** throughout: `step 1–5`, `review 1–3`, `learn 1–3`, `update 1–2`, `tools mode 1–2`
- **`tools mode builder`** — "builder" replaces "default" as the plain language mode name

### Changed

- **Command prompt reduced** from ~2,100 lines to ~1,470 lines (~30% reduction) through structural consolidation and removal of link/migrate/adopt sections
- **`tools upgrade`** absorbs `migrate` (layout migration) and `adopt` (new codebase onboarding) — detects context and runs the appropriate flow
- **`review`** with no argument runs `review 1` (audit) by default, then offers to run review 2 and 3
- **Version string** bumped to v2.0.0 in routing table, help message, and command description

### Removed

- **`/hacky-hours link`** and **`link --sync`** — multi-repo coordination removed; guidance updated to recommend monorepo + `--root`
- **`/hacky-hours migrate`** standalone — absorbed into `tools upgrade`
- **`/hacky-hours adopt`** standalone — absorbed into `tools upgrade`
- **`/hacky-hours status`** standalone — behavior incorporated into bare command
- **`/hacky-hours version`** standalone — version shown in help message header
- **`/hacky-hours checklist`** standalone — content in `help step 4`

### Design doc updates

- **`ARCHITECTURE.md`** — lifecycle diagram updated to five-step cycle, command surface section updated, Known Fragility updated
- **`CLAUDE.md`** — "Level" → "Step" throughout, command references updated (`review 1`/`update 1` instead of `audit`/`sync`)
- **ADR: v2.0.0 Command Surface Redesign** — documents all thirteen decisions with rationale, tradeoffs, and breaking changes migration table

---

## [1.8.0] — 2026-04-11

Learn suite, upgrade command, testing design doc, and expanded audit scorecard.

### Added

- **`/hacky-hours learn [tour|onboard|quiz]`** — new learning suite for knowledge transfer and onboarding. Three modes: guided tour of the project (scoped to focus area), hands-on task scoping for engineers new to an area, and knowledge quiz (broad or scoped). All modes work as Claude Code conversations; tour and quiz optionally generate a shareable Astro static site. Conversation-first design means the feature always works even without Node.js.
- **`/hacky-hours upgrade`** — brings existing project artifacts up to date with the current command version. Detects missing scaffold folders, new doc templates, and `.claudeignore` entries introduced since the project was last scaffolded. Absorbs the v0.x → v1.0 folder migration previously handled by `migrate`. Read-only until the user confirms. Writes a `<!-- hacky-hours: vX.Y.Z -->` version marker to `CLAUDE.md` after running.
- **`02-design/TESTING.md` template** — new Level 2 design doc for test strategy, test types, definition of done, and test environments. Scaffolded by default alongside ACCESSIBILITY.md and LICENSING.md.
- **`hacky-hours/learn/` and `hacky-hours/feedback/`** — new scaffold folders. `learn/` holds generated tour/quiz Astro sites (tour/, quiz/, personal/<username>/). `feedback/` holds user-submitted feedback files (`feedback-<username>-<timestamp>.md`) from learn sessions.
- **Feedback loop** — `iterate` Step 1 Capture now checks `hacky-hours/feedback/` for feedback files from learn sessions before asking the user to brain-dump. Surfaces them as additional input.
- **Expanded audit scorecard (Phase 2)** — now checks all design doc types (ARCHITECTURE, DATA_MODEL, USER_JOURNEYS, STYLE_GUIDE, ACCESSIBILITY, MARKET_FIT, BUSINESS_LOGIC, SECURITY_PRIVACY, LICENSING, TESTING, RELATED_REPOS) with a consistent per-domain format: exists? filled in? specific gap if not. Reports as a table with ✓/✗/⚠ indicators.
- **ADR: Learn Suite Architecture** (`02-design/decisions/2026-04-11-learn-suite-architecture.md`) — documents the conversation-first/site-optional design, Astro stack selection, and sub-subcommand grouping decision.

### Changed

- **Scaffold structure** — `learn/` and `feedback/` folders added. `02-design/TESTING.md` added. `hacky-hours/learn/` added to `.claudeignore` defaults.
- **`help design`** — TESTING added to available docs list.
- **`hacky-hours/02-design/README.md`** — TESTING.md added to the design doc index.
- **Version bumped** to v1.8.0 in routing table, help message, and command description.

### Design doc updates

- **`ARCHITECTURE.md`** — Learn Suite section, Static Site Generation section (Astro), Upgrade Command section, Known Fragility updated
- **`SECURITY_PRIVACY.md`** — `onboard` automated git push, user-generated content in feedback files, Astro/Node.js supply chain surface
- **`ACCESSIBILITY.md`** — scope updated to include generated web UI; v1.8.0 command notes; WCAG 2.1 AA evaluation flagged as outstanding
- **`TESTING.md`** — created for hacky-hours-docs: testing layers, pre-release checklist, eval coverage, v1.8.0 testing notes

---

## [1.7.0] — 2026-04-04

Voice mode — non-technical plain language is now the default conversation style, with an opt-in engineer mode for technical users.

### Added

- **`/hacky-hours mode`** — new command to toggle conversation voice between `default` (plain language) and `engineer` (technical). Persists to `CLAUDE.md` across sessions. Toggles without an argument; accepts `mode engineer` or `mode default` explicitly.
- **`help mode`** — subcommand help entry documenting mode usage, both voices, and persistence behavior
- **Voice mode in scaffold** — new projects get a `## Hacky Hours Voice` section in their generated `CLAUDE.md`, defaulting to plain language, with a one-line note on how to switch

### Changed

- **Default conversation style is now non-technical** — tradeoffs explained through outcomes, analogies, and consequences; no jargon without plain-language definition. Engineers opt in to technical mode rather than non-technical users having to ask for simpler explanations.
- **`ARCHITECTURE.md`** — Voice Mode section added documenting mode as a persistent config concept
- **`ACCESSIBILITY.md`** — non-technical default documented as an explicit accessibility decision with rationale
- **Version bumped** to v1.7.0 in routing table, help message, and command description

---

## [1.6.0] — 2026-03-30

Readability and accessibility pass — making every document approachable for non-technical users.

### Added

- **"What is this?" intros** on all Level 2 design doc templates — plain-language explanations of what each document type is and why it exists, so non-technical users aren't put off by terms like "architecture" or "data model"
- **Beginner bridges** on advanced docs — `import-as-resource.md`, `github-action-sync.md`, and `install-as-command.md` now explain prerequisites and audience before diving into instructions
- **Pre-push git hook** — blocks tag pushes if CHANGELOG.md doesn't have a matching version entry, preventing the version drift that happened with v1.5.1/v1.5.2

### Changed

- **`runbooks/document-hygiene.md`** — full rewrite replacing engineer jargon (Hot/Warm/Cold tiers, ADRs, append-only ledger) with plain-language equivalents; added note that `/hacky-hours` handles most of this automatically
- **`runbooks/getting-started/03-git-basics.md`** — expanded "Working with Branches" section with plain-language explanations of what branches are, why you'd use them, and what flags like `-b` and `-u origin` do
- **`runbooks/getting-started/07-linux-setup.md`** — added context for `curl | sudo bash` pattern and step-by-step explanation of the npm permissions workaround
- **`runbooks/getting-started/02-claude-code.md`** — explained why Claude Pro is required (vs free account) and what `npm install -g` does
- **`runbooks/cross-tool-usage.md`** — added one-line descriptions of Cursor, Windsurf, MCP, and Claude.ai Projects for readers unfamiliar with them
- **`README.md`** — added context line before Mermaid diagram; marked advanced sections (slash command install, import-as-resource) with callouts directing beginners elsewhere
- **`runbooks/getting-started/05-windows-setup.md`** — linked PATH error to glossary with inline explanation
- **`02-design/ACCESSIBILITY.md`** — reformatted header to match other Level 2 templates (added attribution line, replaced inline intro with "What is this?" callout)
- **`02-design/LICENSING.md`** — removed redundant intro paragraph (replaced by "What is this?" callout)

### Fixed

- **`runbooks/costs.md`** — replaced Google Domains reference (shut down) with Squarespace Domains
- **`CHANGELOG.md`** — added missing entries for v1.5.1 and v1.5.2

---

## [1.5.2] — 2026-03-30

Cross-reference fixes and `.claudeignore` from optimize run.

### Fixed

- **CLAUDE.md** — fixed broken path to SECURITY_PRIVACY.md, removed reference to nonexistent `04-build/README.md`
- **ARCHITECTURE.md** — updated prompt size metric, fixed stale optimize description in lifecycle diagram
- **Non-linear lifecycle ADR** — noted optimize redesign from v1.5.1
- **`.claudeignore`** — created (was missing — archived docs were loading into context unnecessarily)
- Removed empty `03-roadmap/` directory

---

## [1.5.1] — 2026-03-30

Optimize command redesign and milestone housekeeping.

### Changed

- **`/hacky-hours optimize`** — redesigned from metrics-only dashboard to substantive review comparing design intent vs. current reality. For code projects, reads planning docs AND the codebase. For docs-only projects, analyzes the command prompt against design docs.

### Fixed

- **SECURITY_PRIVACY.md** — added GitHub API surface (`sync --issues`), cross-repo writes (`link`), and audit secret scanning limitations
- **ACCESSIBILITY.md** — added v1.5.0 new command evaluation notes
- **PRODUCT_OVERVIEW.md** — fixed stale version reference (v1.0.1 → v1.5.0), updated non-goals
- **CLAUDE.md** — added Project State Machine section (eating our own dogfood)

### Housekeeping

- Archived CHANGELOG entries v0.1.0–v0.8.0 to `archive/changelog/`
- Archived completed `ITERATION.md` (v1.5.0) and unused `ROADMAP.md` stub

---

## [1.5.0] — 2026-03-30

Non-linear lifecycle: product pivot, doc efficiency optimization, and two-way GitHub Issues sync.

### Added

- **`/hacky-hours optimize`** — new command that evaluates framework documentation efficiency. Scans all docs for token cost (estimated), staleness (last modified vs. last commit reference), density (placeholder vs. real content), and cross-reference usage. Generates actionable recommendations: archive, consolidate, trim, or fill in. Optionally saves results as an optimization report in `audits/`. Also integrated as a lighter check in iterate Step 2 — flags oversized/stale docs during synthesis.
- **`/hacky-hours pivot`** — new lifecycle path for product re-ideation with full context. Reads all existing artifacts, walks through Level 1 questions with awareness of current state, produces a structured diff of what changed, and cascades changes through Levels 2-4. Includes doc structural refactoring (merge, split, retire) and ADR generation for significant direction changes. Use when the product direction itself needs rethinking, not just refinement.
- **`/hacky-hours sync --issues`** — two-way reconciliation between BACKLOG.md and GitHub Issues. Push: creates Issues from BACKLOG items without `#<number>` annotations. Pull: surfaces open Issues with `[hacky-hours]` label not in BACKLOG. Diverged items shown side-by-side for human resolution. Last-write-wins conflict model — every change requires explicit confirmation. Creates `[hacky-hours]` label automatically if missing.
- **ADR: Non-Linear Lifecycle** (`02-design/decisions/2026-03-30-non-linear-lifecycle.md`) — documents the shift from a strictly linear four-level lifecycle to one with backward arcs via `pivot` and self-evaluation via `optimize`.
- **ADR: Two-Way GitHub Issues Sync** (`02-design/decisions/2026-03-30-issues-two-way-sync.md`) — documents the last-write-wins conflict resolution model, identity linking (`#<number>` in BACKLOG, `[hacky-hours]` label on Issues), and the decision to keep neither source canonical.

### Changed

- **Lifecycle model** — the framework is no longer strictly linear. ARCHITECTURE.md now includes a Mermaid diagram showing the iterate → pivot backward arc and the optimize self-evaluation loop.
- **ARCHITECTURE.md** — added Lifecycle Model section, GitHub Issues Integration section, updated command prompt size metric.
- **Iterate guidance (Step 2)** — now includes a lightweight efficiency check that flags oversized/stale docs during synthesis, with a suggestion to run `/hacky-hours optimize` for full analysis.
- **Sync command** — now has two modes: `sync` (releases, unchanged) and `sync --issues` (issue reconciliation). Routing and help updated accordingly.
- **Help message** — added `optimize`, `pivot`, and `sync --issues` entries.
- **Subcommand help** — added `help optimize`, `help pivot`, and `help sync --issues` entries.

---

## [1.4.0] — 2026-03-21

Cross-repo linking: connect related repos, generate RELATED_REPOS.md in both, and re-sync when the authoritative repo changes.

### Added

- **`/hacky-hours link`** — new command for connecting two related repos. Run in the dependent repo, pointing at the authoritative repo's local path. Reads both repos' design docs, infers the relationship and source-of-truth boundary, asks clarifying questions, and generates `RELATED_REPOS.md` in both repos plus a `## Related Repositories` section in this repo's `CLAUDE.md`. `--sync` flag re-reads the authoritative repo's current design docs and surfaces what's changed since the link was established — without auto-updating anything.
- **`RELATED_REPOS.md` template** (`02-design/RELATED_REPOS.md`) — new Level 2 design artifact for documenting cross-repo relationships. Contains: relationship table (role + source-of-truth boundary per repo), Decision Routing Table (design question → doc in other repo), and cross-repo coordination protocol. Single file with one `## Repo:` section per related repo.

### Changed

- **Level 2 guidance** — added `RELATED_REPOS.md` to the "which docs does your project need?" table, prompted when `ARCHITECTURE.md` indicates a multi-repo split. Also added `link` suggestion to the Claude Guidance section of `02-design/README.md`.
- **Help message** — added `--- Multi-repo ---` section with `link` entry.
- **Subcommand help** — added `help link` entry documenting both initial link and `--sync` usage.

---

## [1.3.0] — 2026-03-21

Accessibility audit, glossary expansion, version bump check, and CLA resolution.

### Added

- **Pre-release version bump check** — the audit flow (Phase 2) now checks whether version strings in the command prompt match the latest CHANGELOG version before tagging. Flags mismatches as warnings.
- **19 new glossary entries** — ARIA, CCPA, copyleft, frontmatter, GDPR, GPL, HIPAA, MCP, NVDA, OAuth, OWASP Top 10, screen reader, submodule, symlink, tag, VoiceOver, WCAG, YAML, and backend. All terms were found used in runbooks or templates without definition.

### Changed

- **ACCESSIBILITY.md** — updated with audit findings: 21 terms addressed, remaining gaps documented (screen reader navigation, i18n, shell-specific instructions).
- **LICENSING.md** — CLA checklist item resolved: not needed for a Markdown-only MIT project. Revisit only if commercial product or relicensing is considered.

---

## [1.2.0] — 2026-03-21

Cross-tool support, CHANGELOG deduplication, and architecture documentation.

### Added

- **Cross-tool usage runbook** (`runbooks/cross-tool-usage.md`) — documents how to use the framework in Cursor, Windsurf, Claude.ai Projects, or any LLM tool that reads project context. The slash command is a Claude Code convenience; the framework works anywhere via CLAUDE.md project instructions.
- **Release Process section in ARCHITECTURE.md** — documents the dev → installed publish cycle, version bump strategy (patch/minor/major), and the three places version strings need updating.
- **Cross-Tool Support section in ARCHITECTURE.md** — explains how the framework works without the slash command: artifacts + CLAUDE.md project state machine.

### Changed

- **CHANGELOG deduplication** — `hacky-hours/04-build/CHANGELOG.md` is now a symlink to the root `CHANGELOG.md`, eliminating duplicate changelogs. The adopt flow now detects existing CHANGELOGs and creates symlinks instead of new files.
- **ARCHITECTURE.md Known Fragility** — updated to reflect v1.1.0 harmonization work; remaining fragility items are now: no gradual rollout, single-file architecture, cross-tool portability.
- **Adopt flow** — now detects existing `CHANGELOG.md` files and creates a symlink to them instead of creating a duplicate. Includes explicit guidance on computing relative symlink paths.

---

## [1.1.0] — 2026-03-21

Subcommand help, persistent audit scorecards, and command prompt harmonization.

### Added

- **`/hacky-hours help <command>`** — detailed per-command help for all 10 commands (ideate, design, roadmap, build, iterate, audit, sync, adopt, migrate, dry-run). Shows what the command does, when it's done, and what to run next.
- **Audit scorecards (Phase 5)** — after running `/hacky-hours audit`, optionally save results as a persistent Markdown scorecard in `audits/`. Scorecards capture secrets scan, doc readiness, git status, and next steps in a standardized, dated format (`YYYY-MM-DD-audit.md`).
- **`audits/` directory** — added to scaffold structure and `.claudeignore` defaults. Stores persistent audit scorecards.
- **Context preambles** — Iterate, Sync, Audit, Adopt, and Migrate workflows now have "Context to read before starting" sections, matching the pattern already used by Levels 1–4.
- **`hacky-hours/` framework artifacts** — dogfooding: the framework's own PRODUCT_OVERVIEW, ARCHITECTURE, SECURITY_PRIVACY, LICENSING, ACCESSIBILITY, ROADMAP, BACKLOG, and CHANGELOG now live under `hacky-hours/`.

### Changed

- **Scaffold structure** — now creates `audits/` directory alongside `archive/`.
- **Generated `CLAUDE.md`** — scaffold now notes that paths should be substituted when ROOT_PATH differs from `hacky-hours/`.
- **Adopt file list** — now matches what Scaffold creates: includes `02-design/README.md`, `02-design/decisions/`, `03-roadmap/ROADMAP.md`, and `audits/`.
- **Help message** — updated to show `help <cmd>` option and audit scorecard description.

---

## [1.0.1] — 2026-03-20

### Fixed

- **`/hacky-hours iterate`** — `ITERATION.md` was being created at the project root instead of under ROOT_PATH (`hacky-hours/` by default). Archive path was also pointing to `archive/` instead of `ROOT_PATH/archive/`. Both paths now correctly follow ROOT_PATH, consistent with all other framework artifacts.

---

## [1.0.0] — 2026-03-20

Safety-first design philosophy, licensing as a first-class artifact, and `hacky-hours/` subfolder as the default scaffold location.

### Added

- **`02-design/LICENSING.md`** — new design document template covering product license choice (MIT, Apache, GPL, proprietary, etc.), third-party dependency license compatibility, business model implications, and a pre-build checklist. Scaffolded by default alongside `ACCESSIBILITY.md`.
- **`/hacky-hours audit`** — new read-only release readiness command: (1) secrets and sensitive file scan with heuristic pattern matching, (2) framework doc readiness checks, (3) git status translated into plain language, (4) numbered next-steps to-do list ordered by severity. Never modifies any files. The recommended step before `/hacky-hours sync`.
- **`/hacky-hours adopt`** — new command for bringing an existing codebase into the framework. Reads README, package manifests, directory structure, schema files, auth files, env var references, git log, and TODO comments to infer artifact stubs for PRODUCT_OVERVIEW, ARCHITECTURE, SECURITY_PRIVACY, and BACKLOG. Asks clarifying questions for what can't be inferred. Always confirms before writing. Hands off to `iterate` as the natural next step.
- **`/hacky-hours migrate`** — new command that moves existing root-level framework artifacts into the `hacky-hours/` subfolder using `git mv` (preserving history). Updates `.claudeignore`, `CLAUDE.md`, and flags any `hacky-hours-sync.yml` GitHub Action path changes needed. Shows exactly what it will do before doing anything. Commits framework files only — not `git add -A`.
- **Constraints & Values section in `PRODUCT_OVERVIEW.md`** — captures licensing intent, privacy stance, infrastructure preference, and accessibility commitment at Level 1, seeding Level 2 design decisions before any code is written.
- **Safety-first design philosophy** — documented in `CLAUDE.md` and embedded throughout Level 2 guidance: free before paid, less infrastructure before more, privacy-preserving before data-rich, accessible by default, fewer dependencies before more. Claude leads with the simplest safe option and explains tradeoffs before suggesting complexity.
- **Licensing questions at Level 1** — the Level 1 → Level 2 transition now explicitly includes licensing intent questions so that dependency choices in Level 2 are made with license compatibility in mind.
- **Context-reading preambles on every level command** — each level command (`ideate`, `design`, `roadmap`, `build`) now explicitly states which prior artifacts to read before starting. Claude won't ask users to repeat what's already written.

### Changed

- **Default scaffold location** — framework artifacts now default to `hacky-hours/` subfolder instead of the project root. Pass `--root .` to operate at the root as before. The survey step falls back to the root automatically for existing projects and suggests running `migrate`.
- **No-arg behavior** — `/hacky-hours` (no argument) now runs the full guided session (survey + orient + act) instead of printing the help message. Use `help` for the help message. This makes the no-arg path the natural "just run this and it'll figure out where you are" on-ramp for new users.
- **Help message** reorganized into logical groups: Getting started, Navigate the framework, Release workflow, Utilities. Clearer description of each command's purpose.
- **`/hacky-hours sync`** — redesigned. Now does one thing: publish a GitHub Release from the latest CHANGELOG entry. BACKLOG→Issues and milestone creation removed — these created maintenance burden without meaningful value for the core audience. Sync now: checks `gh` auth, confirms the tag, previews exactly what will be published, and publishes on explicit confirmation.
- **Milestone-complete flow** — when BACKLOG.md empties, now suggests `audit` before `sync` so users catch issues before publishing.
- **Generated project `CLAUDE.md`** — paths updated to `hacky-hours/` prefix; now also suggests `audit` before `sync` on milestone completion.
- **`.claudeignore` defaults** updated to use `hacky-hours/` prefixes.
- **`ARCHITECTURE.md` Claude Guidance** — strengthened with explicit safety-first defaults: managed/hosted before self-hosted, fewer external services, established open-source libraries, cost and data residency implications flagged.
- **`SECURITY_PRIVACY.md`** — added Dependency Security and License Hygiene section; Claude Guidance updated to recommend OAuth/magic links over custom auth, and to cross-reference `LICENSING.md`.
- **`ACCESSIBILITY.md` Claude Guidance** — added "start simple, stay semantic" principle and note on accessible-first UI library selection.
- **`02-design/README.md`** — added `LICENSING.md` row; Claude Guidance updated to read Constraints & Values section first and apply safety-first defaults throughout.
- **Version** bumped to v1.0.0.

---

## [0.9.0] — 2026-03-20

Dogfooding support, sync upgrades, project state machine, and GitHub Action template.

### Added

- **`--root <path>` flag** — all commands now accept `--root <path>` to scaffold and operate in a subdirectory instead of the project root (e.g. `/hacky-hours ideate --root meta/` for dogfooding the framework within its own repo)
- **Generated project `CLAUDE.md`** — scaffolded alongside the level folders; contains state machine instructions so Claude automatically checks GitHub Issues at session start, removes completed items from BACKLOG.md, adds them to CHANGELOG.md, closes linked issues, and prompts the release process when the milestone is done
- **GitHub Action template** — `runbooks/templates/hacky-hours-sync.yml`: a copy-paste workflow that calls the Claude API on PR merge to remove the completed item from BACKLOG.md and add it to CHANGELOG.md automatically
- **`runbooks/github-action-sync.md`** — setup guide for the Action template, including cost, matching logic, and troubleshooting

### Changed

- **`sync` guidance** — upgraded with deduplication (checks for existing issues before creating), issue URL back-linking (records GitHub URL into BACKLOG.md after creation), pre-flight `gh auth status` check, and a post-sync summary

---

*Older entries (v0.1.0–v0.8.0) archived to `hacky-hours/archive/changelog/`.*
