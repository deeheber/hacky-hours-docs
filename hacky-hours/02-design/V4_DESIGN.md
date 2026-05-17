# Hacky Hours v4.0.0 — Design Document

**Status:** Draft — 2026-05-13
**Branch:** `feat/v4.0.0`
**Prior version:** v3.0.0

---

## 1. Context — Why v4

v3 framed Hacky Hours as a *documentation framework for LLM-assisted app development*. In practice that framing leaked in three ways:

1. **The audience was aspirational.** "For everyone" didn't hold — non-engineers hit forms like `MARKET_FIT.md` and bounced.
2. **The dogfood loop underperformed.** Running hacky-hours on hacky-hours produced ideas, but the friction-to-framework-edit path was manual and lossy.
3. **`productionize-me` existed as a sibling skill** that did things hacky-hours should have done natively (tier calibration, enforceable rules, real scaffolding, retrospective design docs).

v4 reframes the project around what it actually is and what it's becoming.

---

## 2. The Thesis

**Hacky Hours is a competence prosthesis.** It gives any one person — non-engineer or engineer — the ability to build software at the standard a great software team would produce, with the confidence that the dimensions they couldn't personally cover are being covered, and producing artifacts that can graduate to a real team when the time comes.

Two user value propositions, same underlying machinery:

- **Non-engineer:** *"I can build something real, without being intimidated. I can have the conversation with anyone — a security expert, a designer, an architect — because the framework has done the homework I couldn't."*
- **Engineer:** *"I trust this because I know what good looks like. The conventions I know matter but can't personally cover — accessibility, security review, observability, ops — are being attended to. This extends my reach."*

