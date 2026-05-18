# ADR: Team learning capture step (Slice 12)

**Date:** 2026-05-17
**Status:** Accepted
**Slice:** 12 (v4.0.0)
**Arbitration mode:** decide (conductor + framework synthesis)

## Context

V4.0.0's headline thesis is *"orchestra of stakeholder-role AI agents that learn and grow with context."* Slices 2 and 8 shipped the destinations (per-agent files: `feedback.md`, `history.md`, `system-prompt.md`, `preferences.yml`) and the promoter (`/hacky-hours team update`, which reads pending entries from `~/.hacky-hours/sessions/<id>/pending/` and commits accepted ones into the team repo). Slice 9 shipped the team site rendering agent profiles.

A Step-5 iteration on the v4.0.0 branch surfaced a thesis-blocking gap:

- **No verb writes to `sessions/<id>/pending/`.** Grep across `steps/01–05`, `reviews/audit`, `tools/adopt`, `tools/arbitrate` — zero references to capturing pending changes. `team-update.md` line 11 claims capture happens "automatically when you give behavior feedback" but no verb file enforces it.
- **No verb writes to `history.md`.** The per-project track record is a structural slot nothing populates.
- **Live evidence:** after extensive v4 dogfooding, `~/.hacky-hours/sessions/` was empty and the default team's git log showed exactly one commit (the initial `cp -R` from the template). Zero agent updates had ever landed.

The conductor's question that surfaced the gap: *"as of the changes we have on this v4.0.0 branch with team, do we have functionality to update our team members' context and metadata based on what projects they've worked on with the user?"* The honest answer was no — the slots exist, the promoter exists, but the capture step was unspecified.

## Roles involved

- **🏗️ Priya (Architect)** — capture must fire at a discrete, observable moment or it won't fire at all. Inline-capture (assistant watches for behavior feedback mid-conversation) depends on the assistant correctly classifying mid-flow remarks — exactly the vibes-spec we're trying to fix. End-of-verb is the only reliably-fired moment without harness hooks.
- **📊 Maya (Product)** — pushed scope discipline: wire the pattern end-to-end through one verb first (proof-of-loop), then propagate. Conductor overrode in favor of combined-slice scope on grounds of "this is a thesis-blocker, ship it complete." Both shapes documented in ITERATION.md for the record.
- **📈 Yuki (Data)** — pending-entry schema and history-entry schema need distinct shapes because they have distinct review semantics (review-required vs. silent fact-of-record).
- **🔍 Emma (QA)** — test plan needs to validate the end-to-end loop, not just per-step file writes. Without a test that proves "session capture → team-update accept → agent learned from it," the same gap could reappear.

## Decision

Slice 12 adds an explicit **Phase N — Stash** step at the tail of every multi-role verb. The Stash step does two things in fixed order:

1. **History append (silent)** — for each agent that actually participated in the verb, append one line to that agent's `~/.hacky-hours/teams/<active>/agents/<agent-id>/history.md` with a structured summary (`date · project · verb · contribution`). Committed in a single git commit on the team repo at end-of-verb. No conductor review required — these are facts, not editorial.

