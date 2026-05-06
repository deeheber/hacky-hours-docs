# Review 3 — Pivot

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `review 3` / `review pivot`.*

**Context:** Read ALL framework artifacts under ROOT_PATH: `PRODUCT_OVERVIEW.md`, every design doc in `02-design/`, `ROADMAP.md`, `BACKLOG.md`, `CHANGELOG.md`, ADRs in `02-design/decisions/`, and `ITERATION.md` if it exists. Build a complete mental model before asking anything.

**Purpose:** Go back to the foundational questions with the full benefit of everything built and learned. This is for when the direction itself needs rethinking, not the execution.

**Always confirm before modifying any files. Pivot can change everything.**

---

**Phase 1: Read and summarize current state**

Present a concise summary:
> "Here's what your docs currently say: Who: [X]. What: [X]. Why: [X]. Architecture: [key points]. Shipped: [last 2-3 releases]. Queued: [backlog]."

Then ask: "What's changed? What's making you rethink the direction?"

---

**Phase 2: Revisit Step 1 questions**

Walk through the PRODUCT_OVERVIEW 5Ws as re-evaluation. Note whether each has changed. Focus on what's actually shifting — skip unchanged Ws quickly.

---

**Phase 3: Identify the diff**

```
Product direction diff:
  Who:    [unchanged] / [changed: was X, now Y]
  What:   [unchanged] / [changed: was X, now Y]
  ...
```

Ask: "Does this diff capture the pivot accurately?"

---

**Phase 4: Cascade through Step 2**

For each change in the diff, identify which design docs are affected. For each: amend (update sections), rewrite (start over), or retire (no longer relevant)? Also check for docs that should be created or consolidated.

For two-tier docs (v3.0.0+): pivots land in the **deep dive first** (the source of truth). Once the deep dive reflects the new direction, regenerate the summary from it. Never edit the summary directly during a pivot.

---

**Phase 5: Cascade through Steps 3 and 4**

- **Roadmap:** Which milestones still make sense? Rewrite with new direction.
- **Backlog:** Clear items that no longer align. Add new items. Note what survived unchanged.

---

**Phase 6: Record the pivot**

Write an ADR: `02-design/decisions/YYYY-MM-DD-pivot-<topic>.md`. Update `PRODUCT_OVERVIEW.md`. Add a note at the top pointing to the ADR.

Update CLAUDE.md if path references changed. Archive retired docs — never delete.

**Done when:** PRODUCT_OVERVIEW.md reflects the new direction, all design docs are consistent, roadmap and backlog are updated, and an ADR documents the pivot. ✅