The framework adapts: it stands in for *more* of the process for someone without the background, *less* for someone with it, and steps aside entirely if a team chooses to. **The output is always team-grade, and the artifacts can leave home** (graduate to a team's knowledge base).

**Two-sentence version:** Hacky Hours is what LLM-assisted development looks like when you treat the LLM as one section of an orchestra rather than the whole show — small tools that each do one thing well, share a score, and listen to each other. The user is the conductor; the framework is the music stand; the documentation is the orchestral memory; and the bet is that an ensemble like this can improve itself by playing.

---

## 3. Architectural Foundations

### 3.1 The orchestra metaphor — sections are stakeholders, not tools

The sections of the orchestra are **stakeholder roles** — product, design, architect, FE, BE, security, ops, QA, a11y, licensing, Data, AI/ML. Each role is embodied as a subagent. The verbs (`ideate`, `design`, `audit`, `implement`, `ship`, etc.) are *performances* that fan out to the relevant sections in parallel or sequence them when dependent.

The conductor (user) directs gesturally; the orchestra plays.

### 3.2 Production-grade is emergent, not a destination

There is no `productionize` verb in v4. Production-grade emerges from the ensemble being continuously present — stakeholders attending to their concerns throughout the lifecycle, from `ideate` onward. The preflight isn't preflight — it's the work, ongoing.

The only operation on existing code is **`adopt`**: the orchestra meets the codebase, each role roleplays its assessed level of involvement, and from then on the project is just a hacky-hours project. `productionize-me` as a standalone skill dissolves into v4 entirely.

### 3.3 The team is a portable first-class asset

The user's team is **a separate maintained repo**, parallel to projects — *never* baked into any project's codebase or context files. Teams are an *applied layer*: projects bind to a team by reference. Users can build/maintain different teams for different cost/size/context profiles and slot them into projects. The team is `yours`; projects rent it.

### 3.4 Self-improvement via dogfood, not synthetic eval

Improvements to v4 come from running v4 on real work (including on the framework itself). Friction is captured per-tool, per-seam, and per-role. A meta-tool clusters lived friction into framework patches. The improvement loop is local, opt-in, and human-reviewed end to end.

---

## 4. The 20 Locked Decisions

### 4.1 Audit verb full spec
`/hacky-hours audit` runs three parallel lanes:
- **(a) Role-driven codebase audit** — security, a11y, ops, QA, architect read the code and flag
- **(b) Doc audit** — context-free Claude session reads only `hacky-hours/docs/` and answers structured questions about clarity/completeness
- **(c) Cross-reference integrity** — broken links, stale paths, contradictions between docs

Single consolidated report at `hacky-hours/audits/<date>.md`. Includes a **scorecard system with points and traffic light** (🟢/🟡/🔴 per dimension, numerical score aggregate, at-a-glance section). Codebase findings P0/P1/P2; doc findings clarity-scored; cross-ref findings broken-link list.

### 4.2 Verb-role matrix
Each verb fans out to a defined set of roles. Lives in `references/verb-role-matrix.md`. Team-tier configurations override.

Starting matrix:
- `ideate` → product (lead), customer voice, optionally SME
- `design <topic>` → architect (lead) + the role(s) the topic touches
- `audit` → security, a11y, ops, QA, architect, plus doc-audit Claude
- `implement` → BE or FE (lead) + security/a11y/QA as reviewers
- `ship` → ops (lead) + security + QA signoff
- `productionize` → **deleted** (replaced by `adopt` + continuous play)

### 4.3 Cost tracking & budget warnings
`~/.hacky-hours/settings.yml` carries:
- `session_budget_warn: 50000` (soft warn at this token count)
- `session_budget_hard: 200000` (hard stop; require confirmation)

Framework tracks running total across subagent invocations. Surfaces budget bar at end of each verb. Pauses for confirmation before any fan-out that would push past the warn threshold.

### 4.4 Customization promote flow
User customizations to subagent prompts are **pending changes to the team repo**, not a parallel layer. Team repo is always the canonical source of truth.

Flow:
1. **Capture** — during a session, behavior feedback or direct prompt edits are recorded as pending in `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md`
2. **Update** (`/hacky-hours team update`) — framework summarizes pending changes, conductor reviews each, accepts/rejects/edits
3. **Commit** — accepted changes applied to agent files, framework creates a git commit in the team repo, asks before pushing
4. **Clear** — all pending entries (accepted *and* rejected) removed after resolution. No way to accidentally re-promote.

Multi-session race handled at promote step (second to update sees merge prompt). Framework-update conflicts with team agents handled by team-version compatibility check.

### 4.5 Subagent file format
Each agent in a team repo at `~/.hacky-hours/teams/<team>/agents/<agent-id>/`:
- `profile.md` — background, name, role assignments, voice baseline, quirks
- `system-prompt.md` — actual system prompt sent to subagent at invocation
- `history.md` — resume-style summary across projects (compacted over time)
- `feedback.md` — durable conductor feedback absorbed
- `preferences.yml` — model preference, fluency adapters, etc.

`<agent-id>` is stable kebab-case (e.g., `security-lead-alex`); projects reference by this ID so renames don't break bindings.

### 4.6 Multiplexed agent design
For team tiers where one agent wears multiple hats:
- **Single system prompt** declaring role coverage: *"You are Alex, principal engineer. You wear these hats: frontend, backend, data, ML, QA. When asked about each, respond as a senior practitioner of that discipline."*
- **Per-invocation hat cue** from framework: *"You're being called in your security-reviewer hat for this audit."*
- Agent's `profile.md` lists `hats: [...]`; framework checks before routing
- Pattern documented in `references/multiplexed-agents.md` with reference implementation

### 4.7 Team-binding mechanics
Project's `AGENTS.md` declares team binding:
- `team: lean-startup` (local name resolved against `~/.hacky-hours/teams/`)
- **or** `team: git@github.com:user/my-team.git` (URL for portability)

Resolution order: local name first, git URL fallback. Unavailable team triggers explicit warning, offers default team for the session, never silently substitutes. v4.0.0 supports **one active team per project**.

### 4.8 Team repo file structure
```
~/.hacky-hours/teams/<team>/        ← its own git repo (local-only default, GitHub-friendly remote)
├── README.md              ← frontmatter + team description, philosophy, tier
├── VERSION                ← framework version this team built against
├── LICENSE                ← user's choice; "private" by default
├── tier.yml               ← team-size tier, roles present, multiplexing config
├── agents/
│   ├── security-lead-alex/
│   │   ├── profile.md     ← YAML frontmatter for SSG rendering
│   │   ├── system-prompt.md
│   │   ├── history.md
│   │   ├── history-archive/
│   │   ├── feedback.md
│   │   └── preferences.yml
│   └── ...
├── site/                  ← optional Astro template (shipped by framework)
└── docs/                  ← static site build output for GitHub Pages
```

**Static site rendering:**
- Markdown + YAML frontmatter directly consumed by an Astro template (shipped with framework)
- `profile.md` frontmatter: `id`, `name`, `pronouns`, `hats`, `tagline`, `avatar` (emoji or path), `joined`, `specialties`, `projects`
- Three modes: localhost dev server, file:// static (relative URLs, double-click index.html works), GitHub Pages
- Privacy gate before publish; per-field `published: true/false` flag for sensitive entries
- Default emoji avatars per role (🛡️ security, 🎨 design, 📊 product, 🏗️ architect, etc.)

### 4.9 History compaction
- **Trigger:** history file exceeds threshold (~500 lines or ~10k tokens; user-tunable in `settings.yml`)
- **Mechanism:** framework summarizes older entries into a "key facts and patterns" section at top; archives raw history to `agents/<id>/history-archive/<date>.md`
- **Result:** current detail + condensed past; site renders as "Recent Activity" + "Track Record"
- **Backstop:** git history of the team repo preserves all prior versions

### 4.10 Adoption involvement-assessment artifact
When `/hacky-hours adopt` runs on existing code, all team roles fan out to assess. Each writes their section into one consolidated markdown file:

```markdown
# Adoption Assessment — [project] — [date]

## Recommended Tier
[Consensus reasoning from team]

## Per-Role Involvement
### Product
**Recommended involvement:** High
**Why:** ...
**Initial findings:** ...
**Punch list:** ...

### Security
**Recommended involvement:** Critical
...

(continues for every role in the active team)

## Cross-Role Conflicts
[Where roles disagree]

## Conductor Decisions
[Empty section conductor fills in]
```

Roles write sections in parallel. Conductor reviews top-to-bottom, fills in decisions. Adoption proceeds.

### 4.11 Conductor arbitration modes
Three named patterns:
- **`/hacky-hours arbitrate watch <topic>`** — agents converse with each other, transcript visible to conductor, ends on convergence or conductor interrupt. Higher cost.
- **`/hacky-hours arbitrate resolve <topic>`** — conductor states concerns; framework asks each role to propose resolution; conductor picks. Medium cost.
- **`/hacky-hours arbitrate decide <topic>`** — framework summarizes positions concisely; conductor decides directly. Cheapest.

**Default** when conflicts surface mid-verb: `decide`. Conductor escalates as needed. All three produce an ADR in `hacky-hours/02-design/decisions/` once resolved.

### 4.12 SME instantiation flow
During `/hacky-hours ideate`, after PRODUCT_OVERVIEW is drafted, product role asks:

> *"This project sits in [inferred domain]. Want an SME voice involved? Options: (a) external SME — I'll simulate a domain expert for this project, (b) you're the SME — I'll record that and defer to you on domain questions, (c) skip."*

- **(a)** Framework summons project-scoped SME role; recorded in PRODUCT_OVERVIEW + AGENTS.md
- **(b)** Recorded as `sme: conductor` in PRODUCT_OVERVIEW; framework defers
- **(c)** No SME; framework flags later if domain-sensitive questions arise

Teams with permanent SMEs (e.g., healthcare-focused team with embedded medical SME) spec this in `tier.yml` and skip the per-project question.

### 4.13 Voice template creation conversation
First time an artifact type is created in a project, the responsible role asks:

> *"For your design docs in this project — quick voice check. What tone fits: formal-team (declarative, owners, signoff-ready), casual-narrative (story-style, conversational), or technical-handbook (terse, spec-style)? Any structural preferences (length, headings, examples)?"*

Result persisted to `hacky-hours/VOICE.md`, keyed by artifact type:
```yaml
design_docs: formal-team
audit_reports: technical-handbook
user_journeys: casual-narrative
```

Subsequent artifacts inherit. New types ask fresh. Conductor can edit VOICE.md anytime.

### 4.14 Trust boundary surfacing UX
When subagents encounter denylist paths: **inline surfacing, not batched**.

Framework prepends one line to next conductor-facing message:

> *"⚠️ Noticed `.env.production` and `secrets/auth.key`, didn't read — confirm or describe contents if I need them."*

Conductor can answer in same turn, describe inline, override for session, or add to project denylist permanently. Multiple boundary hits coalesced into one ⚠️ line.

### 4.15 Folder structure under v4.0.0
Keep v3's phase-organized artifact layout in each project. Add v4-specific files:

```
<project>/
├── hacky-hours/
│   ├── 01-ideate/, 02-design/, 03-roadmap/, 04-build/, 05-iterate/
│   ├── audits/
│   ├── adoption-assessment-<date>.md
│   ├── NARRATIVE.md          ← new in v4: living one-paragraph
│   ├── STATE.md              ← new in v4: phase + last action
│   ├── HANDOFFS.yml          ← new in v4: pending role-to-role
│   ├── VOICE.md              ← new in v4: voice prefs per artifact type
│   ├── docs/                 ← new in v4: team-grade exports for graduation
│   ├── .hacky-hours-denylist
│   └── .hacky-hours-denylist.local
├── AGENTS.md                 ← new in v4: team binding + role roster index
└── CLAUDE.md                 ← project rules + tier + voice + guardrails
```

Phase-organized stays for migration ease. AGENTS.md indexes by role. Role-organized views are virtual (rendered by `/hacky-hours team` or static site).

`docs/` lives inside `hacky-hours/` (not at project root) to avoid collision with existing repo `docs/` conventions. Configurable override available.

### 4.16 CLAUDE.md schema for v4
Four required sections — denylist split out to its own files:

```markdown
# CLAUDE.md

## 1. Project Tier
**Tier:** 2 (Small team / business)
**Override reasoning:** [if tier was overridden]

## 2. Active Team
**Team:** lean-startup
**Source:** ~/.hacky-hours/teams/lean-startup
**Framework version:** 4.0.0

## 3. Voice & Style
**Mode:** builder
**Tone defaults:** [summary of VOICE.md for LLM context]

## 4. Role-Aware Guardrails
| Rule | Owning role | Enforcement |
|------|-------------|-------------|
| No secrets in code | Security | `.pre-commit/no-secrets.sh` |
| Inputs validated at boundaries | Security | CI gate `scripts/check-validation.sh` |
| Color contrast ≥ 4.5:1 | A11y | manual review |
| ... | ... | ... |

Every guardrail names its owning role + enforcement mechanism (or honest "manual review only" note).

---
Subagent read denylist: see `hacky-hours/.hacky-hours-denylist` and `hacky-hours/.hacky-hours-denylist.local`.
```

Denylist split:
- `hacky-hours/.hacky-hours-denylist` — committed, glob patterns, public-safe
- `hacky-hours/.hacky-hours-denylist.local` — gitignored, sensitive specifics

### 4.17 Invocation policy / SKILL.md description
Reverse v3's `disable-model-invocation: true`. Re-enable context-driven invocation with invitation pattern.

**Description language fires on:** "build me an app/tool/site," "I have an idea," "help me design/architect," "harden this codebase," "audit this," "is this production-grade," "we're shipping," "draft an architecture diagram," "vibe-coded this and want to ship."

**Doesn't fire on:** typo fixes, single-file scripts, "explain this function," tactical one-off code asks.

**Invitation pattern:**
> *"This sounds like a build-a-real-thing moment. Hacky Hours is designed for this — want me to engage the full team (product, design, security, ops, QA, a11y, etc.) so we can do this with the right rigor for your tier? Or just sketch informally first?"*

Two-tier matching: light scan recognizes territory + surfaces invitation; full engagement after explicit confirmation. **Never auto-enters.**

Exact description text is a v4.0.0 deliverable; iterate with real prompts to verify fire-on-relevant / silent-on-noise.

### 4.18 License declarations in user-created content
- **Team repo** (standalone in `~/.hacky-hours/teams/<team>/`): framework drops `LICENSE` file, default private; user edits to override
- **Project's `hacky-hours/` folder** (inside code repo): **no new LICENSE**; inherits the parent project's license
- **Framework code**: MIT in empathetech repo
- **Meta-tool feedback upstream**: explicit permission per submission via `/hacky-hours issue`

Default team LICENSE content:
```
Private — © <user>, all rights reserved.

This content was generated using the Hacky Hours framework, which is open-source
under the MIT license. The framework code is open; this content is not.

To change this license (e.g., to open-source this team), edit this file.
```

### 4.19 Tooling UX commands
- `/hacky-hours team` — list/switch/view/edit team and agents
- `/hacky-hours team update` — push session pending changes into team repo (renamed from "promote")
- `/hacky-hours team site [serve|build|publish]` — three site modes
- `/hacky-hours feedback` — local-only session friction capture
- `/hacky-hours issue` — opt-in GitHub issue upstream to empathetech
- `/hacky-hours changelog` — full viewer + auto-digest on first run after update
- `/hacky-hours update` — framework update from inside Claude Code
- `/hacky-hours rollback` — restore previous framework version
- `/hacky-hours export <target>` — v4.0.0 ships Google Docs + static site
- `/hacky-hours meta` — cluster feedback → framework patches
- `/hacky-hours arbitrate <mode> <topic>` — three arbitration modes
- `/hacky-hours team chat <off | minimal | full>` — set closed-captioned multi-agent dialogue mode (see §4.20)

### 4.20 Team chat — tiered closed-captioned multi-agent dialogue

The orchestra metaphor is the thesis of v4. Without visible team presence, the framework reads as a smarter single-narrator assistant. Chat mode makes the orchestra audible — tiered so the user can choose how much of it to hear at what cost.

**Command:** `/hacky-hours team chat <off | minimal | full>` (default: `minimal`).

**The three modes:**

| Mode | What surfaces |
|------|---------------|
| `off` | Single narrator. The assistant speaks for the team. Current pre-v4 behavior. |
| `minimal` | Speaker attribution at **meaningful moments only**: a role introducing a concern not yet on the table, two roles disagreeing on a recommendation, control handing off between roles. One header per moment; content flows from there. No empty acknowledgments. |
| `full` | Closed-captioned multi-agent dialogue. Per-role fan-out, side chatter visible, mid-stride observations, hand-off conversations rendered as turns. Distinct voices in each agent's `profile.md` baseline. |

**On cost:** `minimal` and `full` cost meaningfully more tokens than `off` — `full` substantially more, because per-role fan-out genuinely happens. The framework deliberately does **not** print upfront cost estimates. Honest reasons: we don't have per-verb calibration data yet, Anthropic doesn't publish a tier → token-envelope mapping precisely, and skills running inside Claude Code have no API access to the user's current `/usage`. Any preflight number would be folklore. The existing `session_budget_warn` from §4.3 still applies — it fires on **actual** consumption, no estimation needed. A future slice (v4.1+) may calibrate per-verb baselines from accumulated session data and revisit upfront surfacing.

**Format (`minimal` and `full`):** canonical role emoji (from §5 roster) + bold `Name (Role) [HH:MM]` header, content on the next line.

```
🛡️ **Sam (Security) [14:32]**
PII colocated with auth state in the user table. Workable, but the blast radius
if leaked is larger than it needs to be.

🏗️ **Alex (Architect) [14:33]**
What's the alternative cost? Splitting means a join on every auth check.

🛡️ **Sam (Security) [14:34]**
Sensitive data behind an encryption layer. Auth doesn't need it — only profile
reads do. Join cost lands on profile, not the hot path.

🏗️ **Alex (Architect) [14:34]**
Fair. Redrawing the data model.
```

**The hard rule — no tokens for tokens' sake.** *Every voice turn must add information the conductor needs* — a reasoning step, a tradeoff, a concern, a hand-off, a mid-stride observation. Forbidden:
- Empty acknowledgments ("Got it." "Sounds good.")
- Filler agreement without addition ("I agree with Maya." with nothing after)
- Manufactured disagreement that doesn't reflect actual per-role reasoning
- Restating what another role just said in different words

This rule applies to all modes. In `full` mode it's load-bearing — the cost premium buys depth, not theater. If a role has nothing substantive to add at a moment, they don't speak.

**Real dialogue, not theater.** Speaking turns reflect *actual* per-role reasoning fan-out, not a single voice dressing up its output in name tags. When chat mode is `minimal` or `full`, the verb's role fan-out must genuinely happen and the captured per-role reasoning is what gets rendered. Voices should be recognizable from tone alone (Alex's terse architectural framing vs Maya's product-discovery questioning vs Sam's risk-first lens) before reading the speaker tag.

