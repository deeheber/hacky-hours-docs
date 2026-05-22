# ADR: Automated team learning — auto-promote / queue split + cross-role propagation

**Date:** 2026-05-22
**Status:** Accepted
**Slice:** v4.1.0 Tier 1 (T1.6) + Tier 2 (T2.2, T2.3)
**Issue:** empathetech/hacky-hours-docs#11 (piece 3)
**Arbitration mode:** decide

## Context

V4.0.0's `team update` mechanism requires the conductor to (a) manually nominate every behavior change as a pending file, and (b) walk the owner through accept/edit/reject/defer for each one. That's three manual steps per learning opportunity, with the conductor as the chokepoint.

Two follow-on problems:

1. **Cross-role propagation doesn't happen automatically.** Felix learned "match the specific anchor" on pomodoro; Maya didn't get the principle even though it applies to product framings more than to design. The update mechanism modifies one bio at a time with no propagation check.

2. **Real teams don't work this way.** When something gets learned, it just gets learned. Sometimes a senior engineer mentions it in passing and three others internalize it. Sometimes it shows up in the next code review as "since we got bitten by X, let's not do Y anymore." Learning is *continuous, agent-to-agent, and only occasionally crosses the founder's desk.*

## Roles involved

- **📊 Maya (Product)** — auto-promote needs a stakes rubric so we don't auto-land things that change product framing. Framing-level patterns must queue for owner review.
- **🏗️ Priya (Architect)** — end-of-verb self-debrief is the right trigger moment for agent-to-agent learning. After a verb completes, participating agents have shared context to reflect on; later moments lose that context.
- **🛡️ Alex (Security)** — auto-promoting bio updates is a self-modification surface. The harness's auto-mode classifier has already blocked one such edit this session. The framework needs to be explicit about what kinds of edits auto-land vs. queue, and the harness needs a way to distinguish "framework-initiated auto-promote" from "ad-hoc bio rewrite."
- **🔍 Emma (QA)** — every auto-promotion is a silent change. Without a visible record, the team drifts and the owner can't audit. `team update` confirmation footer needs to enumerate what auto-landed.

## Decision

### 1. The `stakes:` field in pending-file frontmatter

Every pending behavior-feedback file gains a `stakes:` field:

```yaml
---
captured_at: 2026-05-22T16:00:00Z
session_id: 2026-05-22-1600-abcd
project: my-project
verb: step-2-design
kind: behavior_feedback
target_section: how_i_work
agent: architect
stakes: low                       # NEW: low | high
status: pending
---
```

**Default `stakes: high` for safety.** The conductor (or in T2.3, the auto-debrief logic) explicitly tags `stakes: low` for craft-level patterns.

### 2. Stakes rubric

A new `references/capture-format.md` §"Stakes rubric" section defines the boundary:

**`stakes: low` (auto-promote on next `team update`)** — examples:

- *"Use absolute paths in shell commands."*
- *"Prefer `npm ci` over `npm install` in CI."*
- *"Format git commit messages with a body explaining why."*
- *"When the team has multiple agents review, render attribution per turn even at `team_chat: off`."*

Pattern: craft / convention / tooling preference that affects *how* an agent works, not *what* they prioritize.

**`stakes: high` (queue for owner review)** — examples:

- *"When the user names a specific anchor, verify every addition belongs to that anchor."* (framing)
- *"Don't conflate regulated-practice violation with standard informational disclaimer hygiene."* (judgment)
- *"For products whose core data is small + public, default to client-side engine + JSON snapshot."* (architectural default)
- *"Distinguish between owner-as-co-author and owner-as-reviewer roles."* (interaction model)

Pattern: principle that affects *what* an agent decides, recommends, or prioritizes. These shape future client work; the owner needs to see them before they land.

When in doubt: `high`. Auto-promote is the optimization; queue-for-review is the correct default.

### 3. `team update` flow rework

Step 1 (Collect pending changes) — read `stakes:` from each file, bucket into `auto` and `review`.

Step 2 (Present to conductor) — show only `review`-bucket entries. Auto-bucket entries are committed silently with a single footer summary.

Step 3 (Per-change review) — only for `review` entries. Adds new option **"propagate to peer"**: when accepting, the framework asks *"Which other agents should consider this principle?"* and writes parallel pending files for those agents with `propagated_from: <original-agent-id>` annotation.

