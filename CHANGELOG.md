# CHANGELOG

All notable changes to hacky-hours-docs are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
