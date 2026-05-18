# /hacky-hours adopt — bring an existing codebase into the framework

This is the **only operation on existing code** in v4. There is no separate "productionize" verb — production-grade emerges from continuous ensemble play after adoption.

When this verb runs, the active team meets the codebase. Each role reads the relevant parts, roleplays its assessed level of involvement, and contributes a section to a consolidated adoption assessment. The conductor reviews, confirms, and the framework generates the v4 baseline artifacts (CLAUDE.md, AGENTS.md, NARRATIVE.md, STATE.md, HANDOFFS.yml, VOICE.md, plus first-impressions design docs from high-involvement roles).

**Team chat mode:** Adopt is the *meet the team* moment — chat mode is especially valuable here. Before producing any role-driven output, read `${CLAUDE_SKILL_DIR}/references/chat-format.md` and honor the current `team_chat` value from `~/.hacky-hours/settings.yml` (default `minimal`) throughout this verb. **No tokens for tokens' sake** — every voice turn must add information.

**Team learning capture:** Adopt is the full-team-meets-codebase moment — every role with non-N/A involvement participates. At the tail (Step 8 below), run **Stash** per `${CLAUDE_SKILL_DIR}/references/capture-format.md`: silent `history.md` append for each participating agent (one entry: "Met <project> at Tier <N>; recommended <involvement-level>"), then the one-line behavior-feedback prompt. This is the foundational history entry for the project on this team — every subsequent verb's history line gets read against this baseline.

---

## Step 0 — Pre-flight

1. **Global skeleton:** If `~/.hacky-hours/` doesn't exist → Read `tools/v4-first-run.md` first, then return here.
2. **Default team:** If `~/.hacky-hours/teams/default/` doesn't exist → Read `tools/team.md` and run the Default Team Bootstrap, then return here.
3. **In a project repo:** Confirm cwd has code (not an empty directory). Use `ls` + a quick file inventory. If empty: tell the user *"Adopt needs an existing codebase — there's nothing here yet. Want to start a new project with `/hacky-hours ideate` instead?"*
4. **Detect existing hacky-hours/ folder:**
   - **No `hacky-hours/` folder:** fresh adoption. Continue to Step 1.
   - **v3-shape `hacky-hours/` folder** (has `01-ideate/` etc. but no `NARRATIVE.md`): this is a v3 → v4 migration. Continue to Step 1 but note this — adoption will augment rather than replace.
   - **v4-shape `hacky-hours/` folder** (has `NARRATIVE.md`): re-adoption. Print *"This project already has v4 hacky-hours artifacts. Want to re-run adoption (will update artifacts but preserve your edits), or do you want a different verb (`audit` to re-evaluate, `ideate` to revisit product overview)?"*

## Step 1 — Orientation

Brief conversation, four questions, sensibly defaulted so non-engineers can run it in 90 seconds:

### Q1: What is this?

Read the codebase's README (if present) + top-level file structure. Synthesize a one-sentence guess at what the project is. Confirm with the user:

> *"Looks like this is [one-sentence summary]. Is that right? Anything you'd add?"*

### Q2: What tier of rigor?

Present the tier guide briefly:

> *"How serious is this project? This sets the rigor bar — every role calibrates to it.*
> *  1. **Tier 1 — Personal / Internal** — weekend tool, prototype, internal-only utility*
> *  2. **Tier 2 — Small team / business** — real users but small scale, no compliance scope*
> *  3. **Tier 3 — Customer-facing SaaS** — paying users, real availability needs, security stakes*
> *  4. **Tier 4 — Regulated / safety-critical** — healthcare, finance, compliance-bound*
>
> *Default recommendation based on what I see: [Tier X]. Confirm or override?"*

Base the recommendation on signals: presence of payment integrations → Tier 3, presence of user data → Tier 2+, presence of compliance keywords (HIPAA, SOC2, GDPR-specific) → Tier 4, single-user CLI → Tier 1.

### Q3: Voice mode

> *"Voice mode for this project? builder (plain language, outcome-framing) or engineer (precise vocabulary, terse)? Default from your settings: [builder | engineer]."*

Default to the user's `~/.hacky-hours/settings.yml` `voice_default`. One-word answer fine.

### Q4: Sensitive paths to deny

