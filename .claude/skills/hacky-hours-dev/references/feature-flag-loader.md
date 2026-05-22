# Feature-flag loader — canonical pattern

Read this before authoring any verb whose behavior is gated by a feature flag from `~/.hacky-hours/settings.yml`'s `features:` block.

Design source: ADR `hacky-hours/02-design/decisions/2026-05-22-feature-flag-layer.md`. Locked decision: V4_DESIGN.md §4.23.

---

## What this enables

Feature flags let users disable individual cost-heavy or experimental mechanisms (workroom mode, auto-debrief, status updates, presentations, browser-companion write-back surfaces, etc.). Each v4.1 mechanism that *adds new work to a verb* should be flag-gated:

- Disabled-by-default in v4.1.x patches (so the patch ships without changing default behavior).
- Confirmed-stable flags flip to default-on at v4.1.0 release.

Users can also override per-feature at any time by editing `~/.hacky-hours/settings.yml`.

---

## The pattern

Every flag-gated verb (or branch within a verb) does these three things at the top of the flag-aware section:

1. **Read the flag value** from `~/.hacky-hours/settings.yml`.
2. **Branch on it.** If `true`, run the new (v4.1) behavior. If `false` or absent, fall back to v4.0.x behavior.
3. **Never crash on missing.** Absence of a flag is identical to `false` — no flag in settings.yml ≡ flag is off.

The canonical text to add to a verb file:

```markdown
**Feature-flag check (`<flag-name>`).** Read `~/.hacky-hours/settings.yml`. If `features.<flag-name>` is `true`, run the [v4.1 behavior — link or describe]. If `false` or absent (v4.0.x fallback), skip to [the existing flow / section].
```

For verbs with multiple flag-aware branches, repeat per branch.

---

## Reading from settings.yml

When the verb's preamble (or a phase inside it) needs to consult a flag, run a small Bash check:

```bash
# Returns "true" / "false" / "" (absent).
FLAG=$(awk '/^features:/{f=1; next} f && /^[^ ]/{f=0} f && /^[ ]+<flag-name>:/{print $2}' ~/.hacky-hours/settings.yml | tr -d ' ')
```

Or in TypeScript-flavored pseudocode for clarity:

```ts
const settings = parseYaml(readFile('~/.hacky-hours/settings.yml'));
const enabled = settings.features?.[FLAG_NAME] === true;
```

Honest read in skill-file terms: each verb that needs a flag check does it via `Bash` or by reading the file with `Read`. There's no shared loader binary — it's a doc pattern. The consistency is in *what the verbs do*, not in centralized code.

---

## Fallback discipline

**Every flag must have a tested fallback path.** When `features.<flag-name>` is `false` or absent, the verb still works — just without the new mechanism. Three implications:

1. **Don't make a v4.1 feature the only path through a verb.** The verb has to keep working at v4.0.x behavior when the flag is off.
2. **Don't predicate other verbs on a flag being on.** If verb A requires the output of an optional verb B that's flag-gated, A breaks when B's flag is off. Either A also gates on B's flag, or B's output is always produced and the flag just affects whether the *user-facing* part of B runs.
3. **CI / tests should exercise both paths.** When v4.1's test infrastructure lands (Tier 4), this is mechanical; until then, manual smoke before merging each Tier 1/2/3 PR.

---

## The flag list (v4.1.x)

Maintained canonically in `tools/v4-first-run.md` Step 4 (the seeded settings.yml template). The current flags:

| Flag | Tier | Defaults to (in v4.1.x → v4.1.0) | Gates | ADR |
|---|---|---|---|---|
| `discovery_phase` | T1.1 | false → true | Discovery phase in Step 1 + lo-fi homepage gate | discovery-phase |
| `skeptic_mode` | T1.2 | false → true | `--skeptic` flag on any role | discovery-phase |
| `status_updates` | T1.3 | false → true | Status update artifact + agent-initiated escalation | three-artifact-model |
| `presentations` | T1.4 | false → true | Presentation artifact alongside deep docs | three-artifact-model |
| `cross_role_propagation` | T1.6 | false → true | `team update` Step 3 "propagate to peer" option | automated-team-learning |
| `workroom_mode` | T2.1 | false → true | Multi-turn agent dialogue persisted to messages.jsonl | workroom-mechanic |
| `auto_promote_low_stakes` | T2.2 | false → true | `team update` Step 1 auto-bucketing by `stakes` | automated-team-learning |
| `auto_debrief` | T2.3 | false → true | End-of-verb agent-to-agent self-debrief | automated-team-learning |
| `forms_writeback` | T3.7 | false → true | Browser-companion fillable-forms write-back via `pending-input.json` | browser-companion |
| `backlog_writeback` | T3.8 | false → true | Browser-companion backlog kanban drag-to-reorder | browser-companion |
| `session_monitor` | T3.9 | false → true | Browser-companion session-monitor surface | browser-companion |

This table is informational; the canonical schema lives in `tools/v4-first-run.md` Step 4.

---

## Plan-aware defaults (related but distinct)

`profile.plan` (also in settings.yml) shapes which *defaults* the framework starts with, not which flags exist:

- `plan: pro` — leaner defaults: `team_chat: minimal`, Haiku for `licensing` + `accessibility` per-role overrides, preflight cost estimate on heavy verbs.
- `plan: max5x | max20x` — v4.0.0 defaults (full fan-out, default model).
- `plan: unspecified` — Pro-flavored defaults (safer fallback).

Plan-aware defaults are wired in T1.5 (`tools/v4-first-run.md` Step 5 asks for the plan; `role_models` and `team_chat` are seeded based on the answer).

---

## What this verb completes

Without this loader pattern, every v4.1 feature would re-derive how to read settings.yml and how to fall back. With it, the pattern is one doc; every verb file follows the same shape.

When the implementing engineer for a Tier 1/2/3 item adds a flag check to a verb, they:

1. Read this file.
2. Add the canonical `**Feature-flag check** ...` line to the verb's preamble (or in-phase).
3. Implement the new behavior under the `true` branch.
4. Verify the v4.0.x fallback path still works.
5. Add the flag name to `tools/v4-first-run.md` Step 4's `features:` block (if it's a new flag).

Source: V4_DESIGN.md §4.23. ADR: `02-design/decisions/2026-05-22-feature-flag-layer.md`. Tier 0 item: F1 (this PR introduces both this loader doc and the seeded `features:` block in v4-first-run.md).
