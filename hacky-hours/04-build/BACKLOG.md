# BACKLOG.md

**Step 4 — Build** | hacky-hours-docs

---

## Next Milestone — v4.0.0

### Slice 12 — Team learning closer (capture step + audit Lane B saturation guard + issue label-detect)

**Type:** Implementation (v4.0.0 thesis closer)
**Branch:** `feat/v4.0.0` (continuing on the same release branch)
**Design:** `02-design/V4_DESIGN.md` §4.21
**ADR:** `02-design/decisions/2026-05-17-team-learning-capture.md`
**Origin:** Step 5 iteration on `feat/v4.0.0` (2026-05-17). ITERATION.md surfaced that the v4 persistence story was half-built — files exist, promoter exists, no verb writes to them. Also bundles issue #6 (audit Lane B saturation) since both items are the same failure shape ("framework memory mechanism that doesn't fire").

Close the v4 thesis loop: agents actually learn and grow with context. Plus fix issue #6.

**Scope:**

*New canonical contract:*
- `references/capture-format.md` — pending-entry schema, history-line schema, session-ID resolution algorithm, per-verb implementation responsibilities, edge cases

*Phase N — Stash wired into every multi-role verb:*
- `steps/01-ideate.md`, `steps/02-design.md`, `steps/03-roadmap.md`, `steps/04-build.md`, `steps/05-iterate.md` — preamble + tail Stash block
- `reviews/audit.md` — preamble + Step 5 Stash block
- `tools/adopt.md` — preamble + Step 8 Stash block (foundational team-meets-project history)
- `tools/arbitrate.md` — preamble + Step 5 Stash block (high-signal behavior feedback moments)

*Team-update.md reconciliation:*
- `tools/team-update.md` — drop the "captures automatically when..." vibes-spec; reference `references/capture-format.md` as source of truth; clarify behavior-feedback vs. history-append paths

*Retroactive companion: `/hacky-hours team backfill` (closes the "what about existing project history" gap):*
- New verb `tools/team-backfill.md` — reads the bound project's CHANGELOG.md (or git log), classifies each entry by discipline (file paths + keywords → agent), proposes per-agent history batches, conductor reviews per-agent (accept all / select / edit / reject / defer), commits per agent batch
- Backfilled entries annotated `(backfilled, <CHANGELOG-anchor-or-SHA>)` for distinguishability + provenance
- `tools/team.md` routing — `team backfill` subcommand
- `SKILL.md` — help message + argument-hint
- `references/capture-format.md` — backfill semantics section (review-per-agent-batch vs. silent for forward-capture; per-agent commits vs. per-verb commits)

*Issue #6 fix (Lane B saturation guard):*
- `reviews/audit.md` — Lane B subagent prompt unchanged (preserves stranger purity); new post-Lane-B conductor-side saturation guard cross-checks the "First fix" recommendation against prior audit history + Lane C verification + current doc state; replaces saturated first-fix with a graduation-indicator note; `audits/.lane-b-saturation` durable counter file; scorecard annotation `· saturated (N)` on the Documentation dimension

*Issue #6 tail bug fix:*
- `tools/issue.md` — label-detect via `gh label list` before `gh issue create`; build `--label` from intersection of requested and existing labels; omit `--label` entirely if no intersection (prevents wholesale submission failure); surface missing-labels note in issue body footer

*Design + docs:*
- `02-design/V4_DESIGN.md` §4.21 — full design rationale
- `02-design/decisions/2026-05-17-team-learning-capture.md` — ADR
- `02-design/V4_QA.md` Test 11 — 10 sub-tests covering history append, behavior feedback prompt, "none" answer, team-update promotion, next-session-uses-update verification, session-ID staleness, Lane B saturation, issue.md label-detect, team site reflection

*Misc:*
- CHANGELOG entry under `[Unreleased] — feat/v4.0.0` as "Slice 12 — team learning closer"
- BACKLOG housekeeping: remove Slice 11 (shipped in commit 8ca112c, already in CHANGELOG)

**Done when:**
- Running any multi-role verb appends a `history.md` line per participating agent and commits to the team repo, and the conductor sees a behavior-feedback prompt at end-of-verb.
- A behavior note written by the prompt lands in `~/.hacky-hours/sessions/<id>/pending/<agent>.md` with the canonical schema. `/hacky-hours team update` reads it, promotes it on accept, and the next session's verb output reflects the change.
- `/hacky-hours team backfill` on this very repo (hacky-hours-docs, with its full v3 + v4 CHANGELOG) produces per-agent batches that the conductor can accept; resulting history.md files reflect the project's lifetime; team site shows non-empty histories for the agents that actually shaped this codebase.
- After 3 audits where prior asks have been addressed, Lane B's "First fix" gets replaced with a saturation graduation indicator rather than manufacturing a false-negative critique.
- `/hacky-hours issue` succeeds against `empathetech/hacky-hours-docs` even when `user-feedback` and `v4` labels don't exist upstream — the verb omits `--label` and notes the gap in the issue body.
- V4_QA.md Test 11 passes all 12 sub-tests on a fresh install (10 forward-capture + Lane B saturation + issue label-detect; plus 2 new backfill sub-tests).

