# ADR: Workroom mechanic — team-as-workroom, owner-as-reviewer

**Date:** 2026-05-22
**Status:** Accepted
**Slice:** v4.1.0 Tier 2 (T2.1)
**Issue:** empathetech/hacky-hours-docs#11 (piece 1)
**Arbitration mode:** decide (single-conductor + structural critique)

## Context

V4.0.0's interaction model routes everything through the owner: every step asks for sign-off; agents speak only when invoked; documents are walls of text. Two recent dogfooding projects (`video-game-pomodoro`, `reciprocator`) had framing-level misses where the team faithfully executed what the founder said but missed what they intended. Both required the founder to catch — the team had no offstage space to interrogate the framing among themselves.

The diagnostic: the team is structurally a *contractor team* (agents speak when invoked, no native moment to volunteer "we think we're solving the wrong problem") rather than a *startup team* (productively adversarial, runs Discovery before architecture, sketches before specifying).

The owner's articulation of the desired experience: *"a good orchestra conductor doesn't micromanage. They lead, set vision, point the orchestra, but don't tell the violinist how to hold the bow. The musicians know their instruments better than the conductor does."*

## Roles involved

- **📊 Maya (Product)** — owner-as-reviewer needs a different default question shape than owner-as-co-author. Verbs currently ask "what do you want to do next?" repeatedly; workroom verbs need to ask "is this presentation accurate / what do you want changed?"
- **🏗️ Priya (Architect)** — the workroom is structurally a multi-turn agent-to-agent conversation persisted to disk. Without persistence, the workroom has no audit trail and the owner can't trust the team to have actually done the work.
- **🎨 Felix (Design)** — the digest/presentation that the owner reviews needs to be one screen, decision-and-tradeoff focused, with explicit "things we disagreed about" surfaced. Walls of doc are the failure mode.
- **🛡️ Alex (Security)** — agent-to-agent conversation persisted to disk is a new persistence surface. No PII at risk in normal use, but the framework should not silently exfiltrate session content beyond the local filesystem.
- **🔍 Emma (QA)** — workroom verbs are testable as snapshot fixtures: given inputs + role roster + chat-mode, the produced messages.jsonl should be deterministic (modulo LLM nondeterminism, which we accept).

## Decision

### 1. The shape: multi-turn agent dialogue, persisted

A workroom-flagged verb (Step 2, Step 5, audit) runs a structured multi-turn conversation **among the agents themselves**, not staged for the owner. The conductor coordinates turn-taking but doesn't translate every line into owner-facing prose.

Per-turn structure:

- Each turn is one role speaking, one to several paragraphs.
- Turns can be **proposals** ("I think we should …"), **pushback** ("I disagree because …"), or **convergence** ("OK, I'll defer to …").
- The conductor sequences turns; agents can request follow-ups ("Architect, can you weigh in on this?") which the conductor honors if budget allows.
- Conversation ends when convergence is reached OR `workroom_max_turns` (settings.yml, default 24) is hit.

### 2. Persistence: `sessions/<id>/messages.jsonl`

Every turn is appended as a JSON object to `~/.hacky-hours/sessions/<session-id>/messages.jsonl`:

```json
{"turn": 1, "ts": "2026-05-22T14:15:01Z", "role": "product", "agent_id": "product", "content": "...", "channel": "iterate", "in_reply_to": null}
{"turn": 2, "ts": "2026-05-22T14:15:18Z", "role": "architect", "agent_id": "architect", "content": "...", "channel": "iterate", "in_reply_to": 1}
```

JSONL chosen for line-by-line append (no read-modify-write race; cheap to tail). `channel` field allows multiple workroom conversations within one session (e.g., audit Lane A + Lane B run as separate channels).

This file is **the source of truth for the Slack-style chat surface** (browser companion §4.29 / T3.5). One write surface, two render destinations (terminal team-chat + browser chat-view).

### 3. The owner's view: digest + open questions, not transcript

At the end of a workroom run, the conductor produces a **digest** (the new presentation artifact, §4.25):

- **Outcome:** one paragraph — what the team decided.
- **Per-discipline summary:** one short paragraph per participating role.
- **Disagreements:** explicit "Architect proposed X; Product preferred Y; landed on X because…" notes.
- **Open questions for the owner:** explicit list — questions the team could not resolve without owner input.
- **Linked artifacts:** any docs written, ADRs drafted, BACKLOG items proposed.

