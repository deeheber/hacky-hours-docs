# CHANGELOG

All notable changes to hacky-hours-docs framework artifacts are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] — 2026-03-21

### Added

- **Subcommand help** — `/hacky-hours help <command>` now shows detailed help for any specific command (e.g., `help audit`, `help iterate`). Lists what the command does, when it's done, and what to run next.
- **Audit scorecards (Phase 5)** — after running `/hacky-hours audit`, you can optionally save results as a persistent Markdown scorecard in `audits/`. Scorecards capture secrets scan, doc readiness, git status, and next steps in a standardized format. Named by date (`YYYY-MM-DD-audit.md`).
- **`audits/` directory** — added to scaffold structure and `.claudeignore` defaults. Stores persistent audit scorecards.
- **Context preambles** — Iterate, Sync, Audit, Adopt, and Migrate workflows now have "Context to read before starting" sections, matching the pattern already used by Levels 1–4. Claude reads relevant docs before asking questions.

### Changed

- **Scaffold** — now creates `audits/` directory alongside `archive/`. `.claudeignore` defaults updated to exclude `hacky-hours/audits/`.
- **Generated `CLAUDE.md`** — scaffold now notes that paths should be substituted when ROOT_PATH differs from `hacky-hours/`.
- **Adopt file list** — now matches what Scaffold creates: includes `02-design/README.md`, `02-design/decisions/`, `03-roadmap/ROADMAP.md`, and `audits/`.
- **Help message** — updated to show `help <cmd>` option and audit scorecard description.