> *"Any paths the team shouldn't read directly (besides the framework defaults — .env*, .git internals, vendored deps, secret-pattern files)? Common additions: customer data fixtures, internal API keys committed to local-only files, etc."*

If user says "none" or "default": proceed with the framework defaults only.

## Step 2 — Team binding

1. Determine active team. If `AGENTS.md` exists in the project, read its `team:` field. Otherwise default to `default`.
2. Confirm: *"Engaging team `<name>` (`<tier-from-tier.yml>` tier, <count> agents). Want to switch teams? (e.g., `/hacky-hours team list` to see options.)"*
3. If user wants a different team, run `/hacky-hours team switch <name>` first.

## Step 3 — Role fan-out: each agent meets the code

This is the core of adoption. For each role in the active team's `tier.yml`, spawn a subagent with that role's system prompt and ask it to produce a structured involvement assessment.

### Parallelization

If the Agent tool is available in this environment: spawn the role-agents in parallel (up to 4 at a time to control concurrency). Each agent invocation gets:
- The role's `system-prompt.md` content as the agent's initial context
- A task prompt (see template below)
- Read-only access to the project codebase (respecting the denylist)

If Agent tool isn't available or fan-out isn't feasible: roleplay each role sequentially. The output is the same; only the wall-clock time differs.

### Per-role task prompt template

```
You are <Name> (the <Role> on this Hacky Hours team). Your system prompt is your full context for this work.

Your task right now: meet this codebase for the first time. Produce a structured *involvement assessment* — your honest read on:

1. What level of involvement this project needs from your discipline (Critical / High / Medium / Low / N/A) — calibrate to the project's tier.
2. Your initial findings — 3-7 specific observations about the codebase from your discipline's lens. Be honest. Cite specific file paths or line numbers where you can.
3. Your punch list — concrete things you'd want addressed, prioritized P0 / P1 / P2.
4. Any cross-role conflicts you anticipate (e.g., "security and FE will disagree about CSP strictness — we should arbitrate early").

Project context:
- Tier: <tier>
- Voice mode: <voice>
- Conductor's audience profile: <profile from settings.yml>
- Conductor's brief: <Q1 response>
- Denylist additions: <Q4 response>

Read the codebase using your discipline's lens. Skip files on the denylist (and surface that you skipped them). Produce your section in this exact format:

---

### <Role> — <Name>

**Recommended involvement:** <Critical | High | Medium | Low | N/A>

**Why:** <one-sentence justification calibrated to tier>

**Initial findings:**
- <Finding 1 with file:line reference>
- <Finding 2>
- ...

**Punch list:**
- **P0:** <Item> — <one-line rationale>
- **P1:** <Item>
- **P2:** <Item>

**Anticipated cross-role conflicts:**
- <If any; otherwise "None expected at this stage">

---

Keep it tight — under 400 words per section. Don't pad to seem thorough.
```

### Consolidation

After all roles return their sections:

1. Concatenate into `hacky-hours/adoption-assessment-<YYYY-MM-DD>.md` with this structure:

```markdown
# Adoption Assessment — <project name> — <date>

## Recommended Tier
<Tier confirmed in orientation, with one-paragraph consensus reasoning synthesized from role inputs>

## Per-Role Involvement Assessments

<Concatenated role sections from the fan-out, in this order:
1. Product
2. Design
3. Architect
4. Frontend
5. Backend
6. Security
7. Ops
8. QA
9. Accessibility
10. Licensing
11. Data
12. AI/ML
(or whatever the team's tier.yml ordering specifies)>

## Cross-Role Conflicts Surfaced
<Aggregated from each role's "Anticipated cross-role conflicts" section. If multiple roles flagged the same conflict, consolidate.>

## Conductor Decisions
*This section is for you, the conductor, to fill in.*

For each role, confirm or adjust the recommended involvement level. Optionally add notes:

- [ ] Product — Maya: <recommended level> → confirmed / adjusted to: ___
- [ ] Design — Felix: <recommended level> → confirmed / adjusted to: ___
- ...

Decisions on cross-role conflicts (if any):
- ___

## Next Steps After Conductor Confirms
1. High-involvement roles produce their first-impressions design docs
2. Framework generates baseline state files (NARRATIVE.md, STATE.md, HANDOFFS.yml, VOICE.md, AGENTS.md, CLAUDE.md)
3. Audit findings get queued into BACKLOG.md
4. Project is in the orchestra — every subsequent change goes through normal hacky-hours flow
```

