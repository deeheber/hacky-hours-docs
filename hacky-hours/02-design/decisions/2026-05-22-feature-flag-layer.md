# ADR: Feature-flag layer in settings.yml + plan-aware defaults

**Date:** 2026-05-22
**Status:** Accepted
**Slice:** v4.1.0 Foundation (Tier 0)
**Issue:** empathetech/hacky-hours-docs#10
**Arbitration mode:** decide (single-conductor, single-maintainer project)

## Context

Hacky Hours v4.0.0 shipped on Claude Max and was never benchmarked on Pro. The framework's stated "this is for everyone" intent (SKILL.md global values) conflicts with the actual usage profile — multi-role fan-out, Phase N — Stash, audit Lane B subagents, and `team reflect --all` all assume token headroom that Pro doesn't have.

v4.1 work compounds this risk: the workroom mechanic (#11), automated agent-to-agent debrief (#11), and the browser companion (#8) all add new mechanisms that *increase* fan-out. Without a discipline that lets users disable cost-heavy machinery, v4.1 makes the framework less accessible — the opposite of #11's intent (reduce owner cognitive load, not shift it to wallet load).

Two interlocked needs:

1. **Per-feature toggles** so users can disable specific cost-heavy mechanisms (e.g., a Pro user wants the orchestra but not full workroom transcripts).
2. **Plan-aware defaults** so Pro / Max-5x / Max-20x users get sensible starting configurations without hand-tuning the toggle list.

## Roles involved

- **🚀 Jordan (Ops)** — argued that feature flags are the right shape even outside cost concerns. They let v4.1 work land trunk-based on `main` (instead of long-lived feature branches) and let users opt into bleeding-edge features ahead of release.
- **🛡️ Alex (Security)** — flagged that flags can become attack-surface if misconfigured to grant elevated access. For this framework, flags only enable behaviors (not permissions), so risk is bounded to "verbosity that costs money," not "data exposure."
- **🏗️ Priya (Architect)** — pushed back on hierarchical-vs-flat schema debate: hierarchical is more flexible but harder to teach. Concluded flat with documented grouping in comments.
- **📈 Yuki (Data)** — every feature flag's "current value" should be observable in CI / test output, not just at runtime. Drives a `--print-features` mode.
- **🔍 Emma (QA)** — every feature with a flag needs a no-flag-set fallback path, tested against. Without this, "what happens with `features.X` absent" becomes folklore.

## Decision

### 1. Flat `features:` block in `~/.hacky-hours/settings.yml`

```yaml
features:
  # Day-to-day workflow
  discovery_phase: false              # v4.1 Tier 1 — interrogate framing in Step 1
  skeptic_mode: false                 # v4.1 Tier 1 — --skeptic flag on any role
  status_updates: false               # v4.1 Tier 1 — agent-initiated escalation
  presentations: false                # v4.1 Tier 1 — digest artifact alongside deep docs

  # Team learning
  auto_promote_low_stakes: false      # v4.1 Tier 2 — auto-promote `stakes: low` pending entries
  cross_role_propagation: false       # v4.1 Tier 1 — peer-ask on team update accepts
  auto_debrief: false                 # v4.1 Tier 2 — end-of-verb agent-to-agent self-debrief

  # Workroom mechanic
  workroom_mode: false                # v4.1 Tier 2 — multi-turn agent dialogue persisted

  # Browser companion (#8)
  forms_writeback: false              # v4.1 Tier 3 — schema-aware fillable forms
  backlog_writeback: false            # v4.1 Tier 3 — kanban drag-to-reorder
  session_monitor: false              # v4.1 Tier 3 — tail pending/ + history.md
```

**Flat shape, grouped via YAML comments.** Hierarchical would let us say `features.workroom.transcripts: true` but every level adds cognitive overhead and the framework's audience includes non-engineers. Flat is teachable.

**Default-off in v4.1.x patches.** Each Tier 1/2/3 piece ships disabled-by-default. v4.1.0 release flips confirmed-stable defaults to `true` in the settings template; existing user settings.yml is not modified (additive).

### 2. `profile.plan` schema + plan-aware default selection

```yaml
profile:
  technical_background: engineer
  role_fluency: { ... }
  plan: pro | max5x | max20x | unspecified    # NEW
```

When unset, `tools/v4-first-run.md` asks once and persists.

Plan-aware behavior:

- **`plan: pro`** — leaner defaults: `team_chat: minimal`, `role_models.licensing: claude-haiku-4-5`, `role_models.accessibility: claude-haiku-4-5`. Heavy verbs (`audit`, `team reflect --all`, `team backfill`) print a preflight cost estimate before fanning out.
- **`plan: max5x` / `plan: max20x`** — current v4.0.0 defaults (full fan-out, default model).
- **`plan: unspecified`** — Pro-flavored defaults (safer fallback than assuming Max).

Plan affects defaults, not feature availability. A Pro user can enable any flag; the framework just warns on cost-heavy ones.

### 3. Cost preflight + graceful degradation

Heavy verbs (`adopt`, `audit`, `team reflect --all`, `team backfill`, future `workroom` runs) print:

```
This verb will use approximately N tokens (range: M–P) at your current
settings. That's ~X% of your daily Claude usage at the `pro` plan tier.

  Proceed                    [continues normally]
  Downshift                  [disables high-cost features for this run only]
  Cancel
```

Estimates derive from a lookup table at `references/cost-model.yml` (populated from #10 deliverable 3 — benchmarks). When estimates are absent (new verb, no benchmark yet), the preflight surfaces *"cost data not yet published"* and proceeds without an estimate.

**Graceful degradation:** when session-cumulative cost approaches `session_budget_hard` from settings.yml, the framework auto-downshifts (narrate-only mode, skip non-critical roles, smaller models) rather than failing mid-verb. Logged transparently.

### 4. `--print-features` mode

`/hacky-hours team` (no subcommand) gains a footer:

```
Active features: discovery_phase, status_updates, workroom_mode  (3 of 11)
                 (toggle: edit ~/.hacky-hours/settings.yml, restart Claude Code)
```

So users can see what's active without grepping their config.

### 5. Loader machinery in SKILL.md preamble

Every verb that branches on a feature flag adds, at the top:

```
**Feature-flag check.** Read `~/.hacky-hours/settings.yml`. If `features.<flag_name>` is `false` or absent, skip to <fallback section>.
```

Fallback path is mandatory per Emma's requirement. Default fallback for a missing flag is "v4.0.x behavior" — i.e., the framework continues working without the new mechanism, just without it.

## Consequences

**Positive:**

- v4.1 work lands trunk-based on `main`. No long-lived feature branch with drift / conflict pain.
- v4.0.x patches can ship safely (hotfix queue: HF1, HF2) in parallel to v4.1 work.
- Pro feasibility becomes a per-feature question, not an all-or-nothing one.
- Users can opt into bleeding-edge features ahead of v4.1.0 if they want.

**Negative / accepted trade-offs:**

- 11 flags is a lot to teach. Mitigated by: per-feature inline comments in `settings.yml`, the `--print-features` footer, and v4.1.0's "flip stable defaults to true" so most users never read the file.
- Plan-aware defaults are a heuristic, not a measurement. Mitigated by: `references/cost-model.yml` getting populated with real benchmark data over the v4.1 cycle.
- Adds preamble overhead to every flag-aware verb. Mitigated by: each preamble is one line ("read settings, check flag, fallback if absent"). The framework already does similar for `team_chat` and `profile`.

## Alternatives considered

- **Hierarchical YAML schema** (`features.workroom.enabled: true`): rejected as harder to teach. Flat with comments wins on teachability.
- **Env-var-based flags** (`HACKY_HOURS_FEATURES_WORKROOM_MODE=true`): rejected as fragile across Claude Code sessions and shells.
- **Per-verb config** (each verb file declares its flags): rejected as fragments authority — `settings.yml` is the existing single source of truth for user-level preferences.
- **Long-lived `feat/v4.1` branch**: rejected per ITERATION.md §B4 — drift / conflict pain disproportionate to benefit; feature flags achieve the same "ship together" outcome without the branch.

## Related

- V4_DESIGN.md §4.23 — Feature-flag layer (the locked-decision section that summarizes this ADR)
- #10 — Audit token cost per verb across Claude plans + ship plan-aware defaults
- `references/cost-model.yml` (to be created in Tier 4 / R1 of v4.1.0)
- ITERATION.md (this iteration cycle, 2026-05-22) §A2, §B2, §B4