Step 4 (Commit) — single git commit covers auto-promotes + accepted reviews. Auto-promoted entries are grouped first in the commit message.

Step 6 (Confirmation footer) — distinguishes:

```
Done.
  Auto-promoted: 3 (1 architect, 2 backend) — see commit abc1234
  Reviewed + accepted: 2 (product, security)
  Deferred: 1
  Rejected: 0
  Cross-role propagated: 1 (architect's principle also added to product's queue)
```

### 4. Cross-role propagation

When an accepted entry has `stakes: high` AND the original agent's prompt or feedback file is touched, the framework asks:

> *"Should any peer agents also adopt this principle? (Free-form list of agent IDs, or `none`.)"*

For each peer named, write a new pending file at `sessions/<id>/pending/<peer-id>.md` with:

```yaml
---
kind: behavior_feedback
target_section: how_i_work
agent: <peer-id>
stakes: high
propagated_from: <original-agent-id>
original_pending: <original-session-id>/pending/<original-agent-id>.md
status: pending
---

(content of the original Behavior change section, lightly rewritten to apply to peer's role)
```

Peer pending files surface in the next `team update` cycle for normal review. The owner can accept, reject, or edit.

This is the cross-role propagation mechanism Felix-to-Maya needed. It's a peer-ask, not an auto-apply — the framework proposes; the owner decides.

### 5. End-of-verb auto-debrief (T2.3)

When `features.auto_debrief: true`, every multi-role verb concludes (after Phase N — Stash) with a brief multi-agent self-debrief among participating agents. The structure:

```
🤖 Auto-debrief (2 of 4 agents weighed in):
  Architect — "Cost preflight was useful; would propose surfacing the
              estimate earlier (before role selection, not after)."
  Backend  — "No proposed changes from this verb."
  ...
```

Each "I would propose…" becomes a `stakes: low` pending entry (the conductor reviews the proposal, but stakes are pre-classified by the agent itself for fast review). The auto-debrief is also a `role_event: "debrief"` message in `messages.jsonl`.

`features.auto_debrief` defaults `false` in v4.1.x; flipped to `true` in v4.1.0 if signal is positive.

### 6. Safety: auto-promote requires explicit affordance

The harness auto-mode classifier can flag bio edits as self-modification. Mitigations:

- All auto-promote writes go through the `team update` verb (which has explicit harness permission per the recent settings.json grant).
- Auto-promote writes are batched into a single git commit on the team repo, never to live agent system prompts directly.
- The `team update` footer surfaces auto-promotes clearly; users can audit the team-repo git log to see what auto-landed.

## Consequences

**Positive:**

- Owner sees fewer routine accept/reject prompts. Friction drops.
- Cross-role propagation is now a built-in offer, not a manual remember-to-do-this-yourself task.
- Auto-debrief catches learning opportunities the conductor missed mid-flow.
- Stakes rubric makes the "what should auto-land" question debatable in a structured way.

**Negative / accepted:**

- Auto-promote is a self-modification surface. Mitigated by team-update batching + git auditability + opt-in via feature flag.
- Stakes classification is a judgment call. Some pending entries will be classified wrong. Acceptable because high-stakes-classified-as-low surfaces as a wrong principle in an agent's bio (visible, correctable); low-stakes-classified-as-high just costs an unnecessary owner review.
- Auto-debrief adds token cost at end of every verb. Mitigated by feature flag default-off + per-role budget cap.

## Alternatives considered

- **No stakes field — owner reviews everything.** Status quo. Rejected per ITERATION.md §C1.
- **Auto-promote everything.** Rejected: framing-level patterns affecting future client work need owner visibility.
- **Stakes inferred from content rather than declared.** Rejected: inference is fuzzy; explicit declaration is testable.
- **Cross-role propagation auto-applied.** Rejected: propagation is an editorial judgment call; the framework proposes, the owner decides.

## Related

- V4_DESIGN.md §4.26 — Automated agent-to-agent learning
- `tools/team-update.md` — receives the Step 1/2/3/4/6 rework
- `references/capture-format.md` — receives `stakes:` field + Stakes rubric section
- ADR: 2026-05-22-feature-flag-layer.md (`features.auto_promote_low_stakes`, `features.cross_role_propagation`, `features.auto_debrief`)
- #11 piece 3
- ITERATION.md §A1, §C1