The owner reads the digest. The transcript (`messages.jsonl`) is preserved on disk and renderable via the chat surface; the owner consults it when curious, not by default.

### 4. Verb-by-verb workroom-mode adoption

Not all verbs become workrooms in v4.1.0. Selection:

- **Step 2 (design)** — yes, workroom is the natural fit. Authoring multiple design docs is intrinsically multi-role.
- **Step 5 (iterate)** — yes, synthesis + amendment is naturally multi-role.
- **audit** — partial — Lane A already fans out across roles; formalize as a workroom but keep Lane B/C as currently shaped (framework-internal).
- **arbitrate** — already multi-role by definition; workroom mode is the V1+ shape; v4.1.0 keeps existing format.
- **Step 1 (ideate), Step 3 (roadmap), Step 4 (build)** — usually 1-2 roles; not workroom-shaped by default. May opt in via `features.workroom_mode` + explicit verb flag.
- **adopt** — currently steady-state; workroom not in v4.1.0 scope.

### 5. Owner interruption + redirect

The workroom isn't a black box. The owner can interrupt at any point — Cmd-C in terminal, or a typed message. The conductor surfaces the interruption to the team as an **owner note**: a special role-less message in the transcript that subsequent turns can reference. The most common interruption is *"actually I want it to be an explorer, not a planner"* — a framing redirect. The framework re-routes by inserting that note as turn N+1 and continuing.

A `/hacky-hours redirect "<note>"` slash command formalizes this for non-terminal workflows (e.g., editor extension).

### 6. Cost discipline

Workroom mode is the single biggest token-cost addition in v4.1.0. Mitigations:

- Gated behind `features.workroom_mode: false` by default.
- `workroom_max_turns` cap (default 24) prevents runaway.
- `workroom_role_budget` per-role token cap (default 2K per role per workroom) prevents one verbose agent from dominating.
- Cost preflight (from feature-flag-layer ADR §3) fires for workroom verbs.

## Consequences

**Positive:**

- Team can disagree productively. No more silent compliance with founder framings the team would have caught if given offstage space.
- Owner reviews instead of co-authors. Matches the orchestra-conductor metaphor.
- Transcripts on disk are auditable; "show your work" satisfied.
- One persistence surface (`messages.jsonl`) feeds both terminal team-chat and browser chat-view — no duplication.

**Negative / accepted:**

- Token cost goes up substantially when workroom_mode is on. Acceptable because (a) feature-flagged off by default, (b) bounded by max-turns and per-role budgets, (c) cost preflight surfaces the estimate before commit.
- Owner sees less per-turn. If a workroom converges on a wrong framing and the digest doesn't expose it, the owner won't catch it until later. Mitigated by the digest's mandatory "Disagreements" section + the skeptic-mode flag from §4.31.
- Workroom transcripts are non-deterministic. Snapshot tests must tolerate LLM variation — only structural assertions (turn count, role attribution, channel routing, schema validity).

## Alternatives considered

- **Synchronous conductor-led dialogue (current v4.0.0 behavior).** Rejected: it's the status quo we're explicitly fixing.
- **Single agent producing a fake transcript ("Product says…, then Architect replies…").** Rejected: that's roleplay, not actual disagreement. The framework's value is real fan-out across roles with real divergent perspectives.
- **Persist as Markdown, not JSONL.** Rejected: JSONL is append-safe; Markdown read-modify-write is racy and harder to consume programmatically (browser companion needs structured records).
- **Workroom by default for every verb.** Rejected: most verbs are single-role; the workroom is overkill and expensive there.

## Related

- V4_DESIGN.md §4.24 — Workroom mechanic
- V4_DESIGN.md §4.25 — Three-artifact model (digest comes from here)
- V4_DESIGN.md §4.28 — Browser companion (chat surface renders `messages.jsonl`)
- ADR: 2026-05-22-feature-flag-layer.md (`features.workroom_mode`)
- ADR: 2026-05-22-three-artifact-model.md (digest format)
- #11 piece 1
- ITERATION.md §A1