2. Print the consolidated assessment to the conductor for review.

## Step 4 — Conductor review

Print:

> *"The team has met your codebase. Here's the consolidated assessment:*
> *[print full assessment]*
>
> *Take a moment to read through. When ready, tell me:*
> *  - **Confirm all** — I agree with all recommended involvement levels*
> *  - **Adjust** — I want to change some (tell me which roles + new levels)*
> *  - **Discuss** — pick a finding or conflict to dig into before deciding"*

Wait for explicit conductor input. Don't proceed to Step 5 without it.

When the conductor responds, update the "Conductor Decisions" section of the assessment file with their calls.

## Step 5 — Generate baseline v4 artifacts

Once the conductor has confirmed involvement levels, create the v4 baseline artifacts. Always create these files (creating, not overwriting — if a file exists, surface a diff and ask before changing):

### a) `<project>/CLAUDE.md`

If CLAUDE.md doesn't exist, create from the v4 schema (item 16 in V4_DESIGN.md):

```markdown
# CLAUDE.md

## 1. Project Tier
**Tier:** <tier from orientation> (<tier name>)
**Override reasoning:** <if override given, otherwise "Recommended tier accepted">

## 2. Active Team
**Team:** <active team name>
**Source:** ~/.hacky-hours/teams/<team-name>
**Framework version:** 4.0.0-dev

## 3. Voice & Style
**Mode:** <builder | engineer from orientation>
**Tone defaults:** See `hacky-hours/VOICE.md` for per-artifact-type preferences.

## 4. Role-Aware Guardrails

These are the rules the team will enforce. Every rule names its owning role + enforcement mechanism. Rules without enforcement are wishes — if no automation exists yet, mark "manual review only" honestly.

| Rule | Owning role | Enforcement |
|------|-------------|-------------|
| No secrets in code or commits | Security | TODO: add `.pre-commit/no-secrets.sh` |
| Inputs validated at trust boundaries | Security | TODO: add CI gate `scripts/check-validation.sh` |
| Color contrast ≥ 4.5:1 on text content | Accessibility | manual review only |
| <add as audit P0/M0 findings produce new guardrails> | | |

---
Subagent read denylist: see `hacky-hours/.hacky-hours-denylist` and `hacky-hours/.hacky-hours-denylist.local` (gitignored).
```

If CLAUDE.md exists: read it, propose a merge that adds the four sections without losing the user's existing content.

### b) `<project>/AGENTS.md`

Index of which team is bound to this project + which roles are present:

```markdown
# AGENTS.md

This project uses the Hacky Hours framework with a team of stakeholder-role AI agents.

## Active Team
**Team:** <team-name>
**Source:** ~/.hacky-hours/teams/<team-name>/  (also resolvable via git URL — see team's README)
**Framework version:** 4.0.0-dev

## Roster

| Role | Name | Hat(s) | Recommended involvement |
|------|------|--------|-------------------------|
| 📊 Product | Maya Tanaka | product | <confirmed level> |
| 🎨 Design | Felix Okafor | design | <confirmed level> |
| 🏗️ Architect | Priya Chen | architect | <confirmed level> |
| 🖥️ Frontend | Marcus Rivera | frontend | <confirmed level> |
| ⚙️ Backend | Sam Park | backend | <confirmed level> |
| 🛡️ Security | Alex Davies | security | <confirmed level> |
| 🚀 Ops | Jordan Kim | ops | <confirmed level> |
| 🔍 QA | Emma Wright | qa | <confirmed level> |
| ♿ A11y | Lena Mwangi | accessibility | <confirmed level> |
| 📜 Licensing | Diego Romano | licensing | <confirmed level> |
| 📈 Data | Yuki Nakamura | data | <confirmed level> |
| 🤖 AI/ML | Kai Patel | ai-ml | <confirmed level> |

## Owned Artifacts

Each role owns specific artifacts in this project — see their profile for the full list. Quick map:

- Product (Maya): `hacky-hours/01-ideate/PRODUCT_OVERVIEW.md`, `hacky-hours/03-roadmap/ROADMAP.md`
- Design (Felix): `hacky-hours/02-design/USER_JOURNEYS.md`, `hacky-hours/02-design/STYLE_GUIDE.md`
- Architect (Priya): `hacky-hours/02-design/ARCHITECTURE.md`, ADRs under `hacky-hours/02-design/decisions/`
- Security (Alex): `hacky-hours/02-design/SECURITY_PRIVACY.md`, security findings in `hacky-hours/audits/`
- A11y (Lena): `hacky-hours/02-design/ACCESSIBILITY.md`
- Licensing (Diego): `hacky-hours/02-design/LICENSING.md`
- QA (Emma): `hacky-hours/02-design/TESTING.md`
- Data (Yuki) + Backend (Sam) co-own: `hacky-hours/02-design/DATA_MODEL.md`
- Ops (Jordan): `hacky-hours/runbooks/`
- AI/ML (Kai): AI section of `hacky-hours/02-design/ARCHITECTURE.md`, eval strategy

## How to invoke a specific role

Call them by name or by hat:
- `/hacky-hours design architecture` — engages Architect
- `/hacky-hours audit` — fans out to Security, A11y, Ops, QA, Architect, plus doc-audit Claude
- `/hacky-hours team show <agent-id>` — view profile

See `~/.hacky-hours/teams/<team-name>/README.md` for the team's overall philosophy.
```