**Cadence:** semi-regular at meaningful moments — entering a step, surfacing a tradeoff, mid-stride observation worth seeing, hand-off to another role, finishing a piece. Not every sentence.

**Persistence:** the mode lives in `~/.hacky-hours/settings.yml` as `team_chat: off | minimal | full`. Persists across sessions. Per-session override via `/hacky-hours team chat <mode>`; never silently changed.

**Verb compatibility:** chat mode applies to verbs that fan out to multiple roles (`ideate`, `design`, `audit`, `adopt`, `arbitrate`, `implement`, `ship`). Single-role verbs (`feedback`, `issue`, `team`, `meta`) are unaffected — they run as before regardless of mode.

**Default-minimal rationale.** The thesis of v4 is "working with a team," not "working with a smarter assistant who can be configured to act like a team." Default-`off` would hide the headline change of the major version behind a flag most users won't find. Default-`full` would surprise users with the largest cost premium on first run. `minimal` is the middle path: the team is audibly present at meaningful moments, the cost premium is the smallest of the visible modes, and the user can dial up to `full` or down to `off` per session as needed.

**v4.0.0 deliverable.** This is part of the v4.0.0 release, not a follow-on. Shipping v4 without it underdelivers on the orchestra thesis.

---

## 5. The Role Roster (Core 12)

