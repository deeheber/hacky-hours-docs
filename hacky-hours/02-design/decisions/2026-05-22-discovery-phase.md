# ADR: Discovery phase in Step 1 + skeptic mode flag

**Date:** 2026-05-22
**Status:** Accepted
**Slice:** v4.1.0 Tier 1 (T1.1, T1.2)
**Issue:** empathetech/hacky-hours-docs#11 (pieces 5, 6)
**Arbitration mode:** decide

## Context

Step 1 (Ideate) currently treats the founder's brief as *synthesis input* — the verb writes PRODUCT_OVERVIEW.md by translating what the founder said into structured form (5Ws + Constraints & Values). It does not *interrogate* whether the brief is the right shape for the product the founder actually wants.

Two recent dogfooding misses exposed this gap:

- **pomodoro:** founder said "Mario game"; team delivered SMB1-generic. Founder wanted SMB2 USA Subcon specifically. Team executed the noun without pushing on the specific anchor.
- **reciprocator:** founder said "pathing tool"; team delivered a planner-with-results-page. Founder wanted an explorer-with-pathing-as-one-mode. Team executed the verb without pushing on whether the verb was the whole product.

Both required the founder to catch — the team had no native moment to ask "is this the right shape?"

Additionally, there's a related but distinct gap: even when a framing has been established, the team doesn't have a structural skeptic. When Product proposes a direction, no role is responsible for arguing against it. Productive disagreement is supposed to emerge, but in practice agents converge politely.

## Roles involved

- **📊 Maya (Product)** — discovery is Product's job; the framework's Step 1 currently lets Product skip it. Adding a Discovery phase fixes that at the framework level.
- **🎨 Felix (Design)** — Discovery and lo-fi prototype belong together. The right test for "is this the right shape" is a 5-second-homepage gut-check — verbal or sketched. If the founder can't say what they see in 5 seconds, the framing isn't real yet.
- **🏗️ Priya (Architect)** — skeptic mode shouldn't be a 13th role at v4.1.0; that's a bigger Core-roster change. A modal flag any role can adopt is the lighter-weight v4.1 version. Re-evaluate for v4.2 if signal suggests a dedicated role is better.
- **🛡️ Alex (Security)** — skeptic mode doesn't grant new permissions, just speech-mode. Low risk.
- **🔍 Emma (QA)** — Discovery phase outputs need a testable artifact (the 5-second homepage gut-check sketch); without it, Discovery becomes a verbal exercise that's not auditable.

## Decision

### 1. New phase inside Step 1, not new step

Discovery becomes Phase 1.0 inside `steps/01-ideate.md`. It fires before any synthesis writing happens. Owner lean (during 2026-05-22 iterate Phase 2): keep it inside Step 1 to minimize new skill files and preserve the existing five-step mental model. Rejected: standalone Step 0.5 / 1.5 verb (adds maintenance burden without proportionate benefit).

When `features.discovery_phase: false` (default in v4.1.x), the verb skips this phase — v4.0.x behavior preserved.

### 2. Discovery phase shape

Three questions, asked sequentially, before any PRODUCT_OVERVIEW.md write:

1. **"What is the user doing today, before they reach this product?"**
   Surface: synthesis (Markdown bullet list) of the user's current workflow. Forces explicit articulation of the as-is. Catches the gap where the team executes a verb the founder named without understanding what activity it interrupts or replaces.

2. **"If a stranger lands on your homepage, what do they see in the first 5 seconds, and what do they feel?"**
   Surface: prose + (optional) ASCII / Markdown mockup of the homepage. Forces a 5-second gut-check. Catches framing misses where the team's interpretation of the brief produces a homepage that doesn't match the founder's mental model.

3. **"What's the smallest thing you'd want a user to do in their first session?"**
   Surface: one-sentence description. Forces specific articulation of activation. Constrains future scope discussions (the MVP is whatever satisfies this; everything else is V1+).

Outputs land in `01-ideate/DISCOVERY.md` (new file alongside IDEATION.md and PRODUCT_OVERVIEW.md). Discovery feeds PRODUCT_OVERVIEW.md synthesis but stays around for future reference.

### 3. Lo-fi homepage gut-check gate between Step 1 and Step 2

After Step 1 completes and Discovery is on disk, the framework produces a **lo-fi homepage mockup** (ASCII / Markdown / Mermaid, whichever fits the product). The owner reviews it before Step 2 begins.