### c) `<project>/hacky-hours/NARRATIVE.md`

Living one-paragraph project summary:

```markdown
# Project Narrative

Adopted <date> at Tier <N>. <One paragraph from Step 1 Q1 — what the project is and why it exists.>

Last action: adoption complete; team meeting yielded <count> P0 findings, <count> P1, <count> P2. Next likely action: <recommendation based on findings — e.g., "address security P0s before any feature work" or "/hacky-hours design architecture to formalize ARCHITECTURE.md given Priya's flags">.
```

### d) `<project>/hacky-hours/STATE.md`

```yaml
# Project state — read by every role on entry
adopted: <date>
tier: <N>
voice_mode: <builder | engineer>
active_team: <team-name>
framework_version: 4.0.0-dev

last_action:
  verb: adopt
  date: <date>
  outcome: completed; adoption assessment at hacky-hours/adoption-assessment-<date>.md

pending_actions:
  - "Review P0 findings in adoption-assessment-<date>.md"
  - "Address [first P0] before further feature work"

blocked_on: []
```

### e) `<project>/hacky-hours/HANDOFFS.yml`

```yaml
# Open handoffs from one role/verb to another.
# Consumed when the target acts. Tools and roles check this on entry.

handoffs:
  - from: adopt
    to: audit
    reason: "Adoption surfaced P0/P1 findings — recommend full audit to triage before feature work."
    created: <date>
    expires: +7d
```

### f) `<project>/hacky-hours/VOICE.md`

```yaml
# Voice preferences per artifact type.
# Set during adoption based on conductor's chosen voice mode + any explicit preferences.

design_docs: formal-team
audit_reports: technical-handbook
user_journeys: casual-narrative
runbooks: technical-handbook
adrs: formal-team
ideation_docs: casual-narrative

# Conductor preferences:
tone: <builder | engineer from orientation>
verbosity: standard   # terse | standard | thorough
emoji_in_artifacts: false
```

### g) Denylist files

`<project>/hacky-hours/.hacky-hours-denylist`:
```
# Subagent read denylist — committed, public-safe entries.
# Framework defaults are always denied (.env*, .git internals, etc.). This file extends them.
# See V4_DESIGN.md §4.14 and §4.16 for the model.

<any glob patterns added from Q4>
```

`<project>/hacky-hours/.hacky-hours-denylist.local`:
```
# Sensitive denylist entries — git-ignored, never committed.
# Add specific paths or filenames you don't want subagents to read.
```

Add `hacky-hours/.hacky-hours-denylist.local` to `.gitignore` (create or extend).

## Step 6 — First-impressions design docs

For each role with **High** or **Critical** involvement (as confirmed by the conductor in Step 4), have the role produce their first-impressions design doc. These are the team's actual work product from meeting the codebase — not just an assessment, but the durable artifacts that make the project legible.

### Which docs from which roles

