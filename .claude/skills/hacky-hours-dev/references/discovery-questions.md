# Discovery questions — Phase 1.0 of Step 1 (v4.1+)

The three questions every Step 1 Ideation phase asks before synthesizing PRODUCT_OVERVIEW.md — when `features.discovery_phase: true` in settings.yml.

Design source: ADR `hacky-hours/02-design/decisions/2026-05-22-discovery-phase.md`. Locked decision: V4_DESIGN.md §4.30. Triggered by: GitHub issue #11 piece 5.

---

## What this enables

v4.0.x's Step 1 *synthesized* the founder's brief into PRODUCT_OVERVIEW.md — capturing what the founder said in structured form. It did not *interrogate* whether the brief was the right shape for what the founder actually wanted.

Two recent dogfooding misses showed the cost:

- **pomodoro:** founder said "Mario game"; team delivered SMB1-generic sprites. Founder wanted SMB2 USA Subcon specifically.
- **reciprocator:** founder said "pathing tool"; team delivered a wizard with a results page. Founder wanted an explorer-with-pathing-as-one-mode.

Both required the founder to catch — the team had no native moment to ask "is this the right shape?" Discovery makes that moment structural.

---

## When this fires

Phase 1.0 in `steps/01-ideate.md`. Gated by `features.discovery_phase: true` (default `false` in v4.1.x; flipped to `true` in v4.1.0 release).

When the flag is off, Phase 1.0 is skipped; v4.0.x behavior is preserved (synthesize the brief directly into PRODUCT_OVERVIEW.md). When on, Phase 1.0 runs before any synthesis write.

---

## The three questions

Asked sequentially. Each output writes to `ROOT_PATH/01-ideate/DISCOVERY.md` (or appends if the file exists from a prior session). Format: question header + answer block.

### Question 1 — The current workflow

> *"What is the user doing today, before they reach this product? Walk me through their workflow — what do they Google, what tools do they use, what spreadsheets do they build, who do they ask?"*

**Why:** forces the founder to articulate the as-is workflow. The product should fit into (or replace) a real activity, not introduce a wizard for a workflow the user wasn't running.

**Output:** Markdown bullet list under `## Question 1 — Current workflow` in `DISCOVERY.md`. Five to eight bullets is typical.

**Watch for:** if the founder describes the user *as if the product already existed* ("they use my tool to..."), redirect — *"before this product existed, what were they doing?"*

### Question 2 — The 5-second homepage gut-check

> *"If a stranger lands on your homepage and you have 5 seconds before they leave: what do they see, and what do they feel? Describe it. If you can sketch it (ASCII / Markdown / Mermaid / whatever), even better."*

**Why:** forces the founder to articulate the product's first-impression shape. This is where the pomodoro and reciprocator misses would have surfaced — *"I see a map of US states" → "no, you actually see a wizard"* is the gap that produces the framing miss.

**Output:** Markdown prose + optional ASCII / Mermaid mockup under `## Question 2 — Homepage in 5 seconds` in `DISCOVERY.md`.

**Watch for:** if the founder describes features rather than visuals, redirect — *"OK, but visually — what do they see?"* A list of features isn't a homepage.

### Question 3 — The smallest first-session action

> *"What's the smallest thing you'd want a user to do in their first session? Not 'complete the whole flow' — the smallest concrete action that proves they got value."*

**Why:** constrains future scope. Anything that helps a user complete THIS action is in MVP; everything else is V1+. Forces specific articulation of activation.

**Output:** one-sentence description under `## Question 3 — Smallest first-session action` in `DISCOVERY.md`.

**Watch for:** if the founder describes a *value proposition* ("see how easy it is"), redirect — *"what concrete action — what do they click, type, see?"*

---

## After the three questions: lo-fi homepage gate

The framework produces a **lo-fi homepage mockup** at `ROOT_PATH/01-ideate/HOMEPAGE-SKETCH.md`, derived from Question 2's answer. ASCII / Markdown / Mermaid is fine — the medium isn't the point; the *gut-check* is.

Present the sketch to the founder:

> *"Does this look like what you described? If not, what's missing or wrong?"*

Three possible responses:

1. **"Yes, that's it"** → continue to PRODUCT_OVERVIEW.md synthesis.
2. **"Mostly, but X / Y / Z"** → revise the sketch inline; re-present until acknowledged.
3. **"No — this isn't the right shape"** → return to Discovery (especially Question 2). The framing is wrong; surface this honestly: *"Got it. Let's revisit the homepage question — what was different about what you imagined?"* and iterate before synthesizing.

The gate is **owner sign-off on the sketch**. Architecture (Step 2) does not commit until this acknowledgment.

When `features.discovery_phase: false`, this gate is skipped along with Phase 1.0.

---

## What Discovery feeds into

`DISCOVERY.md` and `HOMEPAGE-SKETCH.md` live in `01-ideate/` alongside `IDEATION.md` and `PRODUCT_OVERVIEW.md`. They are inputs to PRODUCT_OVERVIEW.md synthesis (Step 1's normal output) — and explicitly *not* replacements for it.

When `PRODUCT_OVERVIEW.md` is written, the synthesis can reference Discovery findings (e.g., the as-is workflow informs Who; the 5-second homepage informs What; the smallest first-session action informs What's MVP). The Discovery files persist as reference for later steps (Step 2 Design reads them; Step 3 Roadmap reads them).

In the archive when Step 5 closes a milestone, Discovery files move to `archive/<date>/discovery/` alongside the rest of the milestone's Step 1 artifacts.

---

## Cost shape

Discovery adds three questions + one sketch + one acknowledgment to Step 1. Net token cost: roughly +2–4K tokens per Step 1 invocation when the flag is on. Cheap relative to the framing-miss cost it prevents (downstream architecture rework when the framing turns out to be wrong).

No preflight; Step 1 is not a heavy verb.

---

## What this verb completes

T1.1 (this PR) wires the Discovery phase into Step 1. The cost is one verb adding three questions; the benefit is framing-level course correction *before* architecture commits.

When the implementing engineer extends this pattern to other verbs in the future, they:

1. Read this file.
2. Reference the three-question shape; adapt the questions to the verb's surface.
3. Gate behind a feature flag during early roll-out; flip default-on at the next major release.

Source: V4_DESIGN.md §4.30. ADR: `02-design/decisions/2026-05-22-discovery-phase.md`.
