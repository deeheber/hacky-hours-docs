# ITERATION.md

**Post-release iteration** | hacky-hours-docs v1.5.2

---

## Raw Capture

### Readability audit (2026-03-30)

Scored every README, runbook, glossary, and starter prompt on a 1-10 readability scale (1 = easiest for all audiences, 10 = hardest). Framework claims to be "for everyone" but several docs are engineer-only.

#### Easy (1-2) — no changes needed
- `00-what-is-a-terminal.md` (1)
- `getting-started/README.md` (2)
- `01-github.md` (2)
- `04-ide-setup.md` (2)
- `08-github-codespaces.md` (2)
- `09-github-desktop.md` (2)
- `costs.md` (2)
- `FAQ.md` (2)
- All 5 starter prompts (2)
- `GLOSSARY.md` (2)

#### Accessible (3-4) — minor improvements
- `README.md` (3) — `curl | bash` install and "Import as Resource" sections presented at same weight as beginner path; Mermaid diagram assumes visual literacy
- `02-claude-code.md` (3) — doesn't explain why Pro is needed vs Free; `npm install -g` flag unexplained
- `05-windows-setup.md` (3) — "PATH" reference will confuse beginners (glossary covers it but no link)
- `06-macos-setup.md` (3) — minor; mostly good
- `fork-vs-clone.md` (3) — solid, advanced content hidden behind details toggle
- `contributing.md` (3) — clear
- `03-git-basics.md` (4) — branches section moves too fast; `checkout -b` and `push -u origin` thrown at beginners without enough "why"
- `install-as-command.md` (4) — no explanation of what the command does before install instructions; assumes you know what a "slash command" is
- `cross-tool-usage.md` (4) — assumes familiarity with Cursor, Windsurf, MCP, .cursorrules

#### Engineer-only (5-7) — need significant work
- `07-linux-setup.md` (5) — `curl | sudo bash` pipeline is scary; npm permissions workaround is technical. Acceptable since Linux users skew technical.
- `document-hygiene.md` (6) — "Hot/Warm/Cold tiers," "ADRs," "append-only ledger," `.claudeignore` as convention. Non-technical users would bounce entirely.
- `import-as-resource.md` (6) — git submodules, `--recurse-submodules`, CLAUDE.md snippets. Engineer-only with no beginner bridge.
- `github-action-sync.md` (7) — GitHub Actions, API keys as secrets, YAML config, Claude API calls. No lead-in saying "this is advanced, you don't need it to get started."

### Artifact template education gap

Level 2 design doc templates assume people know what "Architecture Decision Records," "Data Models," "User Journeys," etc. are. For non-technical users, these are opaque professional jargon. Each template should open with a one-sentence plain-language explanation of what the document type is and why it exists.

### Factual issue

- `costs.md` references Google Domains, which shut down and migrated to Squarespace Domains. Needs updating.

### CHANGELOG drift (already fixed this session)

- v1.5.1 and v1.5.2 were tagged without CHANGELOG entries. Fixed during this session.
- Added a pre-push git hook to block tag pushes without matching CHANGELOG entries.
