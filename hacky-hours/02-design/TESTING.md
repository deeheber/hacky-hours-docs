# TESTING.md

**Step 2 — Design** | hacky-hours-docs

---

## What is This?

A testing design document describes how you verify that what you built actually works the way you intended. It covers your testing strategy, what kinds of tests you'll write (or run manually), and what "good enough" looks like before you ship.

For most projects this means code tests. For hacky-hours-docs, which has no code, it means something different — see below.

---

## Testing Strategy

hacky-hours-docs has no runtime code. The "product" is a command prompt and a set of Markdown templates. Testing here means verifying that:

1. **The command routes correctly** — every argument lands in the right workflow
2. **The generated artifacts are correct** — scaffolded files have the right structure, paths, and content
3. **The guidance is internally consistent** — docs referenced in one place exist and say what they're claimed to say
4. **New commands behave as specified** — the guidance matches what the command prompt actually does

### Testing Layers

| Layer | What it covers | How it's done |
|-------|----------------|---------------|
| Command routing | Does `/hacky-hours <arg>` land in the right section? | Manual invocation + eval scripts |
| Scaffold output | Does scaffold produce the correct file structure? | Manual dry-run review |
| Cross-reference integrity | Do links between docs point to real targets? | `review 2` Phase 3 |
| Command guidance accuracy | Does the help text match the actual behavior? | Manual review before release |
| Generated Astro sites (v1.8.0+) | Do tour/quiz sites render correctly and meet WCAG 2.1 AA? | Manual browser testing + axe/Lighthouse |

### What We Don't Test (and Why)

- **LLM output quality** — Claude's responses are non-deterministic. We can test routing and structure, not the quality of every conversation.
- **User project outcomes** — we can't verify that a user's PRODUCT_OVERVIEW.md is "good." We verify that the command asked the right questions.
- **Every edge case of `--root` paths** — accepted fragility. We test the default (`hacky-hours/`) and the project root (`--root .`) and treat other paths as best-effort.

---

## Pre-Release Checklist

Before tagging any release:

- [ ] All new command arguments tested via manual invocation in a clean repo
- [ ] `dry-run` tested for any new scaffold changes
- [ ] `audit` run against this repo — scorecard reviewed
- [ ] `optimize` run — Phase 3 cross-reference check passes
- [ ] Version strings bumped in all three places (routing table, help message, subcommand help)
- [ ] For releases with new web artifacts (v1.8.0+): Astro sites tested in browser, Lighthouse accessibility score reviewed

---

## Eval Framework (Command Behavior)

The `hacky-hours-workspace` skill eval system provides structured test cases for command behavior. Evals compare responses with and without the skill loaded to measure behavioral consistency.

Current eval coverage:
- `version` — verifies version string matches latest tag
- `status` — verifies correct level detection
- `dry-run` — verifies no files are written
- `audit` — verifies help text format

Gaps (not yet covered by evals):
- `iterate`, `optimize`, `pivot` workflows
- `learn` suite (v1.8.0 — needs evals written as part of implementation)
- `upgrade` (v1.8.0 — needs evals written as part of implementation)

---

## v1.8.0 Testing Notes

The learn suite introduces the first interactive web artifacts in the framework. Before these ship:

1. **Astro build:** Run `npm run build` in each generated site (`learn/tour/`, `learn/quiz/`) and verify no build errors
2. **Feedback form:** Test that submitting the feedback form writes a correctly named file to `hacky-hours/feedback/`
3. **`onboard` git push:** Test in a repo with a remote that the feedback commit stages only the feedback file (not other working tree changes)
4. **Node.js fallback:** Test that all three learn modes degrade cleanly to conversation mode when Node is not installed

---

## Cost benchmarking + token instrumentation (v4.1+)

v4.0.0 was dogfooded only on Claude Max. v4.1 introduces a feature-flag layer (§4.23) that lets users gate cost-heavy mechanisms, but requires actual benchmark data to recommend sensible defaults per plan.

### Benchmark methodology

A representative-project taxonomy and verb suite drives benchmarking:

| Project shape | Representative project | Verb suite |
|---|---|---|
| Small | Single-file utility (e.g., a CLI tool with one design doc) | `ideate`, full `design`, `audit`, `iterate` cycle |
| Medium | Multi-doc project with 4–6 roles engaged (e.g., reciprocator-shaped) | Above + `arbitrate`, `team reflect --all` |
| Large | Existing codebase brought via `adopt` with 50+ files (e.g., hacky-hours-docs itself) | Above + `team backfill`, full `audit` Lane A |

For each (project, verb) cell: measure total input tokens, output tokens, per-role share, per-phase share, wall-clock time. Run with `team_chat: off`, `minimal`, `full` separately. Run with `features.workroom_mode: false` and `true` separately.

### Instrumentation

A new `references/cost-instrumentation.md` defines the hook contract: per-verb log entries appended to `~/.hacky-hours/sessions/<id>/cost-log.jsonl`. Schema:

```json
{"ts": "ISO", "verb": "audit", "phase": "lane-a", "role": "security",
 "input_tokens": N, "output_tokens": N, "model": "claude-opus-4-7",
 "wall_ms": N, "cache_hits": N}
```

JSONL chosen for same reasons as `messages.jsonl` — append-safe, cheap to consume.

### Feasibility matrix

Output: `02-design/COST_MODEL.md` documents the cross-product of (verb × plan-tier × features). Each cell gets a green/yellow/red verdict:

- **🟢 Green** — runs comfortably within plan limits at default settings.
- **🟡 Yellow** — runs with caution; preflight estimate should fire; user should consider disabling cost-heavy features.
- **🔴 Red** — likely to exhaust plan tier's daily allowance; recommended only with explicit downshift or on a higher plan.

The matrix becomes the source of truth for plan-aware defaults in `tools/v4-first-run.md` and for the preflight estimates in `references/cost-model.yml`.

### Workroom verb test methodology (v4.1+)

v4.1's workroom verbs produce non-deterministic transcripts (LLM variation). Test approach:

- **Schema validation:** every produced `messages.jsonl` entry must validate against the schema in V4_DESIGN §6 / capture-format.md.
- **Structural assertions:** turn count is within `workroom_max_turns`; role attribution is non-empty; channel is consistent; `in_reply_to` references resolve.
- **Snapshot tests for digests:** the digest's "Disagreements" section must be present (even if empty); per-discipline summary count matches participating role count; "Open questions" section is parseable as a list.
- **Cost tests:** total tokens for a fixture workroom run stays within a published bound (with margin for LLM variation).

We do not assert on transcript content — that's the LLM-non-determinism boundary preserved from v4.0.

## Related

- [ARCHITECTURE.md](./ARCHITECTURE.md) — Known Fragility section
- [ACCESSIBILITY.md](./ACCESSIBILITY.md) — WCAG 2.1 AA requirements for generated sites
- [SECURITY_PRIVACY.md](./SECURITY_PRIVACY.md) — Risk Surface section on automated git push
- [V4_DESIGN.md](./V4_DESIGN.md) §4.23 — Feature-flag layer
- ADR: `02-design/decisions/2026-05-22-feature-flag-layer.md`
- `references/cost-model.yml` (to be authored in Tier 4 / R1 of v4.1.0)
