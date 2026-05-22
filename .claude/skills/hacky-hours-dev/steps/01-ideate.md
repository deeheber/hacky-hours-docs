# Step 1 — Ideation

*Supporting file for the `hacky-hours` skill. Loaded when the user is at Step 1.*

**Context:** If `IDEATION.md` already exists under ROOT_PATH, read it before asking any questions — don't ask the user to repeat what they've already written.

**Purpose:** Get ideas out of the user's head and into structured form.

**Pre-flight:** Before producing any output, Read `${CLAUDE_SKILL_DIR}/references/team-preflight.md` and run its checks. This verb assumes the global skeleton and the active team exist.

**Team chat mode:** Before producing any role-driven output, read `${CLAUDE_SKILL_DIR}/references/chat-format.md` and honor the current `team_chat` value from `~/.hacky-hours/settings.yml` (default `minimal`) throughout this verb. **No tokens for tokens' sake** — every voice turn must add information.

**Cost instrumentation (v4.1+):** Each phase + each role-turn + the verb itself are loggable units per `${CLAUDE_SKILL_DIR}/references/cost-instrumentation.md`. Schema is stable; harness populates token counts as instrumentation rolls out. Skill files declare instrumentable points; the harness writes the JSONL rows.

**Team learning capture:** This verb fans out to roles (mainly Product, with Licensing and Security weighing in on Constraints & Values). At the tail, run **Phase N — Stash** per `${CLAUDE_SKILL_DIR}/references/capture-format.md`: silent `history.md` append for each participating agent, then the one-line behavior-feedback prompt. Track which agents actually contributed.

**IDEATION.md** is a free-writing space. No rules — just capture everything. Prompt the user with:
- "Who is the first person you'd want to use this, and what would they do with it?"
- "What problem have you personally experienced that this solves?"
- "What would have to be true for this to be considered a success in one year?"

**PRODUCT_OVERVIEW.md** synthesizes IDEATION.md into five W answers plus a Constraints & Values section:
- **Who** — target audience (specific, not "anyone")
- **What** — what the product does and what form it takes
- **Where** — platform (mobile, web, desktop, API, etc.)
- **When** — rough timeline or priority
- **Why** — the problem it solves and why it matters
- **Constraints & Values** — licensing intent, privacy stance, infrastructure preference

Go one W at a time. Ask focused questions. Reflect the user's words back to them.

After completing the 5Ws, always ask the Constraints & Values questions before moving to Step 2:

1. **Licensing:** "Do you want your code to be open source — meaning others can see, use, and build on it — or do you want to keep it private? Are you planning to charge money for it?"
2. **Privacy:** "How much user data does this product really need to collect? Less is almost always safer, cheaper, and easier to comply with legally."
3. **Infrastructure:** "Do you want someone else to manage the servers, or are you comfortable managing your own?"

These answers seed the `LICENSING.md` and `ARCHITECTURE.md` work in Step 2.

---

**Phase N — Stash (team learning).** Run per `${CLAUDE_SKILL_DIR}/references/capture-format.md`:

1. List the agents that actually participated during this run (typically: Product; possibly Licensing, Security, Architect on Constraints & Values).
2. Compose a one-sentence past-tense contribution summary per participant.
3. Resolve the session ID per the algorithm in `capture-format.md`.
4. **History append + metrics refresh (silent):** for each participant, append `- <date> · <project-slug> · ideate · <summary>` to `~/.hacky-hours/teams/<active>/agents/<agent-id>/history.md`. Then refresh the `metrics:` block in each participating agent's `profile.md` per `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Derived metrics" + §"Level derivation". Commit both files together: `git -C ~/.hacky-hours/teams/<active>/ add agents/*/history.md agents/*/profile.md && git commit -m "history: ideate @ <project> @ <date> — <N> agent(s)"`.
5. **Behavior feedback prompt:** ask the conductor *"Anything you said during this run that should change how an agent works in future sessions? Free-form by agent, or `none`."* For each agent named, write `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the schema.
6. **Footer:** print *"Stashed <N> behavior note(s) for <agents>. Appended history to <count> agent(s) (commit <sha>). Promote with `/hacky-hours team update` when ready."*

**Done when:** Someone unfamiliar with the project could read PRODUCT_OVERVIEW.md and understand what's being built, including its core values and constraints. ✅
