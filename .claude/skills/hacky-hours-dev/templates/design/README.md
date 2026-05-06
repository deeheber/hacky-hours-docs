# Two-tier design templates

**Status:** Prototype (v3.0.0, ARCHITECTURE only)
**Pattern owner:** ADR `2026-05-06-migrate-to-skill-format.md`

Each design doc has two files:

| File | Audience | Purpose | Length |
|---|---|---|---|
| `<DOC>-deep.md` | The engineer / the AI doing the build | The actual blueprint — source of truth for design decisions | As long as it needs to be |
| `<DOC>-summary.md` | The human (especially non-technical) | A faithful condensation for quick gut checks; onramp into the deep doc | One screen, no scrolling |

## Why two tiers (and which one is canonical)

Demo sessions with non-engineers showed the framework's single-tier docs were experienced as "walls of text." Users either skimmed and rubber-stamped, or relied on Claude to summarize back what they had supposedly written.

The two-tier pattern fixes this **without** moving the source of truth away from the spec:

- **The deep dive is the blueprint.** Built first. The user works through it section by section with Claude, the same way they'd work through any design doc. This is what Step 4 (Build) reads when implementing. Decisions, tradeoffs, threat models, data invariants — all live here.
- **The summary is a derivative.** Built after the deep dive is signed off. A faithful condensation: diagram, one-sentence what-it-does, three key decisions distilled from the deep doc, the most important tradeoff, and cross-links into deep-dive sections. **The summary never adds new information and never makes new decisions.** If the summary and deep dive disagree, the summary is wrong — regenerate it from the deep dive.

This protects against the original failure mode: if a non-technical user only reads the summary and signs off, they're signing off on a faithful view of the spec, not a generated artifact that may have drifted from it. The summary is a navigation tool, not a replacement for the deep dive.

## Standard summary shape

Every summary file should follow the same structure so the user internalizes the *shape*, not just the contents. Each item is a condensation of the corresponding deep-dive section, with a link to the section anchor:

1. **Diagram** — leads the doc. The same diagram as the deep dive (or a simplified subset).
2. **What this does** — one sentence, distilled from the deep dive's System Overview.
3. **Key decisions** — three bullets max. Each cites the section in the deep dive where the full reasoning lives.
4. **What this rules out** — one paragraph. The most important tradeoff. Links to the deep dive's Known Constraints section.
5. **What's next** — links to other docs (their summary + deep) and to specific deep-dive sections of this doc.

The "three bullets max" is a forcing function. If a fourth decision matters enough to surface, the answer is to better-distill the existing three — not to expand the summary.

## Length

Summary files target **one screen, no scrolling at typical reader settings**. ~30 lines of filled-in content. The deep dive is unconstrained — let it be as detailed as the design demands.

## Workflow during Step 2

1. **Build the deep dive first**, section by section. This is the same conversational flow the framework has always used for design docs — questions, decisions, diagrams. The deep dive is what gets the time investment.
2. **Sign off on the deep dive.** This is the explicit milestone — the spec is done.
3. **Generate the summary from the deep dive.** Mechanical condensation. Walk through the standard shape, picking up the highlights from the deep dive's sections and adding cross-links.
4. **Validate the summary against the deep dive.** Read both and check: does the summary make any claim the deep dive doesn't? Does it omit anything load-bearing? Adjust the summary, never the deep dive (unless validation surfaces a real bug in the deep dive — in which case fix the deep, then regenerate the summary).

## Status of this prototype

ARCHITECTURE is the first design doc using this pattern. Once it has been used in at least one real project session and feedback is in, the pattern will be applied to the remaining design docs (DATA_MODEL, USER_JOURNEYS, SECURITY_PRIVACY, etc.) in a follow-up.
