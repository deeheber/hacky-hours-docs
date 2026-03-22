# CHANGELOG

All notable changes to hacky-hours-docs are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

## [0.8.0] — 2026-03-20

Tone pass aligned with Empathetech values, and ACCESSIBILITY.md as a first-class design artifact.

### Added

- **`02-design/ACCESSIBILITY.md`** — new design document template covering WCAG standards, perceivable/operable/understandable/robust criteria, testing plan, and known exceptions. Scaffolded by default and listed as a first-class citizen in the Level 2 design table.

### Changed

- **Tone** — language across CLAUDE.md, README.md, and the command file updated to reflect Empathetech's warm, peer-equal, anti-gatekeeping voice:
  - "C-suite / implementation team" framing replaced with "driver / collaborator"
  - README opener now welcomes anyone — "no experience required"
  - "Done when" criteria softened to be honest rather than clinical
  - Fresh project greeting updated to feel inviting, not procedural
  - "Framework not a rulebook" framing added to the command intro
  - Emoji added where they add warmth without distraction 🛠️🤗🎉✅

---

## [0.7.0] — 2026-03-20

Document lifecycle, iteration cycle, and GitHub sync support.

### Added

- **`/hacky-hours iterate`** — runs an iteration cycle: free-write bugs/ideas into `ITERATION.md`, identify which design docs need amending, triage items into BACKLOG, write ADRs for significant decisions, then proceed with Level 4 build
- **`/hacky-hours sync`** — pushes BACKLOG items to GitHub Issues, creates milestones, and publishes CHANGELOG entries as GitHub Releases via `gh` CLI (always confirms before acting)
- **`archive/` folder** — added to scaffold as cold storage for completed milestones, old CHANGELOG entries, superseded design decisions, and IDEATION.md after Level 1
- **`.claudeignore`** — added to scaffold with sensible defaults to keep LLM context lean as the project grows
- **`02-design/decisions/`** — added to scaffold for Architecture Decision Records
- **`runbooks/document-hygiene.md`** — new runbook covering hot/warm/cold doc tiers, per-document lifecycle, ADR pattern, archive conventions, and a milestone housekeeping checklist

### Changed

- **Scaffold** — expanded to include `archive/`, `.claudeignore`, and `02-design/decisions/`
- **BACKLOG.md** — formalized as a strict queue: items are removed when merged, not marked done. An empty BACKLOG signals milestone complete.
- **Level 2 guidance** — added ADR pattern: when a design decision changes during iteration, write a new ADR rather than rewriting the original document in place
- **Level 4 guidance** — added milestone housekeeping checklist: CHANGELOG trimming, roadmap archival, design doc amendments, `.claudeignore` review

---

## [0.6.0] — 2026-03-20

Command UX improvements: proper autocomplete description, safer default behavior, and a dry-run mode for testing without writing files.

### Added

- **`/hacky-hours dry-run`** — runs the full interactive workflow without creating or modifying any files; file contents are shown in code blocks with a `↳ would write to <path>` note instead
- **YAML frontmatter `description` field** — replaces the `<!-- version: x.x.x -->` comment; autocomplete now shows a human-readable description instead of the version string

### Changed

- **No-argument behavior** — running `/hacky-hours` with no argument now prints the help message instead of immediately starting the workflow, preventing accidental framework invocation
- **Help message** — added a one-paragraph description of what Hacky Hours is, so the help output is useful to someone who hasn't seen the framework before
- **"Fresh project" greeting** — expanded to introduce the framework to users encountering it for the first time in a new project

### Fixed

- **README.md** — corrected "Hacky Hour" to "Hacky Hours"

---

## [0.5.0] — 2026-03-20

Quality-of-life improvements to the slash command: new utility arguments, version tracking, and a dev/release naming distinction.

### Added

