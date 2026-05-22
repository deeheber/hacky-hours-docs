# Step 3 — Roadmap

*Supporting file for the `hacky-hours` skill. Loaded when the user is at Step 3.*

**Context:** Read all Step 2 design documents that exist under ROOT_PATH. If `ROADMAP.md` already exists, read it and identify what's already placed.

**Purpose:** Sequence what to build and prioritize ruthlessly.

**Pre-flight:** Before producing any output, Read `${CLAUDE_SKILL_DIR}/references/team-preflight.md` and run its checks. This verb assumes the global skeleton and the active team exist.

**Team chat mode:** Before producing any role-driven output, read `${CLAUDE_SKILL_DIR}/references/chat-format.md` and honor the current `team_chat` value from `~/.hacky-hours/settings.yml` (default `minimal`) throughout this verb. **No tokens for tokens' sake** — every voice turn must add information.

**Team learning capture:** Product owns roadmap, with Architect weighing in on sequencing and risk and other roles surfacing scope concerns from their disciplines. At the tail, run **Phase N — Stash** per `${CLAUDE_SKILL_DIR}/references/capture-format.md`: silent `history.md` append for each participating agent, then the one-line behavior-feedback prompt.

List every feature mentioned across the Step 2 documents. Then categorize each:

- **MVP** — the smallest version that proves the core value proposition. Push back hard. "Can the product prove its value without this?" If yes, it's not MVP.
- **V1** — MVP plus what's needed for it to be genuinely useful
- **V2+** — valuable but not required for V1

Milestones should be outcome-based ("users can complete a purchase") not task-based ("implement checkout UI").

After the MVP list is set, ask: "Based on what's in the MVP, how long do you realistically think this would take to build? What are the most complex or risky parts?" If the answer suggests months, the MVP is probably still too big.

---

**Phase N — Stash (team learning).** Run per `${CLAUDE_SKILL_DIR}/references/capture-format.md`:

1. List the agents that actually participated (typically: Product, Architect; possibly Security/Ops/QA if scope risk surfaced from those lenses).
2. Compose a one-sentence past-tense contribution summary per participant.
3. Resolve the session ID per the algorithm in `capture-format.md`.
4. **History append + metrics refresh (silent):** for each participant, append `- <date> · <project-slug> · roadmap · <summary>` to `~/.hacky-hours/teams/<active>/agents/<agent-id>/history.md`. Then refresh the `metrics:` block in each participating agent's `profile.md` per `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Derived metrics" + §"Level derivation". Commit both files together: `git -C ~/.hacky-hours/teams/<active>/ add agents/*/history.md agents/*/profile.md && git commit -m "history: roadmap @ <project> @ <date> — <N> agent(s)"`.
5. **Behavior feedback prompt:** ask the conductor *"Anything you said during this run that should change how an agent works in future sessions? Free-form by agent, or `none`."* For each agent named, write `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the schema.
6. **Footer:** print *"Stashed <N> behavior note(s) for <agents>. Appended history to <count> agent(s) (commit <sha>). Promote with `/hacky-hours team update` when ready."*

**Done when:** Every planned feature has a home (MVP, V1, or V2+), and the MVP is small enough to actually ship and learn from. ✅
