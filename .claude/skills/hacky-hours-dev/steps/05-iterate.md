# Step 5 — Iterate

*Supporting file for the `hacky-hours` skill. Loaded when the user is at Step 5.*

**Context:** Read `04-build/CHANGELOG.md` to understand what shipped in the last release. Read `04-build/BACKLOG.md` to see if anything is already queued. Skim the Step 2 design docs.

**Purpose:** Capture bugs, ideas, and improvements after a release, amend the docs that need updating, and queue the work.

**Pre-flight:** Before producing any output, Read `${CLAUDE_SKILL_DIR}/references/team-preflight.md` and run its checks. This verb assumes the global skeleton and the active team exist.

**Team chat mode:** Before producing any role-driven output, read `${CLAUDE_SKILL_DIR}/references/chat-format.md` and honor the current `team_chat` value from `~/.hacky-hours/settings.yml` (default `minimal`) throughout this verb. **No tokens for tokens' sake** — every voice turn must add information.

**Cost instrumentation (v4.1+):** Each phase + each role-turn + the verb itself are loggable units per `${CLAUDE_SKILL_DIR}/references/cost-instrumentation.md`. Schema is stable; harness populates token counts as instrumentation rolls out.

**Team learning capture:** Iteration is always multi-role (synthesis touches whoever owns the design docs that need amendment). At the tail, run **Phase 6 — Stash** per `${CLAUDE_SKILL_DIR}/references/capture-format.md`: silent `history.md` append for each participating agent, then the one-line behavior-feedback prompt. Track which agents actually weighed in during synthesis and amendment.

**Phase 1: Capture**

Before asking the user anything, check `ROOT_PATH/feedback/` for any feedback files (`feedback-<username>-<timestamp>.md`). If files exist, read and summarize them. Tell the user: "I found N feedback file(s) from recent learn sessions. Here's what they say: [summary]."

Then ask the user to brain-dump freely: bugs, feedback, ideas for improvements. Write everything into `ITERATION.md` under ROOT_PATH. No filtering yet — just capture.

Prompts:
- "What's broken or annoying that you've noticed since the last release?"
- "What did users ask for that you didn't have time to build?"
- "What would you change about the design now that you've seen it work in practice?"

**Phase 2: Synthesize**

Read `ITERATION.md` alongside the existing design docs. For each item:
- Does this change how the product works? → Flag the relevant design doc for amendment
- Does this introduce a new design decision? → Note that an ADR will be needed
- Is this purely an implementation fix? → Goes straight to backlog

**Lightweight review check:** While reviewing design docs, flag any that look oversized, stale, or mostly placeholder. If multiple docs are flagged, suggest running `/hacky-hours review 2` after the iteration cycle completes.

**Phase 3: Prioritize**

Categorize each item:
- **Hotfix** — broken in production, needs immediate attention
- **Next milestone** — important enough to be in the next planned release
- **Backlog** — valid but not urgent; add to BACKLOG.md without a milestone assignment

**Phase 4: Amend design docs**

For each flagged design doc, work through the needed changes. Write ADRs for significant decisions. Update affected sections.

**Phase 5: Build**

Proceed with the Step 4 build cycle using the updated backlog.

**Phase 6: Stash (team learning)**

Run per `${CLAUDE_SKILL_DIR}/references/capture-format.md`:

1. List the agents that actually participated in synthesis and amendment.
2. Compose a one-sentence past-tense contribution summary per participant (concrete — what they actually flagged, amended, or co-authored).
3. Resolve the session ID per the algorithm in `capture-format.md`.
4. **History append + metrics refresh (silent):** for each participant, append `- <date> · <project-slug> · iterate · <summary>` to `~/.hacky-hours/teams/<active>/agents/<agent-id>/history.md`. Then refresh the `metrics:` block in each participating agent's `profile.md` per `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Derived metrics" + §"Level derivation". Commit both files together: `git -C ~/.hacky-hours/teams/<active>/ add agents/*/history.md agents/*/profile.md && git commit -m "history: iterate @ <project> @ <date> — <N> agent(s)"`.
5. **Behavior feedback prompt:** ask the conductor *"Anything you said during this run that should change how an agent works in future sessions? Free-form by agent, or `none`."* For each agent named, write `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the schema.
6. **Footer:** print *"Stashed <N> behavior note(s) for <agents>. Appended history to <count> agent(s) (commit <sha>). Promote with `/hacky-hours team update` when ready."*

**Done when:** ITERATION.md has been fully triaged, design docs reflect current reality, and new items are in BACKLOG.md. Move `ITERATION.md` to `ROOT_PATH/archive/` when complete. ✅