Ships in v4.0.0. Extensibility model for additional roles (e.g., DBA, Mobile, Performance Eng) deferred to v4.1+.

| Role | Owns | Default emoji |
|------|------|---------------|
| Product | user value, business outcomes, scope, priorities | 📊 |
| Design / UX | user journeys, flows, IA, style | 🎨 |
| Architect | system design, ADRs, cross-cutting concerns | 🏗️ |
| Frontend Eng | components, state, perf, browser support | 🖥️ |
| Backend Eng | APIs, data model, scalability, reliability | ⚙️ |
| Security Eng | threat model, secrets, auth, compliance | 🛡️ |
| Ops / SRE | deployment, observability, runbooks, incidents | 🚀 |
| QA | test strategy, edge cases, regression risk | 🔍 |
| Accessibility | WCAG, keyboard nav, semantic HTML, contrast | ♿ |
| Licensing / Legal | license compatibility, data privacy compliance | 📜 |
| Data | data eng, pipelines, schemas, analytics | 📈 |
| AI/ML | model selection, prompt eng, eval, safety | 🤖 |

Plus configurable **SMEs** (project-scoped or team-embedded) and **Customer Voice** (advocacy from the demand side).

**Team-size tiering with role multiplexing:**

| Tier | Roster shape | Use case |
|------|--------------|----------|
| Solo | 1 polymath engineer + product + design (light) | Single-person project, prototype, weekend tool |
| Lean | 1 engineering agent + product + design + security (light) + ops (light) | Solo-toward-team, side project getting real |
| Startup | 3-4 engineering agents (FE+BE merged, Data+ML merged) + product + design + security + ops + QA | Small team, MVP-to-traction |
| Full | 12 specialists as above | Mature product, regulated domain, larger team |

