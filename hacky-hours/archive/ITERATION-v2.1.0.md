# ITERATION.md

**Post-v2.0.0 iteration log** | hacky-hours-docs

---

## Captured Items

### Research: Skill format vs. slash command format

**Captured:** 2026-04-14

The Claude Code `SKILL.md` format exists alongside the slash command format (`.claude/commands/`). This repo currently uses slash commands exclusively. A `hacky-hours` skill and `hacky-hours-dev` skill also exist in the session environment — unclear whether these were created separately or are auto-derived.

**Questions to answer:**
- What does the SKILL.md format provide that the slash command format doesn't?
- Are skills the forward-looking mechanism for this kind of framework assistant?
- Is there meaningful overlap between the two, or do they serve distinct purposes?
- If skills are the preferred format, what would a migration look like and what version would it warrant?

**Triage:** Research spike — no implementation until the above is answered.

---

### Documentation update: README and all docs to v2.0.0 terminology

**Captured:** 2026-04-18

**Completed:** 2026-04-18

README.md was out of date with v2.0.0. Identified and fixed across 20+ files:
- Level → Step language throughout all template docs, runbooks, and README
- Diagram updated to show five steps including Step 5 — Iterate with loop-back
- Stale v1.x command references replaced with v2.0.0 equivalents (`step 1–5`, `review 1–3`, `update 1–2`, `tools upgrade`, etc.)
- Inclusive language: "paralyzed" → "stuck in endless planning" (follow-up to PR #2)
- `hacky-hours/` self-documentation intentionally left as-is (historical record)

**Triage:** ✅ Complete — no backlog items needed.

---

### Design exploration: Two-tier design artifacts (human summary + deep doc)

**Captured:** 2026-05-06

Live demos with non-engineers reveal a tension: the framework produces comprehensive design docs that are well-suited for AI/engineers to build from, but feel like "walls of text" to non-technical stakeholders trying to learn. Sessions take ~3 hours and most of that is planning, with output volume that risks users rubber-stamping AI-generated content rather than internalizing it.

**Hypothesis:** Each design doc could have two layers — a short, visual, human-facing summary (the artifact the user signs off on) and a deeper technical expansion (AI's working notes for build time). If the summary is *primary* — the thing the human commits to — it flips cognitive load back toward the human. The deep doc exists to serve build, not to be read cover-to-cover.

**Design questions to answer:**
- Is the summary a separate file (`SUMMARY.md`) or a capped top section of the existing doc?
- What's the standard shape for a summary? Candidate: problem / decision / tradeoff / diagram / what's next.
- How is length enforced? ("One screen, no scrolling" as a forcing function.)
- Should diagrams (Mermaid) lead the summary instead of being buried inline?
- Does the summary get generated *from* the deep doc, or does the deep doc expand *from* a human-signed-off summary? (The latter is the version that resists the AI-rubber-stamp trap.)
- Which Step 2 docs benefit most from this two-tier shape? Probably ARCHITECTURE, DATA_MODEL, USER_JOURNEYS — the ones non-technicals most need to align on.

**Why it matters:** Connects to the broader product shift from "framework that produces docs" to "framework that produces *understanding*." Likely warrants an ADR before becoming a backlog item.

**Triage:** Design spike — needs exploration before scoping into BACKLOG.

---

## Status

*In progress — items being captured. Skill format research and two-tier artifact exploration not yet triaged.*
