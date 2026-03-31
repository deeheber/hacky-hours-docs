# CHANGELOG

All notable changes to hacky-hours-docs are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