| Role | Doc produced (if High/Critical involvement) | Location |
|------|---------------------------------------------|----------|
| Product | `01-ideate/PRODUCT_OVERVIEW.md` | hacky-hours/01-ideate/ |
| Architect | `ARCHITECTURE.md` (two-tier: deep + summary, per v3 template) | hacky-hours/02-design/ |
| Security | `SECURITY_PRIVACY.md` (two-tier) | hacky-hours/02-design/ |
| Accessibility | `ACCESSIBILITY.md` (two-tier) | hacky-hours/02-design/ |
| Backend + Data (co-author) | `DATA_MODEL.md` | hacky-hours/02-design/ |
| Design | `USER_JOURNEYS.md`, `STYLE_GUIDE.md` (if UI exists) | hacky-hours/02-design/ |
| QA | `TESTING.md` | hacky-hours/02-design/ |
| Licensing | `LICENSING.md` | hacky-hours/02-design/ |
| Ops | runbooks for known failure modes | hacky-hours/runbooks/ |
| AI/ML | AI/ML section of ARCHITECTURE.md (or dedicated `AI_ML.md`) | hacky-hours/02-design/ |
| Frontend | FE section of ARCHITECTURE.md | hacky-hours/02-design/ |

Skip roles with **Medium**, **Low**, or **N/A** involvement — those docs come later when the team accumulates enough decisions in the discipline to justify them.

### Per-role generation prompt

For each High/Critical role, spawn or roleplay the agent with this task:

```
You are <Name> (<Role>). Your system prompt is your context.

Your task: write the first-impressions design doc you own for this project.

Doc to write: <doc name> at <path>
Project context:
  - Tier: <N>
  - Voice mode: <builder | engineer>
  - Voice template per VOICE.md: <relevant tone for this doc type>
  - Conductor's brief: <Q1 from orientation>
  - Existing assessment findings (your section): <quote your findings from the assessment>
  - Two-tier template guidance: <if applicable, read ${CLAUDE_SKILL_DIR}/templates/design/README.md for the deep + summary pattern>

Write in **team-grade voice**:
  - Declarative, not exploratory ("This system uses X" — not "We're thinking about X")
  - Include `owner:` and `last_reviewed:` frontmatter
  - Cross-reference related docs with relative-path links that work outside hacky-hours folder
  - Avoid framework jargon ("hacky-hours says...") — write as if a team member wrote this and committed it
  - Include "what this covers" and "what this doesn't" at the top — be honest about scope

The doc must be standalone-readable. If someone copy-pastes it into a Notion page, it should still make sense.

Cite specific file paths and line numbers where you reference code. Don't make up details — read the codebase as needed (respect the denylist).

Aim for thorough but not exhaustive. The doc should let a new contributor understand this dimension of the project in one sitting.
```

### Frontmatter template for every first-impressions doc

```yaml
---
owner: <agent-id>          # e.g., security-lead-alex
co_owners: []              # if multiple roles co-author
last_reviewed: <YYYY-MM-DD>
status: first-impressions  # → reviewed | living
tier: <N>
covers:
  - <thing 1>
  - <thing 2>
does_not_cover:
  - <out-of-scope item 1>
related_docs:
  - <path to related doc>
---
```

### Parallelization

If Agent tool is available: spawn first-impressions doc generation in parallel across roles (up to 4 concurrent). Doc generation per role takes longer than the assessment — token budget here is significant.

Otherwise: sequentially, in this order to respect dependencies:
1. Product (`PRODUCT_OVERVIEW.md` — anchors everything else)
2. Architect (`ARCHITECTURE.md` — needed by Security, Data, FE, BE, AI/ML)
3. Then in parallel: Security, A11y, Data/BE, Design, QA, Licensing, Ops, AI/ML, FE

### Budget warning

These docs are expensive. Surface budget before starting:

> *"Generating first-impressions design docs for <count> high-involvement roles. Estimated total: ~<estimate> tokens (your warn threshold: <warn>, hard cap: <hard>). Proceed?"*

Conductor can opt out and run them later on demand: *"defer all design docs → I'll generate them later with /hacky-hours design <topic>"*.

### v3 → v4 migration case

If the project has pre-existing v3 design docs at `hacky-hours/02-design/<DOC>.md`:
- **Don't overwrite.** Surface them to the conductor: *"You already have an ARCHITECTURE.md from earlier work. Want Priya to: (a) review and augment, (b) rewrite in v4 team-grade voice, (c) leave as-is and skip?"*
- Default to (c). v3 docs are existing work that may already be good.

### After generation

