# Step 4 — Build

*Supporting file for the `hacky-hours` skill. Loaded when the user is at Step 4.*

**Context:** Read `04-build/BACKLOG.md` to see what's queued. For each task, read the relevant design doc sections — particularly `SECURITY_PRIVACY` and `LICENSING.md`. If `ROADMAP.md` exists, confirm the task belongs to the current milestone before starting.

**Purpose:** Implement incrementally, with review at each step, aligned to design decisions.

**Team chat mode:** Before producing any role-driven output, read `${CLAUDE_SKILL_DIR}/references/chat-format.md` and honor the current `team_chat` value from `~/.hacky-hours/settings.yml` (default `minimal`) throughout this verb. **No tokens for tokens' sake** — every voice turn must add information.

Before starting any task:
1. **Read the deep-dive design docs (`<DOC>-deep.md`), not the summaries.** The deep dive is the source of truth and contains the Implementation Notes section that drives the build. Summaries are derivative — for human gut-checks only — and intentionally omit build-phase detail.
2. If a project still has single-tier design docs (e.g., `ARCHITECTURE.md` without the `-deep` / `-summary` split), read those. The two-tier pattern is opt-in for projects upgrading from earlier versions.
3. If a design doc doesn't address something you need to implement, surface it to the user first — the deep dive may need a new section. Update the deep dive, then regenerate the summary.

The task cycle:
1. Pick a task from BACKLOG.md
2. Create a branch named for the task (e.g., `feat/user-signup`, `fix/login-error`)
3. Implement — referencing design documents throughout
4. Before marking complete, verify against the pre-merge checklist (see SKILL.md)
5. Commit with a clear message, push, open a pull request for human review
6. Merge, update CHANGELOG.md, tag a release when a milestone is complete

**Milestone housekeeping (run when BACKLOG.md is empty):**
- Append milestone entry to CHANGELOG.md; move entries older than 3 releases to `archive/changelog/`
- Move the completed roadmap milestone section to `archive/roadmap/`
- Update any design docs that changed; write ADRs for significant decisions
- Move `IDEATION.md` to `archive/` if not already done
- Review `.claudeignore` — anything newly cold that should be excluded?
- Tag the release

**Done when:** All milestone tasks are merged, CHANGELOG.md is updated, and you've cut a tagged release. 🎉