---

## 6. Operations & State Files

### NARRATIVE.md
Living one-paragraph project summary. Every role updates with one sentence on each run describing what they did and what they expect next. Other roles read it before acting. The orchestra's score. Compacts when it grows past a paragraph (older content → `NARRATIVE_LOG.md`).

### STATE.md
Current phase, last completed step, who acted last, what's pending, what's blocked. Short, machine-readable-ish. Used for resume detection and conductor's score view.

### HANDOFFS.yml
Structured open invitations from one role/verb to another. Each: `from`, `to`, `reason`, `expires`, optional `payload`. Consumed when target acts. Enables listening, not just file sharing.

### AGENTS.md
Documents the role roster for this project. Indexes by role; points to which docs each role owns. Lists the bound team and version. Auto-generated as part of `adopt` or `ideate`. **Distinct from CLAUDE.md** — CLAUDE.md is the project's rulebook; AGENTS.md is the team org chart.

### settings.yml (`~/.hacky-hours/settings.yml`)
User-level global preferences:
```yaml
# Budgets
session_budget_warn: 50000
session_budget_hard: 200000

# Models (per-role overrides for cost optimization)
default_model: claude-opus-4-7
role_models:
  licensing: claude-haiku-4-5

# Voice defaults (baseline; per-project VOICE.md overrides)
voice_default: builder

# About-the-user (informs audience adaptation)
profile:
  technical_background: non_engineer
  role_fluency:
    security: novice
    product: expert

# Privacy
share_feedback_with_empathetech: false
auto_update_check: false
```

