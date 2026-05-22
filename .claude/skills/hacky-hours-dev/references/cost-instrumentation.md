# Cost instrumentation — `cost-log.jsonl` schema

Token-accounting log for v4.1+. Defines the schema, the write contract, and the read pattern. Sister doc to `references/cost-preflight.md` (preflight is the proactive surface; this is the recording surface).

Design source: ADR `hacky-hours/02-design/decisions/2026-05-22-feature-flag-layer.md` §3. Locked decision: V4_DESIGN.md §4.23.

---

## What this enables

v4.0.x had no cost-tracking primitive. Without one, users couldn't audit their own usage, the framework couldn't publish per-verb cost benchmarks (R1), and graceful degradation (auto-downshift when `session_budget_hard` is approached) couldn't fire mid-verb because the framework had no idea where the session stood.

F2 introduces `~/.hacky-hours/sessions/<session-id>/cost-log.jsonl` — one append-only JSONL log per session, with per-verb / per-role / per-phase entries that build up over the session's lifetime.

This is **always-on infrastructure** (no feature flag). It logs whether you want it or not — the cost of recording one extra JSONL row per verb-phase is negligible compared to the verb itself, and the data is what unlocks every subsequent cost-aware feature.

---

## Schema

One JSON object per line, appended at the END of each instrumentable unit (verb, phase, role-turn). Schema:

```json
{
  "ts": "2026-05-22T18:30:00.123Z",
  "session_id": "2026-05-22-1830-abcd",
  "verb": "audit",
  "phase": "lane-a",
  "role": "security",
  "agent_id": "security",
  "input_tokens": 4521,
  "output_tokens": 1233,
  "cache_hits": 2840,
  "cache_creation": 0,
  "model": "claude-opus-4-7",
  "wall_ms": 12450,
  "verb_invocation_id": "audit-2026-05-22-abc1",
  "settings_snapshot": {
    "team_chat": "minimal",
    "profile_plan": "pro",
    "active_features": ["workroom_mode", "presentations"]
  }
}
```

### Field reference

| Field | Type | Required | Notes |
|---|---|---|---|
| `ts` | ISO 8601 with milliseconds + 'Z' | yes | Append time, not start time. Use UTC. |
| `session_id` | string | yes | Same as the session ID in `~/.hacky-hours/sessions/.current-session`. |
| `verb` | string | yes | The top-level verb (`audit`, `adopt`, `step-2`, etc.) |
| `phase` | string \| null | optional | Sub-phase of the verb (`lane-a`, `phase-1-capture`, `stash`, etc.). Null for verbs without phases. |
| `role` | string \| null | optional | The role this turn represents. Null when the entry is verb-level / framework-level. |
| `agent_id` | string \| null | optional | Folder-name of the agent (same as `role` for default team). Distinct field for future when role != agent_id (e.g., multiplexed agents). |
| `input_tokens` | integer | yes | Total input tokens for this unit. |
| `output_tokens` | integer | yes | Total output tokens for this unit. |
| `cache_hits` | integer | optional | Tokens served from prompt cache (Anthropic API). Set 0 when unknown. |
| `cache_creation` | integer | optional | Tokens used to create cache entries. Set 0 when unknown. |
| `model` | string | yes | Model ID used for this unit (`claude-opus-4-7`, `claude-haiku-4-5`, etc.). |
| `wall_ms` | integer | yes | Wall-clock duration in milliseconds. |
| `verb_invocation_id` | string | yes | Unique-per-invocation ID for joining multi-phase entries. Format: `<verb>-<date>-<4hex>`. |
| `settings_snapshot` | object | optional | Subset of settings.yml relevant to this entry. Helps explain cost variation across sessions. |

JSONL chosen for the same reasons as `messages.jsonl`: append-safe (no read-modify-write race), cheap to tail, programmatically consumable via `jq` / streaming readers.

---

## When entries are appended

Three levels of granularity, all written to the same `cost-log.jsonl`:

