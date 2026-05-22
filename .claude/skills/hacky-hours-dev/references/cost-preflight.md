# Cost preflight — pattern for heavy verbs

Read this when authoring a heavy verb (one that fans out to multiple roles, runs multi-phase audits, or processes the project's full history). The preflight is the framework's promise to Pro-plan users: *"we'll tell you before we burn a chunk of your daily token budget."*

Design source: ADR `hacky-hours/02-design/decisions/2026-05-22-feature-flag-layer.md` §3. Locked decision: V4_DESIGN.md §4.23.

---

## What this enables

The framework's "this is for everyone" intent (see SKILL.md global values) extends to all Claude plan tiers. Pro-plan users have substantially lower token budgets than Max-5x or Max-20x. Without preflight, a single `audit` or `team backfill` run can chew through a significant fraction of a day's allowance with no warning.

Preflight surfaces the cost *before* the fan-out begins, gives the conductor three named options (proceed / downshift / cancel), and respects the conductor's choice for the duration of the verb.

This pattern is **always-on** (not feature-flagged). It runs on every heavy verb, regardless of `features:` settings.

---

## Heavy verbs (the four that require preflight)

| Verb | Why heavy | Typical token range (input + output) |
|---|---|---|
| `adopt` | Reads codebase + writes 5+ docs across multiple disciplines | 30K – 80K |
| `audit` | Three parallel lanes; Lane A engages 5+ roles | 80K – 200K |
| `team reflect --all` | Walks every agent's history + feedback + profile | 40K – 120K |
| `team backfill` | Reads project history (CHANGELOG / git log) + per-agent classification | 60K – 150K |

Ranges are observation-based estimates until R1 (cost benchmarks, V4_DESIGN §10.R1) publishes real numbers.

Other verbs (`step 1` through `step 5`, `arbitrate`, `team update`, `meta`) are lower-cost and **do not** trigger preflight by default. They may still surface a cost estimate informally when `team_chat: full` and the user is on `plan: pro`.

---

## The preflight pattern

Each heavy verb adds a **Cost preflight** section near the top of its skill file, after team-preflight and before the verb's main fan-out:

```markdown
## Step 0.X — Cost preflight (v4.1+)

This verb is cost-heavy. Before fanning out, read `~/.hacky-hours/settings.yml` for `profile.plan`. Surface to the conductor:

> *"This verb typically uses ~N tokens at your current settings (roughly X% of your daily limit at the `<plan>` plan tier).*
> *  - **Proceed** — continue normally*
> *  - **Downshift** — reduced fan-out: skip non-critical roles, smaller models for low-output roles, narrate-only mode*
> *  - **Cancel*"*

Apply the conductor's choice for the duration of this verb invocation.
```

The literal `~N tokens` is the verb's typical range from the table above. The `X%` is computed against a rough plan-tier daily limit (Pro ≈ 100K daily; Max-5x ≈ 5M; Max-20x ≈ 20M — these are approximations until R1 publishes real numbers).

---

## When to fire

Three rules in order:

1. **Always fire when `profile.plan: pro` or `unspecified`.** Pro budgets are tight; safer default is to ask.
2. **Skip when `profile.plan: max5x` or `max20x`** UNLESS the verb's estimate exceeds 50K input tokens (the rough threshold for "this is a noticeable bite even on Max").
3. **Always fire when session-cumulative cost already exceeds `session_budget_warn`** in settings.yml. Even on Max, late-session verbs deserve a heads-up.

The third rule depends on F2 (token instrumentation) being wired. Until F2 lands, the third rule is documented but not enforced. F1's design is plan-aware-defaults-first; F2 will tighten the loop.

---

## What "Downshift" means per verb

Each heavy verb defines its own downshift profile in its skill file. Conventions:

- **`adopt` downshift:** skip the optional involvement-assessment artifact; use Haiku for cheap roles (licensing, a11y); narrate-only voice mode.
- **`audit` downshift:** run Lane A only (skip Lane B doc-stranger + Lane C cross-ref); reduce Lane A's role set to the top 3 (security, architect, qa); narrate-only.
- **`team reflect --all` downshift:** process agents one at a time (vs. parallel); skip the prose-update generation step (offer to re-run later for individual agents).
- **`team backfill` downshift:** classify by file-path heuristic only (skip the keyword-classification pass); narrate-only when surfacing per-agent batches.

Each downshift preserves the verb's core output — just less polish, less coverage, less voice.

---

## Graceful degradation (paired discipline)

The preflight is the proactive case ("ask before spending"). Graceful degradation is the reactive case ("auto-downshift when about to overrun"). They share a goal but differ in trigger:

- **Preflight:** fires at verb entry, gives the conductor a choice.
- **Graceful degradation:** fires mid-verb when `session_budget_hard` is approached. Auto-downshifts without asking; logs the downshift to the verb's output ("Switched to narrate-only mode at 75% of session budget").

Graceful degradation depends on F2 (token instrumentation). Until F2 lands, the framework documents the graceful-degradation intent but cannot enforce mid-verb. F2 wires the runtime measurement.

---

## What this verb completes

T1.5 (this PR) wires preflight into the four heavy verbs and seeds plan-aware role-model defaults (the latter mostly done in F1's first-run script — T1.5 ensures existing settings.yml files without `profile.plan` are handled gracefully).

When the implementing engineer for a future heavy verb adds it, they:

1. Read this file.
2. Add the canonical `Cost preflight` section to the verb's skill file.
3. Define the verb's downshift profile inline.
4. Add the verb to the heavy-verb table above with its observed token range.

Source: V4_DESIGN.md §4.23. ADR: `02-design/decisions/2026-05-22-feature-flag-layer.md` §3.
