# Review 2 — Optimize

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `review 2` / `review optimize`.*

**Context:** Read ALL framework docs under ROOT_PATH, the project's `CLAUDE.md`, and `.claudeignore`. For projects with code, also read the codebase structure, package manifests, and key implementation files.

**Purpose:** A deep review comparing design intent against current reality, proposing specific, actionable changes. This is not a metrics dashboard — it reads everything, understands the intent, and tells you what to fix.

Run all phases in order, then present a unified report.

---

**Phase 1 — Design Intent vs. Current Reality**

For each design doc, compare against what actually exists. Report:
- **Accurate** — doc matches reality
- **Stale** — specific sections that no longer reflect current state
- **Missing** — things that exist in the project but aren't covered
- **Contradicted** — design says X, implementation does Y

For two-tier docs (v3.0.0+): the deep dive is the source of truth and what implementation reads. Compare against reality starting from the deep dive. Then validate the summary against the deep dive — flag if the summary makes claims the deep dive doesn't, or omits load-bearing detail from the deep dive's Key Decisions / Known Constraints sections.

---

**Phase 2 — Structural Efficiency**

- **Redundancy:** Multiple docs covering the same ground?
- **Dead artifacts:** Docs, sections, or folders that exist but serve no purpose?
- **Missing artifacts:** Complexity not yet documented?
- **CLAUDE.md alignment:** Does it include a Project State Machine? Reference the right design docs?
- **`.claudeignore` effectiveness:** Is cold content excluded? Is anything excluded that shouldn't be?

---

**Phase 3 — Cross-Reference Integrity**

Check all references between docs, from the SKILL.md routing, and in CLAUDE.md. Flag broken references with the exact file, line, and what it points to.

---

**Phase 4 — Actionable Recommendations**

Group by priority:

- **[FIX] Corrections** — factually wrong or contradicted
- **[UPDATE] Stale content** — was true but isn't anymore
- **[TRIM] Efficiency gains** — consumes context without adding value
- **[ADD] Missing coverage** — things the project does that aren't documented
- **[REFACTOR] Structural improvements** — reorganizations that would improve clarity

For each recommendation: what to change, where (file + section), why it matters, whether you can implement it now.

---

**Phase 5 — Save Report (optional)**

Ask to save to `ROOT_PATH/audits/YYYY-MM-DD-optimize.md`. If the user confirms changes, implement them.
