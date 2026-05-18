# ITERATION.md — post-Slice-11

**Cycle:** v4.0.0 closer (Slice 12)
**Opened:** 2026-05-17
**Closed:** 2026-05-17 (same session)
**Status:** Resolved — Slice 12 scoped, designed, implemented in dev-path skill; awaiting commit + ship of v4.0.0.

Resolution summary at the bottom of this file. All three items addressed in Slice 12.

---

## Item 1 — Audit doc-stranger lane saturates (issue #6)

**Source:** GitHub issue [empathetech/hacky-hours-docs#6](https://github.com/empathetech/hacky-hours-docs/issues/6) — filed by conductor via `/hacky-hours issue`.
**Verb affected:** `/hacky-hours audit` — Lane B (doc-stranger / context-free Claude reading project docs).
**Subject project tier:** 1 (personal-use, single-builder).

### What's happening

The doc-stranger lane (a context-free Claude session reading project docs to test the graduation property) saturates after multiple consecutive audit rounds on the same project. Once the earlier rounds' actionable critiques have been addressed, the lane keeps returning 🟡 with new "first-fix" recommendations that are factually false — asking for changes that are already in the docs the stranger just read.

Observed across four audit rounds on a Tier-1 PWA. By round 4, the stranger's first-fix was *"add an anchor callout to the README's opening paragraph and reorder the doc list so STYLE_GUIDE comes before PRODUCT_OVERVIEW"* — both already done and verifiable on the very lines the stranger had read.

### Why it matters

The doc-stranger lane is the framework's built-in graduation test — *"if a context-free Claude session can onboard from the docs, the graduation property is working."* When the lane saturates and starts manufacturing false-negative critiques, the graduation signal loses meaning. The lane is doing what a critical reviewer does (find something), but with no awareness of prior audit history it has no calibration for "this is genuinely saturated."

### Possible directions (not prescriptive — from issue body)

1. **Saturation exit condition** — give the stranger awareness of prior audit runs and what was addressed. Risk: defeats the "stranger" purity.
2. **"What changed since last audit" self-correction pass** as a separate sub-step after the cold read.
3. **Different cold-reader rubric for iterated projects** — switch from *"onboard from cold"* to *"onboard from cold + would you ship this?"* after N audits.
4. **Conductor-side saturation flag** — instruct the top-level consolidator to flag suspected saturation when the stranger's first-fix is verifiable-false (already done after a user-initiated course correction; could be formalized).

### Secondary note from the issue

`/hacky-hours issue` tried to apply labels `user-feedback,v4` per the skill spec; neither label exists on this repo. Either create them upstream or have the verb gracefully omit when labels don't exist. (Bug class: `tools/issue.md` skill spec vs. repo state mismatch.)

---

## Item 2 — Team learning/persistence is half-built (v4 thesis gap)

**Source:** Conductor question during Step 5 — *"confirm that as of the changes we have on this v4.0.0 branch with team, we have functionality to update our team members' context and metadata based on what projects they've worked on with the user."*
**Verbs affected:** every multi-role verb (steps, audit, adopt, arbitrate) + `team update`, `team site`.
**Slice context:** structural pieces shipped across Slices 2, 8, 9; capture step never specified.

### What's claimed (design)

Per V4_DESIGN.md and `tools/team-update.md`:
- Agents learn across sessions/projects via `feedback.md` (durable corrections) and `history.md` (per-project track record)
- During a session, behavior feedback / prompt edits / repeated overrides are captured to `~/.hacky-hours/sessions/<id>/pending/<agent>.md`
- `/hacky-hours team update` promotes accepted pending items into the team repo with a git commit
- The team site renders bios + backgrounds that grow over time

### What's actually wired

- ✅ **Structural slots present.** Every agent folder has `system-prompt.md`, `feedback.md`, `history.md`, `preferences.yml`, `profile.md`. Files have proper boilerplate explaining their intent.
- ✅ **Reader/promoter exists.** `tools/team-update.md` correctly reads `sessions/<id>/pending/`, presents per-change review, commits to team repo. `team-update.md` is well-specified.
- ❌ **No verb writes to `sessions/<id>/pending/`.** Grep across `steps/`, `reviews/`, `tools/` — zero references to capturing pending changes. `team-update.md` line 11 says capture happens "automatically when you give behavior feedback" but no verb file enforces this. The capture step is **specification-by-vibes**.
- ❌ **No verb writes to `history.md`.** Per-project track record is a structural slot that nothing populates. Compaction protocol described in the template never triggers.
- ⚠️ **Live evidence:** `~/.hacky-hours/sessions/` is empty after multiple v4 dogfooding sessions. `~/.hacky-hours/teams/default/` git log shows exactly one commit — the initial template copy. Zero agent updates have ever landed despite extensive use.

### Why this matters

The whole v4 thesis — *"orchestra of stakeholder-role AI agents that learn and grow with context"* — depends on the capture step. Without it:
- The team site is a static yearbook, not a living roster.
- "Persistent team" is structural-only — files exist, never change.
- Slice 11 (team chat) makes the orchestra audible, but the orchestra forgets the conversation as soon as it ends.
- The `feedback.md` and `history.md` slots are decorative.

This is the same failure shape as Item 1 — *a framework memory mechanism that doesn't actually fire.*

### Possible directions (not prescriptive)

1. **Add an explicit capture step to multi-role verbs.** Each step/review/tool file gets a "Phase N — Stash" block at the end: scan the session for behavior feedback given to specific agents, write each to `sessions/<id>/pending/<agent>.md`. Closes the loop minimally.
2. **Add a session-end hook (via settings.yml)** that prompts: *"You had behavior feedback for Maya and Alex during this session. Stash for `team update`?"* — less invasive but requires hook infra.
3. **History.md auto-append at verb completion.** When a verb finishes a meaningful unit of work (a step, an audit, an arbitration), append a one-line entry to each involved agent's `history.md`: date · project · role contribution summary. This part doesn't even require conductor review — it's resume entries, not behavior changes.
4. **End-of-session reminder in SKILL.md or a global hook.** Conductor closes a session; framework prompts: *"You've got N pending changes for agents. Run `/hacky-hours team update` before they're lost."*
5. **Honest deferral.** Mark the capture step as not-shipped in CHANGELOG, add a "team learning closer" slice (Slice 12 or v4.1.0) before claiming v4.0.0 is the thesis-complete release.

### Cross-link to Item 1

Both items are the same failure pattern: framework slots exist, the action that fills them doesn't fire. Worth thinking about whether there's a single design fix (e.g., end-of-verb "stash" convention) that addresses both.

---

## Item 3 — BACKLOG out of sync (housekeeping)

**Observed:** Slice 11 shipped in commit `8ca112c` and is documented in `CHANGELOG.md` under `[Unreleased] — feat/v4.0.0`, but `BACKLOG.md` still lists Slice 11 under "Next Milestone — v4.0.0." Per project-state-machine convention, completed slices should be removed from BACKLOG when their PR/commit lands.

Trivial fix; mention here so it doesn't get forgotten.

---

## Phase 2 — Synthesize (pending)

Once capture is closed: walk each item against design docs.

- **Item 1** → affects `reviews/audit.md` (Lane B specification). May need an ADR if we change the lane's purity contract.
- **Item 2** → affects `tools/team-update.md` (clarify capture-step responsibility), and **every** verb file that fans out to roles (steps/01-05, reviews/audit, tools/adopt, tools/arbitrate). Needs an ADR on **where** capture happens — single end-of-verb step vs. inline behavior-watching vs. session-end hook.
- **Item 3** → BACKLOG hygiene only; no design-doc impact.

## Phase 3 — Prioritize (pending)

Hotfix / next-milestone / backlog assignments — after Phase 2.

## Phase 4 — Amend (pending)

## Phase 5 — Build (pending)

---

## Resolution

All three items addressed in Slice 12 of v4.0.0 (this session). Files changed:

**Slice 12 implementation (dev-path skill files — ship with v4.0.0):**
- `.claude/skills/hacky-hours-dev/references/capture-format.md` *(new)* — canonical contract for capture + history schema, session-ID algorithm, per-verb responsibilities, edge cases
- `.claude/skills/hacky-hours-dev/steps/01-ideate.md` — preamble + Phase N — Stash tail
- `.claude/skills/hacky-hours-dev/steps/02-design.md` — preamble + Phase N — Stash tail
- `.claude/skills/hacky-hours-dev/steps/03-roadmap.md` — preamble + Phase N — Stash tail
- `.claude/skills/hacky-hours-dev/steps/04-build.md` — preamble + per-task Phase N — Stash tail
- `.claude/skills/hacky-hours-dev/steps/05-iterate.md` — preamble + Phase 6 — Stash
- `.claude/skills/hacky-hours-dev/reviews/audit.md` — preamble + Step 5 — Stash + **Lane B saturation guard (closes issue #6)**
- `.claude/skills/hacky-hours-dev/tools/adopt.md` — preamble + Step 8 — Stash (foundational team-meets-project history)
- `.claude/skills/hacky-hours-dev/tools/arbitrate.md` — preamble + Step 5 — Stash (high-signal behavior feedback)
- `.claude/skills/hacky-hours-dev/tools/team-update.md` — reconciled to reference capture-format.md as source of truth; dropped vibes-spec
- `.claude/skills/hacky-hours-dev/tools/issue.md` — **label-detect via gh label list before gh issue create (closes issue #6 tail bug)**

**Design + project artifacts:**
- `hacky-hours/02-design/V4_DESIGN.md` §4.21 — full design rationale for capture step
- `hacky-hours/02-design/decisions/2026-05-17-team-learning-capture.md` *(new ADR)*
- `hacky-hours/02-design/V4_QA.md` — Test 11 (10 sub-tests for end-to-end capture loop, Lane B saturation, label-detect)
- `hacky-hours/04-build/BACKLOG.md` — removed Slice 11 (shipped in commit 8ca112c); added Slice 12; updated unscheduled-backlog notes
- `CHANGELOG.md` (root, symlinked from 04-build) — Slice 12 Added section, Deferred section, Backward compatibility note

**Per-item resolution:**

- **Item 1 (Issue #6 — audit Lane B saturation)** → Addressed via the saturation guard in `reviews/audit.md`. Approach: conductor-side post-Lane-B check (direction 4 from the issue body) cross-references stranger's "first fix" against prior audit history + Lane C verification + actual doc state. Replaces saturated first-fix with a graduation-indicator note. Preserves Lane B subagent purity (it still reads only the docs with no prior context). Counter file `audits/.lane-b-saturation` tracks the streak. Scorecard annotation `· saturated (N)`. Recommend: close GitHub issue #6 with a reference to the resolving commit once landed.

- **Item 1b (Issue #6 tail — labels don't exist)** → Addressed via label-detect in `tools/issue.md`. Probes `gh label list` before `gh issue create`; builds `--label` from intersection of requested and existing; omits entirely if none match (prevents wholesale submission failure). Surfaces missing-labels note in issue body footer so upstream can act.

- **Item 2 (Team learning persistence half-built)** → The v4.0.0 thesis-blocker. Resolved via Slice 12 — canonical capture contract + Phase N — Stash wired into every multi-role verb + reconciled team-update.md. Per the ADR's locked decisions: end-of-verb capture (not inline; not session-hook), silent `history.md` auto-append (review burden would fatigue), reviewed behavior-feedback prompt (always shown), session-ID via `.current-session` marker with 4h staleness window. ADR captures rejected alternatives.

- **Item 3 (BACKLOG out of sync)** → Slice 11 removed from BACKLOG; v4.1+ candidates expanded in unscheduled backlog now that Slice 12's deferral list is known.

**Recommended next steps (conductor's call):**

1. Commit Slice 12 with conventional message: `feat(v4): slice 12 — team learning closer + issue #6 fixes`
2. Run V4_QA.md Test 11 against a test project to verify the end-to-end loop (especially the 11.6 "next session uses the updated agent" check — that's the thesis verification)
3. Close GitHub issue #6 with a comment referencing the resolving commit
4. v4.0.0 is now thesis-complete and ship-ready. Suggested order: `/hacky-hours audit` (now with saturation guard), then `/hacky-hours update 1` to publish the GitHub Release

Archive this file at `hacky-hours/archive/iteration-2026-05-17.md` after commit.