Surface: `01-ideate/HOMEPAGE-SKETCH.md`. Single screen, no scrolling at typical reader settings.

The framework asks: *"Does this look like what you described? If not, what's missing or wrong?"*

If the owner rejects or significantly revises, the framework returns to Discovery (or a Step 1 phase that produced the sketch's input) and re-iterates. Architecture (Step 2) doesn't commit until the sketch is acknowledged.

When `features.discovery_phase: false`, this gate is skipped.

### 4. Skeptic mode flag

A new role-mode flag: `--skeptic`. Any role can be invoked with the flag, and the role adopts a structural skeptic posture for that turn:

- Argue against the proposed framing, even when their domain instinct would be to agree.
- Surface the strongest objection from their discipline's lens.
- Name what the team would regret if they're wrong about this framing.

Example: `arbitrate decide --skeptic product "explorer vs. planner"` would have Product argue *against* whatever direction was most apparent.

When `features.skeptic_mode: false` (default v4.1.x), the flag is silently ignored (verbs still work; the flag just doesn't change behavior). When `true`, the role engages skeptic mode for that invocation.

**Cost shape:** one additional role turn per skeptic invocation. Compared to workroom mode, this is cheap; the cost preflight doesn't fire for skeptic-mode alone.

**Multi-skeptic option:** workroom verbs can opt into a "skeptic pass" — after convergence, one role (chosen by the conductor or rotated) argues against the convergence. If the skeptic raises a load-bearing concern, the workroom continues; if not, the digest notes that a skeptic pass was performed.

### 5. v4.2 escalation path

If by v4.2 the modal flag has been used heavily AND produced consistently load-bearing critiques, escalate to a dedicated 13th role:

- **🦂 The Skeptic** (placeholder name) — structurally responsible for challenging accumulated team principles + active framings.

For v4.1.0 the modal flag is sufficient. The bar to "we need a real role for this" is: 10+ uses across at least 3 projects, with the conductor having found the skeptic critique load-bearing in at least 50% of cases.

## Consequences

**Positive:**

- Step 1 now has a structural moment to interrogate the framing, not just synthesize it.
- Lo-fi gate catches framing misses before architecture commits — the exact failure mode pomodoro + reciprocator illustrated.
- Skeptic mode gives the team explicit permission to argue against the apparent direction without breaking the verb's social contract.
- Both behaviors feature-flagged off in v4.1.x → flipped on in v4.1.0 once they've been tested in practice.

**Negative / accepted:**

- Step 1 takes longer when Discovery is enabled (three new questions + one mockup). Mitigated by: most founders welcome these questions; the tax is paid once per project.
- Skeptic-mode invocations are non-deterministic; the same prompt can produce different objections. Acceptable — the point is to surface *any* strong objection from the role's lens, not a canonical one.
- Two new artifacts on disk (`DISCOVERY.md`, `HOMEPAGE-SKETCH.md`) add clutter to `01-ideate/`. Mitigated by: both archive into `archive/<date>/` when Step 2 closes.
- Discovery becomes another thing for the framework to remember to do. Mitigation: Step 1's verb file imports a `references/discovery-questions.md` reference so the phase doesn't drift.

## Alternatives considered

- **New top-level step (Step 0.5 or new "discover" verb).** Rejected per owner lean: too much new surface for a phase that belongs naturally inside Step 1.
- **Skeptic as 13th role in v4.1.0.** Rejected per Architect lean: modal flag is lower-cost trial; escalate if signal warrants.
- **Apply skeptic to every verb automatically.** Rejected: heavy cost + risk of skeptic-fatigue. Opt-in is the right default.
- **Lo-fi gate as Step 1.5 verb instead of phase gate.** Rejected: same reason as Discovery — phase, not new verb.

## Related

- V4_DESIGN.md §4.30 — Discovery phase in Step 1
- V4_DESIGN.md §4.31 — Skeptic mode flag
- `steps/01-ideate.md` — receives new Phase 1.0 + lo-fi gate
- `references/discovery-questions.md` — to be authored as part of T1.1
- ADR: 2026-05-22-feature-flag-layer.md (`features.discovery_phase`, `features.skeptic_mode`)
- #11 pieces 5, 6
- ITERATION.md §A1, §B (the missed-framing pattern this addresses)