- **`/hacky-hours help`** — prints all available arguments and a link to the repo
- **`/hacky-hours version`** — prints the installed command version
- **`/hacky-hours status`** — surveys the project and reports the current framework level in one sentence, with no interactive menu
- **`/hacky-hours checklist`** — prints the pre-merge checklist directly, without navigating through the full build flow
- **Version string** (`<!-- version: 0.5.0 -->`) embedded in the command file so the version is always readable

### Changed

- **`.claude/commands/hacky-hours.md` → `.claude/commands/hacky-hours-dev.md`** — renamed so the project-level command shows as `/hacky-hours-dev` in this repo, distinguishing it from the globally installed `/hacky-hours` release. The install scripts still fetch this file and save it as `hacky-hours.md` globally — the rename is invisible to end users.
- **`install.sh` / `install.ps1`** — updated source URL to match the renamed file.

---

## [0.4.0] — 2026-03-20

Adds a self-contained Claude Code slash command that can be installed globally and used in any repository.

### Added

- **`.claude/commands/hacky-hours.md`** — A Claude Code custom slash command (`/hacky-hours`) that works as a project-level command in this repo and as a global command once copied to `~/.claude/commands/`. The command surveys the current project directory, detects which framework level is active (or that no framework files exist), and guides the user through the appropriate next step. Supports `$ARGUMENTS` for jumping directly to a level (`/hacky-hours ideate`, `/hacky-hours design`, `/hacky-hours roadmap`, `/hacky-hours build`). Embeds the full framework guidance so it functions without the hacky-hours-docs repo being present in the target project.
- **`runbooks/install-as-command.md`** — Instructions for installing the command globally on macOS, Linux, and Windows. Covers verification, updating to new versions, and uninstalling.

### Changed

- **`README.md`** — Added "Use as a Claude Code Command" section with one-liner install instructions and a link to the install runbook.

---

## [0.3.0] — 2026-03-20

Major content additions: a worked example project, copy-paste Claude session starters, a glossary, FAQ, cost breakdown, and a zero-install setup path via GitHub Codespaces.

### Added

- **`example/`** — A fully worked fictional project (NeighborBoard) showing completed Level 1 and Level 2 documents: `IDEATION.md`, `PRODUCT_OVERVIEW.md`, `ARCHITECTURE.md`, `DATA_MODEL.md` (with Mermaid ERD), `USER_JOURNEYS.md` (with flowcharts), and `SECURITY_PRIVACY.md`. Gives non-technical users a concrete model of what the framework outputs look like.
- **`runbooks/starter-prompts/`** — Copy-paste conversation starters for every level: ideation, product overview, design documents, roadmap, and build tasks. Removes the blank-cursor freeze at the start of each Claude session.
- **`GLOSSARY.md`** — Plain-language definitions for every technical term used in the framework (git, fork, branch, API, terminal, npm, etc.).
- **`runbooks/costs.md`** — Full cost breakdown: tools to get started (~$20/month), hosting options, domain names, and when free tiers stop being sufficient.
- **`runbooks/FAQ.md`** — Answers to the most common questions from non-technical users: do I need to code, what if I make a mistake, why does Claude forget things, when am I ready to build.
- **`runbooks/getting-started/08-github-codespaces.md`** — Zero-install setup path: fork the repo, open a Codespace, install Claude Code in the browser terminal, start building. No local installs required.
- **`runbooks/getting-started/09-github-desktop.md`** — Visual git management using GitHub Desktop. Covers clone, commit, push, and branch workflows with buttons instead of terminal commands.
- **Mermaid framework diagram** in `README.md` — A flowchart showing the full four-level journey from idea to shipped product.
- **Resources table** in `README.md` — Quick reference to example project, starter prompts, glossary, FAQ, and costs.
- **GitHub web editor guidance** in `fork-vs-clone.md` — How to edit Markdown files directly on GitHub without opening a terminal or VS Code.

### Changed

- **`runbooks/getting-started/README.md`** — Restructured into three setup paths: zero-install (Codespaces), local with GitHub Desktop, and full terminal. Each path has an OS-specific ordered checklist.

---

## [0.2.0] — 2026-03-20

