# Step 2 — Design

*Supporting file for the `hacky-hours` skill. Loaded when the user is at Step 2.*

**Context:** Read `01-ideate/PRODUCT_OVERVIEW.md` under ROOT_PATH — specifically the Constraints & Values section. Also note which design docs already exist.

**Purpose:** Define how the product works in enough detail to build it.

**Pre-flight:** Before producing any output, Read `${CLAUDE_SKILL_DIR}/references/team-preflight.md` and run its checks. This verb assumes the global skeleton and the active team exist.

**Team chat mode:** Before producing any role-driven output, read `${CLAUDE_SKILL_DIR}/references/chat-format.md` and honor the current `team_chat` value from `~/.hacky-hours/settings.yml` (default `minimal`) throughout this verb. **No tokens for tokens' sake** — every voice turn must add information.

**Team learning capture:** This verb is always multi-role (design fans out across Architect, Security, A11y, Data, Licensing, QA at minimum). At the tail, run **Phase N — Stash** per `${CLAUDE_SKILL_DIR}/references/capture-format.md`: silent `history.md` append for each participating agent, then the one-line behavior-feedback prompt. Track which agents actually contributed to each doc — that list drives both writes.

Start by asking which documents this project actually needs:

| Document | Use when... |
|----------|-------------|
| ARCHITECTURE | The product has multiple systems or services |
| DATA_MODEL | The product stores or transforms data of any kind |
| USER_JOURNEYS | You need to map how users move through the product |
| STYLE_GUIDE | The product has a UI |
| ACCESSIBILITY | The product has a UI (almost always) |
| MARKET_FIT | You want to validate who the users are and why they'd choose this |
| BUSINESS_LOGIC | The product has rules, calculations, or domain-specific behavior |
| SECURITY_PRIVACY | The product handles user data, auth, or payments (almost always) |
| LICENSING | Almost always — ask early, before dependencies are chosen |
| TESTING | Almost always — test strategy and definition of done |

**Two-tier design artifacts (v3.0.0):** Each design doc consists of a **deep dive** (`<DOC>-deep.md` — the actual blueprint, source of truth) plus a **summary** (`<DOC>-summary.md` — a derivative one-screen view for quick gut checks and as a navigation onramp for non-technical readers). Templates live in `${CLAUDE_SKILL_DIR}/templates/design/<DOC>-deep.md` and `<DOC>-summary.md`. **Read `${CLAUDE_SKILL_DIR}/templates/design/README.md` first** — it specifies the pattern, the workflow, and the discipline that keeps the two files in sync.

**Workflow for each doc:**

1. **Build the deep dive first.** Walk the user through it section by section using questions, the same way you would for any design doc. Generate Mermaid diagrams proactively. The deep dive is what gets the time investment — the summary is mechanical compression that comes after.
2. **Sign off on the deep dive.** Confirm with the user that the deep dive captures the architecture / data model / threat model / etc. Make this an explicit milestone before moving on.
3. **Generate the summary as a faithful condensation.** Walk through the standard summary shape (diagram → one-sentence what-it-does → three key decisions max → most-important tradeoff → cross-links). Each summary item is distilled from the corresponding deep-dive section, with a section-anchor link so readers can drill in. **Never add information to the summary that isn't in the deep dive. Never make new decisions in the summary.**
4. **Validate the summary against the deep dive.** Read both side by side. Does the summary make any claim the deep dive doesn't? Does it omit anything load-bearing? If yes, fix the summary, not the deep dive (unless validation surfaced a real bug — in which case fix the deep dive, then regenerate the summary).

If the user wants to skip the deep dive and just write the summary: push back. The summary alone is the failure mode the two-tier pattern was designed to prevent. The deep dive is where the thinking happens; the summary is just the view.

**When a design decision changes during iteration:** write an Architecture Decision Record (ADR) in `02-design/decisions/` named by date and topic (e.g., `2026-03-20-switch-to-postgres.md`). Update the **deep dive** first — that's the source of truth. Then regenerate or update the affected lines of the summary. Add a note in the deep dive pointing to the ADR.

---

**Phase N — Stash (team learning).** Run per `${CLAUDE_SKILL_DIR}/references/capture-format.md`:

1. List the agents that actually authored or co-authored design docs during this run (e.g., Architect on ARCHITECTURE, Security on SECURITY_PRIVACY, Data + Backend on DATA_MODEL, etc.).
2. Compose a one-sentence past-tense contribution summary per participant (concrete: "Authored ARCHITECTURE-deep.md sections 1–3 covering the API gateway split" — not "Helped with design").
3. Resolve the session ID per the algorithm in `capture-format.md`.
4. **History append + metrics refresh (silent):** for each participant, append `- <date> · <project-slug> · design · <summary>` to `~/.hacky-hours/teams/<active>/agents/<agent-id>/history.md`. Then refresh the `metrics:` block in each participating agent's `profile.md` per `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Derived metrics" + §"Level derivation". Commit both files together: `git -C ~/.hacky-hours/teams/<active>/ add agents/*/history.md agents/*/profile.md && git commit -m "history: design @ <project> @ <date> — <N> agent(s)"`.
5. **Behavior feedback prompt:** ask the conductor *"Anything you said during this run that should change how an agent works in future sessions? Free-form by agent, or `none`."* For each agent named, write `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the schema.
6. **Footer:** print *"Stashed <N> behavior note(s) for <agents>. Appended history to <count> agent(s) (commit <sha>). Promote with `/hacky-hours team update` when ready."*

**Done when:** Both `<DOC>-deep.md` and `<DOC>-summary.md` exist for every design doc the project needs, the deep dive contains the actual blueprint with implementation-ready detail, and the summary is a faithful one-screen condensation that cross-links into the deep dive. ✅