---

### Slice 13 — Agent representation (team site history + auto-evolving profile + résumé + reflection)

**Type:** Implementation (v4.0.0 thesis surface)
**Branch:** `feat/v4.0.0` (continues on the release branch)
**Design:** `02-design/V4_DESIGN.md` §4.22
**ADR:** `02-design/decisions/2026-05-17-agent-representation.md`
**Origin:** Conductor confirmation during Slice 12 ship — *"the point of the team site and having these team avatars are that they are learning and growing with context; I want to treat these AI agents like human team members."* Slice 12 closed the persistence loop in data; Slice 13 closes it in the visible layer.

Make the orchestra appear as teammates with track records. Four coordinated pieces, all in v4.0.0.

**Scope:**

*Derived metrics block:*
- New `metrics:` frontmatter block in every agent's `profile.md` (auto-managed; conductors don't hand-edit)
- Schema in `references/capture-format.md` §"Derived metrics" + §"Level derivation"
- Refresh hook bundled into history-append step of every multi-role verb's Stash phase + `team backfill` per-agent batch + `team reflect`
- Single git commit per refresh (bundled with history)

*Team-site generator updates (un-defers v4.1+ deferral from Slice 12):*
- `templates/team-site/generate.py` — reads `history.md`, `feedback.md`, metrics block, and `resume.md` per agent
- Profile page additions: "Recent track record" timeline (last 10), "Lessons applied" section, résumé link (when present), level + contribution-count in header metadata
- Index card additions: level badge + contribution count (hidden for level-0 agents)
- New `render_resume_page` for standalone résumé HTML pages
- CSS additions for new sections; mobile-responsive
- All pure Python stdlib; no new dependencies

*New verbs:*
- `tools/team-resume.md` — synthetic résumé generator; three style presets (`minimal` / `standard` / `deep`); fact-derived only; outputs `agents/<id>/resume.md`
- `tools/team-reflect.md` — opt-in conductor-invoked self-reflection; refreshes Track record section in profile (silent); proposes prose updates via `team update` pending flow (`kind: prose_update`); prints self-observations for conductor to optionally stash as behavior feedback

*Routing + help:*
- `tools/team.md` — routes `team resume` and `team reflect` subcommands; help message
- `SKILL.md` — argument-hint + help message

*Capture-format contract extensions:*
- §"Derived metrics" (schema)
- §"Level derivation" (table + breadth bumps)
- §"Resume composition" (cross-reference to `team-resume.md`)
- §"Reflection semantics" (cross-reference to `team-reflect.md`)
- Step 5 of Implementation responsibilities (metrics refresh in same commit as history append)

**Done when:**
- After any multi-role verb run, the participating agents' `profile.md` files have an updated `metrics:` block bundled in the same commit as the history append. Levels and counts are accurate.
- `/hacky-hours team resume <agent-id>` writes `resume.md` composited from sources. `--all` works. Honest about thin work (no padding for zero-history agents).
- `/hacky-hours team reflect <agent-id>` refreshes Track record section silently, proposes prose updates as pending entries, and surfaces self-observations the conductor can opt to stash.
- `/hacky-hours team site build` after the above produces HTML pages where: index cards show level badges; profile pages show Recent track record + Lessons applied + résumé link; résumé pages render at `agents/<id>-resume.html` with back-link to profile.
- V4_QA.md Test 12 passes all 10 sub-tests on a fresh install (metrics refresh, resume generation, reflection flow, team site rendering, hybrid bio editing semantics).
- After backfilling this very repo (`hacky-hours-docs`), running `team resume --all`, and rebuilding the team site: agents that have shaped this codebase render with real histories, real lessons, real résumés, and accurate level badges. The thesis becomes visible.

---

## Backlog (unscheduled)

### BACKLOG hygiene pass (post-v4.0.0)

Cross-check `02-design/V4_DESIGN.md` deferred-scope list against shipped slices and re-seed the unscheduled backlog with the actual v4.1+ candidates. After Slice 12, the known v4.1+ items include:

- **History compaction** — automated rollup of `history.md` past ~500 lines / ~10k tokens into a "Key facts and patterns" summary at top with raw entries archived to `history-archive/<date>.md`. Deferred from Slice 12 per ADR.
- **Implicit feedback capture** — detect repeated conductor overrides of an agent's recommendation and stash a pending entry implicitly. Real signal but classification is fuzzy; re-evaluate after explicit prompt has run a release cycle.
- **Team site history rendering** — surface `history.md` on agent profile pages. Needs design once we have enough accumulated entries to know what pattern works.
- **Per-verb stash-mode override** in settings.yml (`team_learning.stash_prompt: end_of_verb | end_of_session | off`). Defer until we have signal that always-on prompt is too noisy.
- **Extensibility for additional roles** beyond the core 12 (e.g., DBA, Mobile, Performance Eng).
