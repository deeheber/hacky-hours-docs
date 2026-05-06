# BACKLOG.md

**Step 4 — Build** | hacky-hours-docs

---

## Next Milestone

*No milestone assigned yet.*

---

## Backlog (unscheduled)

### ADR: Migrate to SKILL.md format

**Type:** ADR drafting
**Branch:** `docs/adr-skill-migration`

Spawned from completed research spike (`02-design/research/2026-05-06-skill-vs-slash-command.md`). Draft an ADR capturing the decision to migrate from the slash command format to SKILL.md, the rationale (Anthropic's official direction; bundled supporting files unlock the two-tier artifacts work), and consequences (install path change, v3.0.0 bump).

**Output:** `02-design/decisions/YYYY-MM-DD-migrate-to-skill-format.md`.

---

### Migration: Slash command → SKILL.md format (v3.0.0)

**Type:** Implementation
**Branch:** `feat/migrate-to-skill-format`
**Gated on:** ADR approval + two-tier artifacts design spike (co-design recommended)

Move `commands/hacky-hours.md` to `skills/hacky-hours/SKILL.md` with proper frontmatter (`disable-model-invocation: true`, `allowed-tools`, `argument-hint`). Update install scripts to write to the new path and clean up the old file. Update `hacky-hours-dev` similarly. Targets v3.0.0 due to install-path change.

**Scope (combined with two-tier artifacts spike):**
- Refactor SKILL.md into entrypoint + bundled supporting files (per-step guidance, per-design-doc templates as summary + deep pairs)
- Update install scripts (`install.sh`, `install.ps1`) for new path; clean up old `commands/hacky-hours.md`
- **Update README.md** to document:
  - The new skill-based architecture (entrypoint + bundled files; two-tier templates)
  - Migration instructions for users on v2.x → v3.0.0 (re-run install script; old file is auto-removed)
  - Why the split exists (human summary vs. AI deep doc — connects to the two-tier philosophy)
- Update `runbooks/using-this-repo/import-as-resource.md` if path references changed
- Add CHANGELOG entry under `[3.0.0]` with breaking-change callout

---

### Design spike: Two-tier design artifacts (human summary + deep doc)

**Coupled with:** Skill migration above — bundled supporting files in SKILL.md format are the natural home for two-tier templates. Recommend co-designing.

**Type:** Design exploration → ADR
**Branch:** `design/two-tier-artifacts`

Live demos with non-engineers reveal that the framework's comprehensive design docs feel like "walls of text" to non-technical stakeholders. Risk: users rubber-stamp AI-generated content rather than internalizing it. Hypothesis: each design doc could have a short, visual, human-facing summary (the artifact the user signs off on) plus a deeper technical expansion (AI's working notes for build time).

**Design questions:**
- Separate file (`SUMMARY.md`) or capped top section of the existing doc?
- Standard shape for a summary? Candidate: problem / decision / tradeoff / diagram / what's next.
- How is length enforced? ("One screen, no scrolling" as a forcing function.)
- Diagrams (Mermaid) lead the summary instead of being buried inline?
- Summary generated *from* the deep doc, or deep doc expanded *from* a human-signed-off summary? (The latter resists the AI-rubber-stamp trap.)
- Which Step 2 docs benefit most? Probably ARCHITECTURE, DATA_MODEL, USER_JOURNEYS.

**Output:** ADR proposing the two-tier shape, plus a small prototype on one design doc to test the pattern.