1. **Per-role-turn** (finest grain) — when a verb fans out to a role and that role produces output. One entry per (verb invocation, role, turn).
2. **Per-phase** (medium) — verbs with named phases (`audit` Lane A/B/C, `step-5` Phase 1–6) emit one summary entry per phase. `role: null`. `input_tokens` and `output_tokens` are the phase totals (sum of role-turn entries within the phase + framework overhead).
3. **Per-verb** (coarsest) — every verb emits one summary entry at end-of-verb. `phase: null`, `role: null`. Totals for the verb.

Consumers can choose granularity: roll up to verb-level for reports, drill down to role-level for cost-attribution analysis.

---

## Write contract

Verb files do NOT directly write to `cost-log.jsonl` themselves — they can't, because the verb-implementing assistant doesn't have introspective access to its own token usage. **The write happens at the Claude Code harness level**, with verb files cooperating by:

1. **Declaring instrumentable points.** Each multi-role verb's skill file includes a "Cost instrumentation" line in its preamble that names which units the verb expects to be logged (e.g., *"Emit per-phase + per-verb entries"*). This is the **canonical contract** the harness can read.
2. **Calling out the verb_invocation_id.** Each verb invocation generates an ID at start (`<verb>-<YYYY-MM-DD>-<4hex>`) and references it in any prompts where consistency matters. Phases inherit the parent verb's invocation ID.
3. **Providing settings snapshots.** When a verb's behavior depends on settings (workroom_mode, team_chat, etc.), it includes a `settings_snapshot` field in its log entries so future analysis can correlate cost with configuration.

The framework's contract is to define what SHOULD be logged. The harness's contract is to actually log it. Until the harness implements this (Claude Code platform work, outside this repo's scope), the JSONL file may be empty or partial. That's OK — the schema is forward-compatible, and the contract is what unlocks (a) cost-aware features in this framework, (b) the eventual harness instrumentation.

---

## Read pattern

For consumers (the framework's own preflight estimator, future analytics, user-self-audit):

```bash
# Total spend this session:
jq -s 'map(.input_tokens + .output_tokens) | add' \
  ~/.hacky-hours/sessions/<id>/cost-log.jsonl

# Per-verb breakdown:
jq -s 'group_by(.verb) | map({verb: .[0].verb, total: map(.input_tokens + .output_tokens) | add})' \
  cost-log.jsonl

# Per-role breakdown for a given verb invocation:
jq -s 'map(select(.verb_invocation_id == "audit-2026-05-22-abc1")) | group_by(.role)' \
  cost-log.jsonl
```

The framework's own consumers (preflight estimator pulling running averages from prior runs; graceful-degradation tripwire reading session cumulative cost) will run analogous queries.

---

## Privacy

`cost-log.jsonl` is local-only. Never sent anywhere. Lives at `~/.hacky-hours/sessions/<id>/cost-log.jsonl` alongside `messages.jsonl` and `pending/`.

The `settings_snapshot` field deliberately excludes any user-content fields (no profile.technical_background, no role_fluency); it only includes operational settings that affect cost shape.

---

## Heavy verbs that must emit instrumentation

These verbs are the priority for instrumentation coverage. Each verb's skill file includes a "Cost instrumentation" line in its preamble pointing at this reference:

- `tools/adopt.md`
- `reviews/audit.md`
- `tools/arbitrate.md` (multi-role; cost varies sharply by mode)
- `tools/team-reflect.md`
- `tools/team-backfill.md`
- `steps/01-ideate.md` through `steps/05-iterate.md` (multi-role steps)

Single-role verbs (`feedback`, `issue`, `meta`, `team show`, `team site`, `update 1`, `update 2`) emit verb-level entries only.

---

## What this verb completes

F2 (this PR) establishes the schema + contract. The harness instrumentation that actually populates `cost-log.jsonl` is platform-level work outside this repo. Until that lands:

- The schema is stable and forward-compatible.
- The contract documents what to log when instrumentation arrives.
- Future cost-aware features in this framework can read from `cost-log.jsonl` knowing the shape.
- R1 (cost benchmarks) will populate observed values into `references/cost-model.yml` to seed preflight estimates until live measurement is available.

Source: V4_DESIGN.md §4.23. ADR: `02-design/decisions/2026-05-22-feature-flag-layer.md` §3.