---

## 7. Update Flow

**Strict separation of framework code from user content.** Updates touch only the framework.

**Layout discipline:**
```
~/.claude/skills/hacky-hours/    ← framework code (UPDATE OVERWRITES)
~/.hacky-hours/
├── version                       ← installed version
├── settings.yml                  ← user preferences
├── feedback/                     ← local feedback corpus
├── teams/                        ← user-owned, never touched by update
├── sessions/                     ← transient session state
└── versions/                     ← prior framework versions for rollback
```

**Semver contracts:**
- **PATCH** (4.0.0 → 4.0.1): bug fixes only, no schema or behavior change, always safe
- **MINOR** (4.0.x → 4.1.0): additive only, new roles/verbs/exporters, existing user content stays valid
- **MAJOR** (4.x.x → 5.0.0): breaking allowed, required migration script, explicit user opt-in

**On update:**
- Changelog digest shown on first invocation after update (one-time per version, skippable)
- Customizations preserved via `customizations/<role>.md.patch` (but per item 4.4, promoted changes land in agent files directly)
- Pinning per project supported (`.hacky-hours-version`)
- Rollback via `~/.hacky-hours/versions/`
- Audit log of updates kept locally
- Never auto-update — always explicit user action

---

## 8. What's Deferred to v4.1+

