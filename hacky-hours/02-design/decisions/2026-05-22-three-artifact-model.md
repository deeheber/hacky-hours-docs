# ADR: Three-artifact model — deep docs + presentations + status updates

**Date:** 2026-05-22
**Status:** Accepted
**Slice:** v4.1.0 Tier 1 (T1.3, T1.4) — schema; render lands with browser companion (T3)
**Issue:** empathetech/hacky-hours-docs#11 (piece 4)
**Arbitration mode:** decide

## Context

V4.0.0 produces one artifact tier: deep documents (`ARCHITECTURE-deep.md`, etc.). These are appropriate for agents reading them at build time. They're inappropriate for the owner trying to scan "what was decided this session" — they're walls of text that force the owner to read every section to know what's going on.

The owner's articulation (during reciprocator session, 2026-05-22): *"I expect that there's always something that is gonna be there in documentation that the agents are going to use so the same level of detail that we have been publishing... but also with regard to me as the human user that I'm getting presentations. So the answer is, it's both, but useful for different people at different points in time."*

Two new artifact types are needed:

1. **Presentations** — synthesis for the owner at review checkpoints. Slide-shaped, decision-and-tradeoff focused.
2. **Status updates** — lightweight, ongoing, standup-style "here's what I'm working on" messages from agents.

Both layer *on top of* the existing deep docs, not in place of them.

## Roles involved

- **📊 Maya (Product)** — presentations need to expose disagreements explicitly. A presentation that says only "we decided X" without showing what was contested is worse than no presentation.
- **🎨 Felix (Design)** — slide-shape is a discipline. One screen, no scrolling, decision per row. ASCII / Mermaid renders fine; SSG render in browser companion is V1+.
- **🏗️ Priya (Architect)** — status updates are different from log entries. A log entry is "I did X"; a status update is "I'm doing X." They're forward-looking; they live in `sessions/<id>/messages.jsonl` like workroom turns.
- **🔍 Emma (QA)** — every artifact type needs a schema that's testable. Without schemas, the framework drifts.

## Decision

### 1. The three layers, audiences, locations

| Artifact | Audience | Location | Lifetime |
|---|---|---|---|
| **Deep docs** (existing) | Agents at build time; future contributors onboarding | `02-design/*-deep.md` | Project lifetime |
| **Presentations** (new) | Owner at review checkpoints | `02-design/*-presentation.md` (alongside deep) | Per-checkpoint, regenerated freely |
| **Status updates** (new) | Owner day-to-day; team for coordination | `sessions/<session-id>/messages.jsonl` (with `role_event: "status"` field) | Session-scoped, archived with session |

### 2. Presentation schema

Markdown with frontmatter:

```markdown
---
kind: presentation
verb: design                  # or audit, iterate, etc.
generated_at: 2026-05-22T15:01:00Z
generated_by: hacky-hours v4.1.0
session_id: 2026-05-22-1500-abcd
deep_source: ARCHITECTURE-deep.md
---

# What we decided

<one paragraph; outcome>

## Per-discipline summary

### Product
<one short paragraph>

### Architecture
<one short paragraph>

(... per participating role)

## Disagreements

- **<topic>:** Architect proposed X; Product preferred Y; landed on X because <reason>.
- (per significant disagreement)

## Open questions for you

1. <explicit question only the owner can answer>
2. ...

## What's next

- <linked design doc(s) that contain the full detail>
- <BACKLOG items proposed>
- <ADRs drafted>
```

**Discipline: one screen.** Mermaid renders welcome but should not push the presentation past ~50 lines. If a presentation needs more than one screen, the team isn't synthesizing — they're transcribing.

**Discipline: discussions visible.** The "Disagreements" section is mandatory even if empty (state "No significant disagreements" — the absence is itself signal). The owner needs to see what was contested to calibrate their review.

### 3. Status update schema

A status update is one message in `messages.jsonl` with `role_event: "status"`:

```json
{
  "turn": null,
  "ts": "2026-05-22T15:20:00Z",
  "role": "architect",
  "agent_id": "architect",
  "role_event": "status",
  "content": "Started drafting V4_DESIGN §4.24. Will produce a first cut in ~10 minutes. No questions for the owner yet.",
  "channel": "iterate",
  "in_reply_to": null
}
```

Distinct from workroom turns (which have a `turn` index and contribute to the conversation). Status updates are out-of-band — they don't drive the dialogue, they narrate it.

**Status updates fire when:**

- A long-running role activity begins or ends.
- A role hits a blocker requiring owner input (escalation case).
- The team transitions phases (e.g., Phase 2 → Phase 3 of iterate).

**Agents decide when to fire status updates** — the conductor doesn't prompt for them. The heuristic is "if the owner were watching Slack, would this be the kind of message they'd appreciate?"

### 4. Render destinations

| Artifact | Render destination |
|---|---|
| Deep docs | File on disk; rendered by the browser companion's "project workspace" surface (T3.1) |
| Presentations | File on disk + dedicated "presentations" tab in browser companion + terminal `cat` (always readable as Markdown) |
| Status updates | Terminal output (when `team_chat: minimal|full`) + Slack-style chat surface (T3.5) in browser companion |

### 5. Discipline: presentation is *never* the source of truth

If the presentation and deep doc disagree, the deep doc wins. The presentation is regenerated from the deep doc; the deep doc is amended by hand or by verb. This matches the existing `deep` / `summary` two-tier pattern in the design template (`templates/design/README.md`) — presentations are the "summary" promotion to a first-class artifact.

When the owner reviews a presentation and asks for changes, the changes land in the deep doc (or BACKLOG, or a new ADR), and the presentation is regenerated. The owner never edits the presentation directly.

### 6. Discipline: status updates are never load-bearing

A status update is informational, not authoritative. If the owner needs to make a decision, the team produces a presentation (the formal review surface) or surfaces a question via `role_event: "escalation"`. Status updates are background hum.

## Consequences

**Positive:**

- Owner can scan in 30 seconds what previously required 10 minutes of doc-reading.
- Deep docs stay as deep as they need to be — they're not constrained by "the owner has to read this."
- Disagreements are visible by structure, not buried in prose.
- Status updates are the natural surface for the browser companion's chat view.

**Negative / accepted:**

- Generating a presentation adds a step at every checkpoint. Mitigation: it's a synthesis pass over content the team already produced; agents don't redo work.
- Status updates can become noise if agents over-fire. Mitigation: heuristic in agent system prompts ("would the owner appreciate this?") + ability for owner to set `features.status_updates: false` and silence them.
- Presentations could drift from deep docs if regeneration is lazy. Mitigation: same as existing summary/deep pattern — regeneration is a verb output (Step 5 amend), not a manual exercise.

## Alternatives considered

- **Two artifact tiers (deep + presentations only).** Rejected: the day-to-day owner experience needs lighter-weight updates than presentations. Status updates fill the gap.
- **Presentations replace deep docs.** Rejected per ITERATION.md owner directive ("deep docs stay for agents; presentations are layered on top").
- **Status updates as separate files** (`sessions/<id>/status-updates/`). Rejected: they belong in the same conversation log as workroom turns. Same file, different `role_event`.

## Related

- V4_DESIGN.md §4.25 — Three-artifact model
- V4_DESIGN.md §4.27 — Status-update artifact + agent-initiated escalation (sub-section)
- ADR: 2026-05-22-workroom-mechanic.md (digest format described here lives in workroom output)
- ADR: 2026-05-22-browser-companion.md (render destinations)
- `templates/design/README.md` — existing deep/summary pattern this generalizes from
- #11 piece 4
- ITERATION.md §A1, §A3.1
