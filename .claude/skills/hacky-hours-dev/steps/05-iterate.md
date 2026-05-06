# Step 5 — Iterate

*Supporting file for the `hacky-hours` skill. Loaded when the user is at Step 5.*

**Context:** Read `04-build/CHANGELOG.md` to understand what shipped in the last release. Read `04-build/BACKLOG.md` to see if anything is already queued. Skim the Step 2 design docs.

**Purpose:** Capture bugs, ideas, and improvements after a release, amend the docs that need updating, and queue the work.

**Phase 1: Capture**

Before asking the user anything, check `ROOT_PATH/feedback/` for any feedback files (`feedback-<username>-<timestamp>.md`). If files exist, read and summarize them. Tell the user: "I found N feedback file(s) from recent learn sessions. Here's what they say: [summary]."

Then ask the user to brain-dump freely: bugs, feedback, ideas for improvements. Write everything into `ITERATION.md` under ROOT_PATH. No filtering yet — just capture.

Prompts:
- "What's broken or annoying that you've noticed since the last release?"
- "What did users ask for that you didn't have time to build?"
- "What would you change about the design now that you've seen it work in practice?"

**Phase 2: Synthesize**

Read `ITERATION.md` alongside the existing design docs. For each item:
- Does this change how the product works? → Flag the relevant design doc for amendment
- Does this introduce a new design decision? → Note that an ADR will be needed
- Is this purely an implementation fix? → Goes straight to backlog

**Lightweight review check:** While reviewing design docs, flag any that look oversized, stale, or mostly placeholder. If multiple docs are flagged, suggest running `/hacky-hours review 2` after the iteration cycle completes.

**Phase 3: Prioritize**

Categorize each item:
- **Hotfix** — broken in production, needs immediate attention
- **Next milestone** — important enough to be in the next planned release
- **Backlog** — valid but not urgent; add to BACKLOG.md without a milestone assignment

**Phase 4: Amend design docs**

For each flagged design doc, work through the needed changes. Write ADRs for significant decisions. Update affected sections.

**Phase 5: Build**

Proceed with the Step 4 build cycle using the updated backlog.

**Done when:** ITERATION.md has been fully triaged, design docs reflect current reality, and new items are in BACKLOG.md. Move `ITERATION.md` to `ROOT_PATH/archive/` when complete. ✅