- Team marketplace / shared starter teams published by empathetech
- Multi-team-per-project binding (escalate to bigger team for audits)
- Notion / Confluence exporters (v4.0.0 ships Google Docs + static site only)
- Cross-language / i18n
- Multi-user collaboration on shared teams
- Extension model for additional role types (DBA, Mobile, Performance Eng, etc.)
- "Defer" option in promote flow (v4.0.0 only supports accept-or-discard)

---

## 9. Implementation Kickoff Order

Before any user-visible change, ground these six foundations:

1. **Pick subagent file format concretely** — write one reference agent end-to-end. Recommend **security**, as it's the highest-stakes role for the thesis and most demonstrable.
2. **Specify shared schemas as actual file shapes** — NARRATIVE.md, STATE.md, HANDOFFS.yml, AGENTS.md, CLAUDE.md (v4 schema), with reference examples.
3. **Build the team-repo skeleton** — `~/.hacky-hours/teams/default/` with one starter team, plus the binding mechanic on the project side.
4. **Reverse the invocation policy in SKILL.md** — implement the invitation pattern, verify on a few realistic prompts.
5. **Spec the adoption flow** — the involvement-assessment artifact format, exact prompts each role uses on first contact.
6. **Wire the Astro static site template** — the team-browser surface that makes the persistent-team thesis tangible.

