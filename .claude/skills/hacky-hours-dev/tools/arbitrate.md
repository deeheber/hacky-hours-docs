# /hacky-hours arbitrate <mode> <topic> — resolve role disagreement

When roles disagree on a project, the conductor arbitrates. This verb gives the conductor three named patterns to do that, calibrated to how much depth they want and how much budget they're willing to spend.

## Three modes

- **`decide`** (cheapest) — framework summarizes positions concisely; conductor decides directly. No further agent dialogue.
- **`resolve`** (medium) — conductor states high-level concerns; framework asks each role to propose resolutions against those concerns; conductor picks.
- **`watch`** (richest) — two or more roles converse with each other; transcript visible to conductor; ends on convergence or conductor interrupt.

Default when a conflict surfaces during a verb: `decide`. Conductor explicitly escalates.

## Step 0 — Pre-flight

1. **Project is adopted:** read `AGENTS.md` for active team. If absent, project not adopted yet — print *"Arbitration assumes the team is engaged on this project. Run `/hacky-hours adopt` first."*
2. **Parse arguments:** `/hacky-hours arbitrate <mode> <topic>`
   - Mode required: `decide` | `resolve` | `watch`
   - Topic optional: free-text description. If absent, prompt: *"What's the disagreement about?"*

## Step 1 — Identify the involved roles

Read the project's `HANDOFFS.yml`, `STATE.md`, and most recent verb outputs for context about what was happening when the disagreement surfaced. If unclear, ask the conductor:

> *"Which roles are in disagreement? (e.g., 'security and frontend on CSP strictness')"*

Resolve role names to agent IDs via the active team's `tier.yml`.

## Step 2 — Mode-specific orchestration

### Mode `decide`

Spawn each involved role and ask for their position in compressed form:

```
Task prompt per role:
You are <Name> (<Role>). Your system prompt is your context.

Topic of arbitration: <topic>

Briefly (under 100 words):
1. What's your position?
2. Why? (the discipline-specific reasoning)
3. What's the cost if your position loses?

Be concise. The conductor is going to read all positions side-by-side.
```

After all roles respond:

Print:

```
=== Arbitration: <topic> ===

[Role 1] — <Name>: <position> · why: <reason> · cost if loses: <cost>
[Role 2] — <Name>: <position> · why: <reason> · cost if loses: <cost>
...

Conductor — your call?
  - Pick a role's position
  - Propose a hybrid (which two positions to blend)
  - Defer (don't decide now)
```

Wait for conductor's decision. Then write an ADR.

### Mode `resolve`

Two-step:

**Step A:** ask the conductor for high-level concerns to weight against:
> *"Before each role proposes a resolution, what high-level concerns should they be weighing against?*
> *(e.g., 'don't break user trust', 'we ship in 2 weeks', 'no new infrastructure dependencies')"*

**Step B:** for each role, prompt them with the topic + the conductor's concerns:

```
Task prompt per role:
You are <Name> (<Role>). Topic: <topic>.

The conductor's concerns (weight your proposal against these):
1. <concern 1>
2. <concern 2>
...

Propose a resolution that addresses the topic AND respects the conductor's concerns. Be concrete:
- What you'd do
- Why this serves the conductor's concerns
- What it costs (effort, time, opportunity)
- Confidence: low | medium | high
```

After all roles propose: present side-by-side, ask conductor to pick (or hybridize). Write ADR.

### Mode `watch`

The richest and most expensive. Two or more roles literally converse with each other while the conductor observes.

**Setup:**
- Pick a "first speaker" — usually the role that flagged the disagreement
- Pick a turn limit (default: 6 exchanges, so 3 back-and-forths per role)

**Loop (until convergence, turn limit, or conductor interrupt):**

For each turn:
1. Pass the current transcript to the next role's subagent
2. Their task prompt: *"You are <Name>. You're in a working conversation with <other roles>. The topic: <topic>. Here's the conversation so far: <transcript>. Respond — agree where you can, push back where you must, propose specific things. Under 200 words."*
3. Append their response to the transcript
4. Show to conductor; offer interrupt option

**Convergence detection:** if the most recent two turns from different roles propose substantively the same resolution, declare convergence.

**Conductor interrupt:** after any turn, conductor can:
- Continue (next role responds)
- Inject a question or constraint
- Force a decision now

**End:** write the full transcript to `hacky-hours/02-design/decisions/<date>-<topic>-watch.md` and write an ADR with the resolved decision (or document the unresolved-status if no convergence).

## Step 3 — ADR output

Every arbitration produces an ADR at `hacky-hours/02-design/decisions/<YYYY-MM-DD>-<topic-slug>.md`:

```markdown
# ADR: <topic>

**Date:** <date>
**Status:** Resolved | Unresolved
**Arbitration mode:** decide | resolve | watch

## Context
<what the disagreement was about; brief>

## Roles involved
- <Role 1> — <position summary>
- <Role 2> — <position summary>
- ...

## Decision
<what the conductor decided>

## Rationale
<why; reference the role positions that shaped it>

## Consequences
<what changes downstream; what we're now committed to>

## Alternatives considered (and not chosen)
- <Alternative 1> — rejected because <reason>
- <Alternative 2> — rejected because <reason>

<For watch mode, append:>
## Conversation transcript
<full multi-turn transcript>
```

## Step 4 — Update state

- Update `HANDOFFS.yml`: if there was a pending handoff that the disagreement blocked, mark it resolved.
- Update `NARRATIVE.md`: add a sentence noting the decision was made.

## Cost guidance

| Mode | Roughly tokens | When to use |
|------|----------------|-------------|
| `decide` | ~3-8K | Default. Fast, clear, conductor knows their preference and just needs the positions stated. |
| `resolve` | ~10-20K | When the conductor's concerns aren't obvious to the roles and they'd produce wrong proposals without context. |
| `watch` | ~20-50K | When the disagreement is genuinely complex and the conductor wants to see how disciplines reason against each other. Rare. |

Surface estimated cost before starting (esp. for `watch`):

> *"This arbitration in `watch` mode will likely use ~30K tokens. Your warn threshold is <warn>. Proceed?"*

## Notes for the assistant

- **Conductor always decides.** No mode auto-picks a winner. The framework's role is to surface positions clearly.
- **Don't force convergence in `watch`.** If roles genuinely disagree after the turn limit, document it as Unresolved and let the conductor decide.
- **ADRs are the durable output** — even a decide-mode arbitration that takes 90 seconds should produce an ADR. Otherwise the decision evaporates and the team will re-litigate it next month.
- **Roles should be calibrated to tier** in their positions. A Tier 3 security position may be a Tier 1 over-engineering — the roles should acknowledge that explicitly.