For each completed doc:
1. Write it to the target path
2. Add an entry to AGENTS.md "Owned Artifacts" section if not already there
3. Note in NARRATIVE.md that the doc was produced
4. Add a `HANDOFFS.yml` entry from the producing role to `/hacky-hours audit` recommending the doc be included in the next audit's doc-audit lane

## Step 7 — Wrap up

After Step 6 completes:

Print to conductor:

> *"Adoption complete. The team is in.*
>
> *Files created:*
> *  - `hacky-hours/adoption-assessment-<date>.md` — the team's first-impressions report*
> *  - `hacky-hours/NARRATIVE.md`, `STATE.md`, `HANDOFFS.yml`, `VOICE.md`*
> *  - `hacky-hours/.hacky-hours-denylist`, `.hacky-hours-denylist.local`*
> *  - `AGENTS.md` — team roster index*
> *  - `CLAUDE.md` — project tier + voice + guardrails*
> *  - <count> first-impressions design docs from high-involvement roles (listed above)*
>
> *Next suggested steps:*
> *  - `/hacky-hours audit` for a scorecard + doc-audit lane evaluating the new design docs*
> *  - Triage the P0s from the assessment*
> *  - `/hacky-hours team` to browse the roster*
> *  - `/hacky-hours team update` to promote any feedback you've given the agents during this session*"

## Step 8 — Stash (team learning)

Run per `${CLAUDE_SKILL_DIR}/references/capture-format.md`. Adoption is the foundational team-meets-project moment, so the history entries here are especially load-bearing — every subsequent verb's history line implicitly references this baseline.

1. List the agents that actually contributed to the assessment (skip any with N/A involvement).
2. Compose a one-sentence past-tense contribution summary per participant. Include the recommended involvement level: e.g., *"Met hacky-hours-docs at Tier 1; recommended High involvement; flagged 2 P0s on input validation in tools/issue.md and tools/team.md."* Concrete.
3. Resolve the session ID per the algorithm in `capture-format.md`.
4. **History append + metrics refresh (silent):** for each participant, append `- <date> · <project-slug> · adopt · <summary>` to `~/.hacky-hours/teams/<active>/agents/<agent-id>/history.md`. Then refresh the `metrics:` block in each participating agent's `profile.md` per `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Derived metrics" + §"Level derivation". Commit both files together: `git -C ~/.hacky-hours/teams/<active>/ add agents/*/history.md agents/*/profile.md && git commit -m "history: adopt @ <project> @ <date> — <N> agent(s)"`.
5. **Behavior feedback prompt:** ask the conductor *"Anything you said during adoption that should change how an agent works in future sessions? Free-form by agent, or `none`. (Common at adopt-time: 'be terser on this codebase' — it sets the rhythm for everything that follows.)"* For each agent named, write `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the schema.
6. **Footer:** print *"Stashed <N> behavior note(s) for <agents>. Appended adoption history to <count> agent(s) (commit <sha>). This is the project's foundational team-meets-project record — every subsequent verb's history line references it. Promote with `/hacky-hours team update` when ready."*

## Notes for the assistant running this

- **Roleplay vs fan-out:** Where the Agent tool is available, spawn each role as its own subagent for higher fidelity (true context isolation, no cross-contamination of disciplines). Where not, sequential roleplay produces identical artifacts.
- **Respect the denylist** at every step. Each role should declare what it skipped reading and surface it inline (see SKILL.md "Trust boundary surfacing UX").
- **Cost awareness:** Adoption with 12 parallel subagents is token-expensive. Check `~/.hacky-hours/settings.yml` for `session_budget_warn` and surface a budget bar to the conductor before fan-out begins:

  > *"This adoption will involve <count> role agents reading the codebase. Estimated cost: ~<estimate> tokens (your warn threshold is <warn>, hard cap <hard>). Proceed?"*

- **v3 → v4 migration case:** if the project has a v3-shape `hacky-hours/` folder, the adopt verb augments rather than replaces. Add NARRATIVE/STATE/HANDOFFS/VOICE; merge into existing CLAUDE.md; create AGENTS.md. Do not delete v3 design docs — they are the team's prior work, just in a v3 voice. The team can re-author them via subsequent `design` verbs.
- **Idempotency:** if the conductor re-runs adoption, treat existing artifacts as the source of truth and update only what's stale. Never silently overwrite the assessment file — write to a new date-stamped file.