After these, the verb implementations and role-role coordination flow naturally.

---

## 10. Risks Being Held Consciously

- **Two audiences, one product.** Most products serving "complete beginner" and "expert" end up serving neither well. The voice/audience-adapter machinery must actually deliver in turn one, not be configured at a depth users never reach.
- **Role roster will want to grow.** Resist adding roles beyond the core 12 in v4.0.0. Extensibility model is the release valve.
- **Team history can become noise.** Compaction is mandatory; without it, agent files bloat and lose their resume-like utility.
- **The graduation property is testable, and you'll be tested on it.** The first team that picks up a hacky-hours project and rejects the docs is existential. The fresh-context Claude audit lane gives us a self-administered version of this test that doesn't require human reviewers.
- **The "conductor arbitrates flexibly" pattern is powerful but advanced.** Default to the cheapest (`decide`) so first-time users aren't paralyzed.
- **Cost of fan-out adoption** on a non-trivial codebase. Team-tier multiplexing addresses much of this; per-role model overrides in `settings.yml` cover the rest.
- **Two update loops in tension** (local meta-tool patches vs upstream framework changes). Resolved structurally: promoted changes live in the team repo, not as customization patches against framework prompts.

---

## 11. The Bet

Hacky Hours v4 is making a specific, falsifiable bet: that an orchestra of stakeholder-role subagents, conducted by one person, can produce software at team-grade quality, with documentation that graduates cleanly to a real team, and that the framework itself can improve by being used. If that bet is wrong, the symptoms will be: docs that real teams reject, non-engineers who can't make decisions through the framework, or an improvement loop that doesn't compound across sessions.

The validation surface is built in:
- The fresh-context Claude audit lane tests graduation continuously
- The meta-tool surfaces friction patterns from real sessions
- The static site and `/hacky-hours team` make the team's improvement visible
- Dogfooding on hacky-hours-docs itself is the highest-stakes test of the bet

---

## 12. Reference Documents

- `references/verb-role-matrix.md` — which roles fire for which verbs (per team tier)
- `references/multiplexed-agents.md` — pattern for one-agent-many-hats
- `references/audit-protocol.md` — the three-lane audit including doc-audit Claude session
- `references/stranger-audit-protocol.md` — exact prompts and input bundle for fresh-context Claude doc audit
- `references/team-tiers.md` — Solo / Lean / Startup / Full roster shapes
- `references/static-site-template.md` — Astro template, frontmatter conventions, three render modes
- `references/migration-v3-to-v4.md` — additive migration story from v3.0.0
- `references/role-defaults/<role>.md` — default system prompt per role, MIT-licensed

These references are the v4.0.0 deliverable scope alongside SKILL.md.