2. **Behavior feedback prompt (opt-in, always shown)** — print one prompt: *"Anything you said during this run that should change how an agent works in future sessions? Free-form by agent, or `none`."* For each agent named, write `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the canonical schema. The conductor reviews and promotes these via `/hacky-hours team update`.

The canonical contract for both lives in `references/capture-format.md` (single source of truth). Every multi-role verb's tail reads it and follows.

Session ID resolution is via a `.current-session` marker file in `~/.hacky-hours/sessions/`, regenerated when its `mtime` is >4 hours old. No coupling to Claude Code's process lifetime (which skills can't observe).

The behavior-feedback prompt is always shown — even if the conductor expects to answer `none`. The micro-cost of one extra prompt buys a habit-forming surface that closes the v4 thesis. Silence here was the failure mode that produced the bug.

## Rationale

**Why end-of-verb instead of inline capture.** Inline capture asks the assistant to classify mid-conversation conductor remarks as "this is behavior feedback for an agent." Classification rules are inherently fuzzy — the failure mode is exactly the current state of v4.0.0-dev's persistence: "we said capture happens automatically" with no mechanism that fires. End-of-verb gives capture a discrete, named moment with a structured prompt the conductor explicitly answers.

**Why both slots fire at the same moment.** History append and behavior-feedback prompt are co-located because they share trigger conditions (verb completion + identified participants). Splitting them into separate phases doubles the interruption cost and the implementation surface.

**Why history.md auto-appends (silent).** History is a record-of-fact: *"Maya worked on the audit verb at hacky-hours-docs on 2026-05-17."* You can't reject a fact. Requiring conductor review per entry would (a) interrupt every verb run, (b) fatigue to "approve all" within days, and (c) defeat the team-site goal — the site comes alive *because* history accumulates without friction.

**Why behavior feedback always requires review.** A behavior change ("Maya, lead with concrete examples before scope discussion") is editorial. The conductor's intent at capture may not be their intent days later. Forcing the round-trip through `team update` gives them the option to refine, reject, or defer.

**Why a `.current-session` marker file with 4h staleness.** Skills can't observe Claude Code's process boundaries reliably. A timestamp-based heuristic with `mtime` touch on every capture means an active session keeps its ID indefinitely; a gap of 4+ hours starts a fresh one. The escape hatch (delete the marker manually) covers users who want explicit control.

**Why a single canonical contract (`references/capture-format.md`) instead of per-verb capture sections.** Slice 11 set this pattern with `references/chat-format.md`. Centralizing the spec means changes happen in one file, verb files stay thin, and the contract is auditable as a single artifact. Same principle as design-doc DRY.

**Why ship as one combined slice instead of 12a/12b.** The conductor's call. The combined-slice cost is touching ~10 verb files instead of 1 + 9; the upside is a complete thesis at v4.0.0 ship time. Counterargument (Maya): the combined slice forecloses pattern revision after first-touch — if the capture format needs adjusting after we see it in practice, every verb file must be re-touched. Mitigation: the canonical contract lives in one file, so format changes affect verb files only via the boilerplate footer (small surface).

**Why add `team backfill` to Slice 12 (mid-scope addition).** Forward-capture (Stash phase) handles work done after Slice 12 lands. Long-running projects that adopted v4 mid-stride — including hacky-hours-docs itself — need *retroactive* population, or agents' track records start empty on day-one of v4.0.0 install. The team site renders bios with no history; agents look like they've never worked on the project even when they've shaped most of it. Without backfill, the persistence loop only closes for fresh projects. The conductor surfaced this gap mid-Slice-12-implementation: *"will `team update` work manually to pick up on a repo that has gone through changes?"* The honest answer was no — `team update` is a forward-only promoter of pending entries written by verbs. Adding `team backfill` as a separate one-shot retroactive verb (read CHANGELOG/git → classify by file paths and keywords → propose history entries per agent → batch review → commit per agent batch) closes the gap without changing forward-capture semantics. Ship with v4.0.0 so the persistence story is retroactively complete on day-one.

**Backfill review semantics differ from forward-capture by design.** Forward-capture appends `history.md` silently because the conductor just watched the verb produce the contribution — the entry is fact, no review needed. Backfill bulk-proposes dozens of entries per agent from a source the conductor hasn't been watching, classified heuristically. Per-agent batch review (with `select` for entry-level granularity when needed) is the right gate — same model as `team update`'s pending review for behavior feedback, but scoped per-agent and per-batch rather than per-entry. Annotated `(backfilled, <anchor>)` so retroactive entries are distinguishable from forward-captured ones; the anchor (CHANGELOG section or git SHA) gives verifiable provenance.

## Consequences

**What changes downstream:**

- Every multi-role verb gains a tail Stash phase (steps/01–05, reviews/audit, tools/adopt, tools/arbitrate). Single-role verbs are unaffected.
- `~/.hacky-hours/sessions/` actually accumulates state during normal use.
- `~/.hacky-hours/teams/<active>/` accumulates commits — one per verb completion for history, plus separate commits via `team update` for behavior changes.
- The team site (`/hacky-hours team site`) starts surfacing real per-agent history once any work has happened — bios become living documents.
- `tools/team-update.md` is updated to reference the canonical contract (no longer claims "captures automatically" with no source).
- `tools/team-site.md` (or its template) may want to surface `history.md` summaries on agent profile pages in a follow-up — out of scope for Slice 12 but enabled by it.

**What we're committed to:**

- Every multi-role verb run prints one Stash prompt. This is a UX cost we're choosing to pay for the persistence loop.
- The team repo gets `git commit` traffic at end of every multi-role verb. Conductors with a team git remote (rare; default is local-only) will see push pressure accumulate; we surface this in the footer.
- The capture format becomes a stable contract — third-party verbs (if any future plugins target the framework) need to honor it.

**What we're not doing yet (deferred to v4.1+):**

- **History compaction.** When `history.md` exceeds ~500 lines or ~10k tokens, the boilerplate says compaction should summarize older entries and archive. Slice 12 ships the append; compaction is a daemon-style task that needs more thought (when does it run, who triggers it, conductor-reviewed or automatic). Until then, long histories just produce long files. Git preserves the raw record.
- **Implicit feedback capture.** "User overrides agent recommendation more than once in similar shape → write a pending entry implicitly." Real signal, but classification is fuzzy and the failure mode is the one we're already fixing. Re-evaluate after we see how the explicit prompt performs in practice.
- **History rendering on the team site.** The site reads `profile.md`; it doesn't surface `history.md` yet. v4.1+ candidate once we have enough accumulated entries to know what surfacing pattern works.
- **Per-verb capture-mode override.** `~/.hacky-hours/settings.yml` could add `team_learning.stash_prompt: end_of_verb | end_of_session | off` for conductors who want to tune intensity. Defer until we have signal that the always-on prompt is too noisy in practice.

## Alternatives considered (and not chosen)

- **Inline capture (assistant watches mid-flow).** Rejected — depends on classification rules that don't exist. Failure mode is the current state.
- **End-of-session hook only.** Rejected — Claude Code skills can't reliably hook session-end events without harness coupling. Also loses the per-verb context that makes capture summaries useful.
- **Conductor-initiated capture only (`/hacky-hours team stash <agent> <feedback>`).** Rejected — depends on the conductor remembering to invoke a separate verb. Habit-formation needs the prompt in-flow.
- **Capture only the behavior feedback; skip history.md.** Rejected — history.md is the team-site lifeblood. Without it, agent profiles stay static and the "team grows with context" claim stays unsupported even with behavior feedback wired.
- **One pending file per session per agent, mutated across verbs.** Rejected — makes audit harder and conflict semantics worse. One-file-per-agent-per-verb gives `team update` a clean per-event review surface.
- **Tie session ID to a hash of cwd + day.** Rejected — too coarse (multiple Claude Code sessions in one project per day get conflated) and surfaces project paths in session IDs (privacy adjacent).
- **Have `team update` auto-detect "no pending entries → offer to backfill from project history."** Rejected — conflates two different operations (forward-promote vs. retroactive-populate) into one verb with different review semantics and different commit patterns. Two separate verbs (`team update` and `team backfill`) keep each operation's contract clean and let the conductor decide explicitly which they want. Same shape as Slice 11's choice to make `team chat` a subcommand of `team` rather than an implicit mode of every verb.

## Related

- Slice 11 (`references/chat-format.md`) — set the pattern of "canonical contract referenced by every multi-role verb." Slice 12 follows the same architecture.
- `tools/team-update.md` — the consumer of pending entries; updated as part of Slice 12 to reference this contract instead of claiming automatic capture.
- `~/.hacky-hours/teams/<team>/agents/<agent>/feedback.md` and `history.md` templates — the destinations.
- ITERATION.md Item 2 — the gap that catalyzed this slice.
