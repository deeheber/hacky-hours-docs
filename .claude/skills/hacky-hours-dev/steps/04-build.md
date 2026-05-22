# Step 4 — Build

*Supporting file for the `hacky-hours` skill. Loaded when the user is at Step 4.*

**Context:** Read `04-build/BACKLOG.md` to see what's queued. For each task, read the relevant design doc sections — particularly `SECURITY_PRIVACY` and `LICENSING.md`. If `ROADMAP.md` exists, confirm the task belongs to the current milestone before starting.

**Purpose:** Implement incrementally, with review at each step, aligned to design decisions.

**Pre-flight:** Before producing any output, Read `${CLAUDE_SKILL_DIR}/references/team-preflight.md` and run its checks. This verb assumes the global skeleton and the active team exist.

**Team chat mode:** Before producing any role-driven output, read `${CLAUDE_SKILL_DIR}/references/chat-format.md` and honor the current `team_chat` value from `~/.hacky-hours/settings.yml` (default `minimal`) throughout this verb. **No tokens for tokens' sake** — every voice turn must add information.

**Cost instrumentation (v4.1+):** Each phase + each role-turn + the verb itself are loggable units per `${CLAUDE_SKILL_DIR}/references/cost-instrumentation.md`. Schema is stable; harness populates token counts as instrumentation rolls out.

**Team learning capture:** Build is *sometimes* multi-role (each task typically engages 1–3 roles). At the tail of each task — not each session — run **Phase N — Stash** per `${CLAUDE_SKILL_DIR}/references/capture-format.md` for the roles that contributed to that task: silent `history.md` append per participating agent, then the behavior-feedback prompt. If only one role engaged, history still fires for that role; the prompt is still shown (conductor can answer `none`).

Before starting any task:
1. **Read the deep-dive design docs (`<DOC>-deep.md`), not the summaries.** The deep dive is the source of truth and contains the Implementation Notes section that drives the build. Summaries are derivative — for human gut-checks only — and intentionally omit build-phase detail.
2. If a project still has single-tier design docs (e.g., `ARCHITECTURE.md` without the `-deep` / `-summary` split), read those. The two-tier pattern is opt-in for projects upgrading from earlier versions.
3. If a design doc doesn't address something you need to implement, surface it to the user first — the deep dive may need a new section. Update the deep dive, then regenerate the summary.

The task cycle:
1. Pick a task from BACKLOG.md
2. Create a branch named for the task (e.g., `feat/user-signup`, `fix/login-error`)
3. Implement — referencing design documents throughout
4. Before marking complete, verify against the pre-merge checklist (see SKILL.md)
5. Commit with a clear message, push, open a pull request for human review
6. Merge, update CHANGELOG.md, tag a release when a milestone is complete

**Milestone housekeeping (run when BACKLOG.md is empty):**
- Append milestone entry to CHANGELOG.md; move entries older than 3 releases to `archive/changelog/`
- Move the completed roadmap milestone section to `archive/roadmap/`
- Update any design docs that changed; write ADRs for significant decisions
- Move `IDEATION.md` to `archive/` if not already done
- Review `.claudeignore` — anything newly cold that should be excluded?
- Tag the release

---

**Phase N — Stash (team learning, runs at task completion not milestone).** Run per `${CLAUDE_SKILL_DIR}/references/capture-format.md`:

1. List the agents that actually participated on the task that just completed (typically: the implementing role, possibly QA on the test plan, possibly Architect on design alignment).
2. Compose a one-sentence past-tense contribution summary per participant. Reference the task slug from BACKLOG.md.
3. Resolve the session ID per the algorithm in `capture-format.md`.
4. **History append + metrics refresh (silent):** for each participant, append `- <date> · <project-slug> · build:<task-slug> · <summary>` to `~/.hacky-hours/teams/<active>/agents/<agent-id>/history.md`. Then refresh the `metrics:` block in each participating agent's `profile.md` per `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Derived metrics" + §"Level derivation". Commit both files together: `git -C ~/.hacky-hours/teams/<active>/ add agents/*/history.md agents/*/profile.md && git commit -m "history: build <task-slug> @ <project> @ <date> — <N> agent(s)"`.
5. **Behavior feedback prompt:** ask the conductor *"Anything you said during this task that should change how an agent works in future sessions? Free-form by agent, or `none`."* For each agent named, write `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the schema.
6. **Footer:** print *"Task stash: <N> behavior note(s) for <agents>; history appended for <count> agent(s) (commit <sha>). Promote with `/hacky-hours team update` when ready."*

**Done when:** All milestone tasks are merged, CHANGELOG.md is updated, and you've cut a tagged release. 🎉