Accessibility pass: added beginner-friendly onboarding content, completion checkpoints, and simplified the most intimidating parts of the setup process.

### Added

- **`runbooks/getting-started/README.md`** — Master entry point for the getting-started folder with OS-specific ordered checklists (macOS, Windows, Linux) and a time estimate for each step.
- **`runbooks/getting-started/00-what-is-a-terminal.md`** — Beginner explainer: what a terminal is, how to open it on each OS, how to read and run command blocks, and what to do when something goes wrong.
- **"You're done when..." completion checkpoints** — Added to every setup runbook so users know exactly when a step is complete before moving on.
- **Screenshot placeholders** — Marked key steps in each runbook with `> **Screenshot:**` callouts indicating where visual guides should be added.

### Changed

- **Path placeholders replaced with concrete examples** — `cd path/to/your-project` replaced with `cd ~/Documents/my-project-docs` plus an explicit note to substitute the real path.
- **`fork-vs-clone.md`** — Simplified for beginners: clear 3-step beginner path, advanced `git remote` steps moved into a collapsible `<details>` block.
- **`02-claude-code.md`** — Added Claude Pro pricing context and a link to `claude.ai/pricing`. Added a tip for finding your folder path in VS Code.
- **`01-github.md`** — Explained what an authenticator app is with links to recommended options. Sends users back to the master checklist after completing the step.
- **OS setup runbooks** (`05`, `06`, `07`) — Added terminal explainer link at the top, expanded Homebrew install instructions with password entry note (macOS), added completion checkpoints.

### Fixed

- **`README.md`** — Corrected Empathetech URL from `.net` to `.org`.

---

## [0.1.0] — 2026-03-20

Initial framework release. Establishes the four-level documentation system, all template documents, and setup runbooks for Windows, macOS, and Linux.

### Added

- **Four-level folder structure** — `01-ideate/`, `02-design/`, `03-roadmap/`, `04-build/` with numbered prefixes for clear progression.
- **Level 1 — Ideation** — `IDEATION.md` (stream-of-consciousness template) and `PRODUCT_OVERVIEW.md` (5Ws synthesis template), each with Claude guidance blocks and related links.
- **Level 2 — Design** — Seven templates: `ARCHITECTURE.md`, `DATA_MODEL.md`, `USER_JOURNEYS.md`, `STYLE_GUIDE.md`, `MARKET_FIT.md`, `BUSINESS_LOGIC.md`, `SECURITY_PRIVACY.md`. Mermaid diagram guidance in `diagrams/README.md`.
- **Level 3 — Roadmap** — `ROADMAP.md` template with MVP / V1 / V2 tiers and milestone format.
- **Level 4 — Build** — `BACKLOG.md` with task-to-branch-to-version tracking, `CHANGELOG.md` template following Keep a Changelog format.
- **`CLAUDE.md`** — In-session guidance for Claude covering the four-level system, C-suite/implementation-team framing, escalating sophistication model, and import-as-resource instructions.
- **Setup runbooks** — `01-github.md`, `02-claude-code.md`, `03-git-basics.md`, `04-ide-setup.md`, platform-specific setup for Windows (`05`), macOS (`06`), and Linux (`07`).
- **Using-this-repo runbooks** — `fork-vs-clone.md`, `import-as-resource.md` (git submodule, CLAUDE.md snippet, manual copy), `contributing.md`.
- **`README.md`** — Framework overview with four-level table, getting started instructions, and import-as-resource summary.

---

[0.5.0]: https://github.com/empathetech/hacky-hours-docs/releases/tag/v0.5.0
[0.4.0]: https://github.com/empathetech/hacky-hours-docs/releases/tag/v0.4.0
[0.3.0]: https://github.com/empathetech/hacky-hours-docs/releases/tag/v0.3.0
[0.2.0]: https://github.com/empathetech/hacky-hours-docs/releases/tag/v0.2.0
[0.1.0]: https://github.com/empathetech/hacky-hours-docs/releases/tag/v0.1.0
