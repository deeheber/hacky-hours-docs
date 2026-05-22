# CHANGELOG

All notable changes to hacky-hours-docs are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] — v4.1 cycle (in progress)

v4.1 work lands on `main` behind feature flags (default-off). v4.1.0 release will flip stable defaults to `true`. v4.0.x patches (e.g., HF1, HF2) ship freely during the v4.1 cycle. Release strategy: trunk-based development with feature flags — see ADR `hacky-hours/02-design/decisions/2026-05-22-feature-flag-layer.md`.

### Added — v4.1 Tier 1 (T1.5: plan-aware defaults wiring, 2026-05-22)

- **Cost preflight on heavy verbs.** `adopt`, `audit`, `team reflect --all`, and `team backfill` now surface a token estimate before fanning out across roles, with **Proceed** / **Downshift** / **Cancel** options. Pattern documented in new `references/cost-preflight.md`.
- **Plan-aware preflight rules.** Fires always on `plan: pro` or `unspecified`. Fires on Max plans only when the estimate exceeds 50K input tokens (with `audit` always crossing that threshold).
- **Per-verb downshift profiles** documented inline in each heavy verb's skill file — `adopt` skips the involvement-assessment artifact + Haiku for cheap roles; `audit` runs Lane A only with top 3 roles; `team reflect --all` processes agents sequentially; `team backfill` uses file-path classification only.
- **README updated** to describe v4 + v4.1 plan-aware defaults, the current install layout, and the persistent-team orchestra (the v4 thesis was missing from README).

Note: graceful degradation under `session_budget_hard` pressure is documented but not enforced until F2 (token instrumentation) lands. Cost estimates are observation-based until R1 (benchmarks) publishes real numbers.

### Added — v4.1 Tier 0 (F1: feature-flag layer foundation, 2026-05-22)

- **`features:` block in seeded `~/.hacky-hours/settings.yml`** (via `tools/v4-first-run.md` Step 4). 11 flags covering v4.1 Tier 1 / Tier 2 / Tier 3 mechanisms — all default `false`.
- **`profile.plan` schema** added to settings.yml. Values: `pro | max5x | max20x | unspecified`. Seeded as `unspecified` by default; `tools/v4-first-run.md` Step 5 now asks the plan question and seeds plan-aware role-model overrides accordingly (Haiku for `licensing` + `accessibility` on Pro).
- **`workroom_max_turns` and `workroom_role_budget`** settings added (defaults 24 and 2000). Consumed by T2.1 when it lands.
- **`references/feature-flag-loader.md`** new — canonical pattern for verbs that gate behavior on a flag. Documents the fallback discipline ("absence ≡ false; v4.0.x fallback must keep working").
- **Documents the flag list** in one place (the new reference's flag-table). Tier 1/2/3 PRs add their flags as they land; v4.1.0 release flips stable defaults to `true`.

This PR doesn't wire any verb to use a flag yet. F1 establishes the infrastructure; T1.1–T3.9 each consume it.

---

## [4.0.1] — 2026-05-22

### Fixed

- **Multi-role verbs now bootstrap the default team on first use** (#7). Steps 1–5, `reviews/audit`, and `tools/arbitrate` previously assumed `~/.hacky-hours/teams/default/` existed and crashed when first-time v4 users (who'd just completed `tools/v4-first-run.md`) ran a step verb before `adopt` or `team`. The two-step pre-flight (skeleton + default team) is now centralized in `references/team-preflight.md` and included from every multi-role verb. `tools/adopt.md`'s inline guard is refactored to use the same reference, so there's one source of truth.

---

## [4.0.0] — 2026-05-17

**v4.0.0 — orchestra of stakeholder-role AI agents.** Reframes hacky-hours as a *competence prosthesis* — an orchestra of stakeholder-role AI agents (product, design, architect, FE, BE, security, ops, QA, a11y, licensing, Data, AI/ML) so one person can build software at team-grade and graduate the work to a real team. Replaces v3's "documentation framework for LLM-assisted app development" framing.

Thesis-complete shipment: Slice 11 (orchestra audible) + Slice 12 (orchestra remembers) + Slice 13 (orchestra visible). See `hacky-hours/02-design/V4_DESIGN.md` for the full design.

### Added (Slice 1 — v4 foundation)

- **v4 identity in SKILL.md** — framework is now the "conductor's podium" for an orchestra of stakeholder-role agents; matches the v4 thesis
- **Reversed model invocation** — `disable-model-invocation: true` removed. Framework can now be invited from context (natural-language prompts like "build me an app", "harden this codebase", "audit this"). Always opens with an invitation pattern — never auto-enters.
- **v4 routing** — new verbs added to SKILL.md: `team`, `adopt`, `audit`, `arbitrate`, `feedback`, `issue`, `meta`. v3 verbs (`step`, `review`, `learn`, `update`, `tools`) remain supported for backward compatibility.
- **v4 first-run flow** — `tools/v4-first-run.md` creates the global user-level skeleton at `~/.hacky-hours/` (version, settings.yml, teams/, feedback/, sessions/, versions/) on first invocation. Seeds the audience profile with one short question.
- **`~/.hacky-hours/settings.yml` schema** — user-level preferences: session budgets, default model + per-role overrides, voice baseline, audience profile (technical background + per-role fluency), privacy toggles.
- **Routing stubs** for v4 verbs not yet implemented in Slice 1 — each stub honestly reports its slice status and points to the v3 fallback where applicable.
- **V4_DESIGN.md** — 503-line design document at `hacky-hours/02-design/V4_DESIGN.md` capturing the thesis, architectural foundations, all 19 locked design decisions, role roster, operations & state files, update flow, deferral list, kickoff order, and risks held consciously.

### Changed

- **SKILL.md description** — expanded into a rich, model-matchable description so context-driven invocation fires on relevant prompts (and stays silent on tactical one-offs)
- **Help message** — updated to v4.0.0 with v4 verbs prominent and v3 verbs marked as legacy-but-supported

### Added (Slice 2 — default team roster)

- **Default team template** at `templates/team/default/` — full 12-agent roster with:
  - Maya Tanaka (📊 Product) — user value, scope discipline, roadmap
  - Felix Okafor (🎨 Design) — user journeys, IA, interaction
  - Priya Chen (🏗️ Architect) — system design, ADRs, technology selection
  - Marcus Rivera (🖥️ Frontend) — components, state, perf, progressive enhancement
  - Sam Park (⚙️ Backend) — APIs, reliability, integration
  - Alex Davies (🛡️ Security) — threat modeling, secrets, auth, validation
  - Jordan Kim (🚀 Ops/SRE) — deployment, observability, runbooks, on-call
  - Emma Wright (🔍 QA) — test strategy, edge cases, regression risk
  - Lena Mwangi (♿ Accessibility) — WCAG, keyboard, screen reader, contrast
  - Diego Romano (📜 Licensing) — license compatibility, compliance scope
  - Yuki Nakamura (📈 Data) — schema, pipelines, retention, analytics
  - Kai Patel (🤖 AI/ML) — model selection, evals, AI safety
- **Each agent has 5 files**: profile.md (SSG-renderable frontmatter + bio), system-prompt.md (full role definition with audience adaptation), history.md (compactable resume), feedback.md (durable conductor feedback), preferences.yml (per-agent config)
- **Team-level files**: README.md (team description), tier.yml (full-tier roster + multiplexing config), VERSION (4.0.0), LICENSE (private by default per item 18), .gitignore
- **`/hacky-hours team` verb** — full implementation upgraded from Slice 1 stub:
  - Default Team Bootstrap on first invocation (copies template, stamps dates, `git init` + initial commit)
  - `team` no-arg: survey + roster view
  - `team list` — list all teams
  - `team show <agent-id>` — view agent profile (and `--prompt` for full system prompt)
  - `team switch <name>` — bind current project to a different team
  - `team new` — create a new team
  - `team init` — idempotent default-team creation
  - `team help` — full help
- **Team architecture made tangible**: teams are user-owned, separate from any project, applied by binding via project `AGENTS.md`. Each team is its own git repo (local-only default; GitHub-friendly remote optional).

### Added (Slice 4b — per-role first-impressions design docs in adopt)

- Adopt's Step 6 now produces real design docs from each **High** or **Critical** involvement role, not a placeholder.
- Each first-impressions doc is written in team-grade voice with frontmatter (`owner`, `last_reviewed`, `status: first-impressions`, `tier`, `covers`, `does_not_cover`, `related_docs`) so docs are standalone-readable and graduation-ready from day one.
- Two-tier template (per v3.0.0) used for ARCHITECTURE, SECURITY_PRIVACY, ACCESSIBILITY: deep + summary.
- Per-role doc generation respects denylist + tier calibration + voice mode.
- Parallel via Agent tool where available; sequential fallback otherwise.
- v3 → v4 migration case: existing v3 design docs are NOT overwritten — conductor is asked whether to augment, rewrite, or skip each.

### Added (Slice 7 — improvement loop closer)

- **`/hacky-hours feedback`** — capture session friction (tool / seam / role kinds) to `~/.hacky-hours/feedback/<date>-<kind>-<slug>.md`. Structured frontmatter, local-only, never auto-uploaded.
- **`/hacky-hours issue`** — opt-in submission of a feedback bundle (or fresh-composed content) as a GitHub issue against `empathetech/hacky-hours-docs`. Per-submission permission gate (`yes` / `edit` / `save draft` / `cancel`). Uses `gh` CLI.
- **`/hacky-hours meta`** — clusters accumulated feedback by kind/target/tags, proposes specific diffs against framework source files (verb files, role system prompts, schemas). Conductor reviews each cluster's proposed patch and chooses apply / submit-as-issue / submit-as-PR / skip / edit. Confidence-rated per cluster. Closes the dogfood improvement loop.

### Added (Slice 8 — team update + arbitration modes)

- **`/hacky-hours team update`** — promotes pending session changes (behavior feedback, prompt edits) into the team repo with per-change accept/edit/reject/defer review. Single git commit on the team repo per session-update; honest multi-session race-condition handling; never silently overwrites.
- **`/hacky-hours arbitrate <mode> <topic>`** — three named arbitration patterns:
  - `decide` — cheapest, framework summarizes positions, conductor decides directly
  - `resolve` — conductor states concerns, framework asks each role to propose against them
  - `watch` — agents converse with each other while conductor observes, ends on convergence or interrupt
- Every arbitration produces an ADR at `hacky-hours/02-design/decisions/<date>-<topic>.md` regardless of mode. `watch` mode appends the full transcript.

### Added (Slice 9 — static team site)

- **`/hacky-hours team site [serve|build|publish]`** — pure Python 3 stdlib static site generator (no npm, no Astro, no PyYAML, no Jinja). Reads agent `profile.md` frontmatter + bodies, generates HTML roster grid + per-agent profile pages.
- Three browse modes:
  - `serve` — local server (`python3 -m http.server 8000`); user runs the command themselves (no background-spawn risk)
  - `build` — generates `~/.hacky-hours/teams/<team>/docs/`; works via `file://` (relative URLs, no fetch dependencies)
  - `publish` — guides through GitHub Pages setup with a clear privacy gate before exposing team data
- Respects per-field `published` flag in profile.md frontmatter — `false` skips the agent entirely.
- Optional auto-deploy GitHub Action template for users who push the team repo.
- Mobile-friendly CSS; emoji avatars; clean readable typography.

### Added (Slice 10 — export verb)

- **`/hacky-hours export <target>`** — exports project docs for graduation into a team's knowledge base.
- v4.0.0 ships:
  - `markdown-bundle` — single concatenated `.md` with TOC, paste-ready for Notion / Confluence / Obsidian / GDocs. Smart heading-demotion, cross-doc link rewriting, two-tier doc handling.
  - `html-bundle` — designed; v4.0.0 recommends running `markdown-bundle` then any SSG (MkDocs/Hugo/etc.). Native html-bundle in v4.1+.
- Excludes operational state files (NARRATIVE.md, STATE.md, adoption-assessment) — exports are team-grade artifacts, not internal working state.
- API-based exporters (notion, gdocs, confluence) designed-but-not-implemented; honest deferral notice.

### Added (Slice 11 — team chat, tiered closed-captioned multi-agent dialogue)

Closes the v4 thesis gap pilot surfaced: orchestra was loaded as context but invisible during flow.

- **`/hacky-hours team chat <off | minimal | full>`** — toggle team visibility for multi-role verbs. Default `minimal`.
  - `off` — single narrator, pre-v4 behavior
  - `minimal` — speaker attribution at meaningful moments only (concern introduction, disagreement, hand-off)
  - `full` — closed-captioned dialogue with real per-role fan-out, side chatter, voice fidelity
- **`references/chat-format.md`** — canonical render contract: emoji glyphs (from V4_DESIGN.md §5), `**Name (Role) [HH:MM]**` header, per-mode rules, voice baselines table.
- **The hard rule** — "no tokens for tokens' sake" enforced across all modes. Every turn must add information; filler agreement, empty acknowledgments, manufactured disagreement, and restated points forbidden. Documented in `references/chat-format.md`.
- **`team_chat` setting** added to `~/.hacky-hours/settings.yml` (added by `v4-first-run.md` for new installs; existing users get a one-line append on first use).
- **Verb guidance updated** to honor `team_chat` mode: steps 1–5, `reviews/audit`, `tools/adopt`, `tools/arbitrate`. Each verb reads the mode and `chat-format.md` at entry.
- **Cost surfacing explicitly deferred to v4.1+** — no per-verb calibration data, no published tier → token-envelope mapping, no skill-level access to `/usage`. Switching to `full` prints a one-line caveat without numbers; existing `session_budget_warn` (§4.3) fires on actual consumption.
- Design source: V4_DESIGN.md §4.20.

### Added (Slice 12 — team learning closer, audit Lane B saturation guard, issue label-detect)

Closes the v4 thesis loop pilot dogfooding surfaced (after Slice 11 made the orchestra audible): the orchestra was loaded, spoke aloud, and forgot the conversation. Pre-Slice-12, no verb wrote to `~/.hacky-hours/sessions/<id>/pending/` or to per-agent `history.md`. The "agents learn and grow with context" headline was structural-only.

- **`references/capture-format.md`** — canonical contract for team-learning persistence. Pending-entry schema (frontmatter + content), `history.md` line schema, session-ID resolution algorithm (marker file at `~/.hacky-hours/sessions/.current-session` with 4-hour staleness window), per-verb implementation responsibilities, edge cases. Every multi-role verb references it; format changes happen in one file.
- **Phase N — Stash wired into every multi-role verb** — `steps/01-ideate.md`, `steps/02-design.md`, `steps/03-roadmap.md`, `steps/04-build.md`, `steps/05-iterate.md`, `reviews/audit.md` (Step 5), `tools/adopt.md` (Step 8, foundational team-meets-project history), `tools/arbitrate.md` (Step 5, high-signal behavior feedback). At verb tail: silent `history.md` append for each participating agent (one line per: date · project · verb · contribution), then a one-line behavior-feedback prompt to the conductor (always shown; `none` is a valid answer). Pending behavior notes accumulate at `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` for promotion via `/hacky-hours team update`. History commits land directly in the team repo at end-of-verb without going through review.
- **`/hacky-hours team backfill` — retroactive history population** (closes the "what about existing project history" gap surfaced during Slice 12 design). Forward-capture handles work done after Slice 12 lands. Projects that adopted v4 mid-stride — including hacky-hours-docs itself — need retroactive population, or agents' track records start empty on day-one of v4.0.0 install (team site renders bios with no history even for projects the team has shaped extensively). One-shot conductor-invoked verb: reads bound project's CHANGELOG.md (preferred) or git log, classifies each entry by which discipline(s) it touched (file paths + keywords table), proposes per-agent batches of history lines, conductor reviews per-agent (accept all / select / edit / reject / defer), commits per agent batch. Backfilled entries annotated `(backfilled, <CHANGELOG-anchor-or-SHA>)` for distinguishability + verifiable provenance. Flags: `--source changelog|git|both`, `--since <YYYY-MM-DD>`, `--dry-run`, `--agent <agent-id>` (incremental). Spec: `tools/team-backfill.md`.
- **`tools/team-update.md` updated** to drop the "captures automatically when..." vibes-spec and reference `references/capture-format.md` as source of truth. Clarifies behavior-feedback (review-required) vs. history-append (silent, fact-of-record) paths.
- **Audit Lane B saturation guard (closes issue #6)** — `reviews/audit.md` adds a conductor-side post-Lane-B saturation check: cross-references the doc-stranger's "First fix" recommendation against prior audit reports + Lane C verification + current doc state. If the recommendation is already present in the docs the stranger just read, replaces the first-fix with a graduation-indicator note instead of recording a false-negative critique. Documentation dimension on the scorecard annotates `· saturated (N)` where N is the consecutive saturation count (durable in `audits/.lane-b-saturation`). Preserves Lane B subagent's purity (it still reads only docs, no prior context); the conductor is the test interpreter.
- **`tools/issue.md` label-detect (closes issue #6 tail bug)** — probes upstream labels via `gh label list --repo empathetech/hacky-hours-docs` before `gh issue create`. Builds `--label` from the intersection of requested labels (`user-feedback`, `v<framework-major-version>`) and existing labels. Omits `--label` entirely if no intersection — submitting with a non-existent label would fail the whole call. Surfaces missing-labels gap in the issue body footer so upstream can address.
- **`V4_DESIGN.md` §4.21** — full design rationale for capture step (mechanism choice, two-slot review semantics, session-ID heuristic, deferred items).
- **ADR** at `02-design/decisions/2026-05-17-team-learning-capture.md` — captures the design decision including rejected alternatives (inline capture, end-of-session hook, conductor-initiated only, history-merged-into-feedback-review).
- **V4_QA.md Test 11** — 10 sub-tests covering pre-state, history append, behavior feedback prompt, "none" answer path, team-update promotion, next-session-uses-updated-agent verification, session-ID staleness regeneration, Lane B saturation guard, issue.md label-detect, team site reflection.

### Deferred to v4.1+ from Slice 12

- **History compaction** when `history.md` exceeds ~500 lines / ~10k tokens. Slice 12 ships append; compaction needs design on trigger + review semantics.
- **Implicit feedback capture** (override-N-times → stash implicitly). Real signal but classification fuzzy. Re-evaluate after explicit prompt has run a release cycle.
- ~~**Team site rendering of `history.md`**~~ — *un-deferred; shipped in Slice 13 (below).*
- **Per-verb stash-mode override** in `settings.yml`. Always-on is the v4.0.0 default; tune later if data says it's noisy.

### Added (Slice 13 — Agent representation: team site history + auto-evolving profile + résumé + reflection)

Closes the v4 thesis loop in the visible layer. Pre-Slice-13, Slice 12's persistence was real in data but invisible on the team site — bios stayed static even as agents accumulated work. Conductor surfaced this during Slice 12 ship: *"the point of the team site and having these team avatars are that they are learning and growing with context; I want to treat these AI agents like human team members."* Slice 13 makes the orchestra appear as teammates with track records, not static personas with attached logs.

**Four coordinated pieces, all in v4.0.0:**

- **Derived metrics block (`metrics:` in `profile.md` frontmatter)** — auto-managed schema in every agent's `profile.md`: `level` (0–5 with breadth bumps), `history_entries`, `projects`, `verbs_run`, `by_verb` counts, `feedback_count`, `last_active`, `metrics_refreshed`, `reflected_at`. Refreshed in the same git commit as history append at end of every multi-role verb's Stash phase (bundled — no separate commit). Display-only; conductors don't hand-edit (overwritten on next refresh). Schema spec: `references/capture-format.md` §§"Derived metrics" + "Level derivation".
- **Team-site renders history + lessons + résumés + level badges** (un-defers the v4.1+ item from Slice 12). `templates/team-site/generate.py` extended (~150 lines added, still pure Python stdlib) to read `history.md`, `feedback.md`, the `metrics:` block, and `resume.md` per agent. Profile pages gain a "Recent track record" timeline (last 10 entries with date/project/verb/summary), a "Lessons applied" section (durable feedback notes), a résumé link (when present), and a level + contribution-count metadata line in the header. Index cards gain a level badge (`lvl 3 · 18 contributions · 1 project`). Agents with no history get no badge — keeps fresh team grids clean. Mobile-responsive CSS additions.
- **`/hacky-hours team resume <agent-id> | --all`** — synthetic résumé generator. Writes `agents/<id>/resume.md` composited from `profile.md` + `system-prompt.md` + `history.md` + `feedback.md` + `preferences.yml`. Structure: header (name, role, level, contributions), summary (distilled), skills (aggregated by verb-type with evidence counts), experience (grouped by project, chronological), recent learnings (paraphrased from feedback), profile (verbatim bio). Three style presets — `minimal` / `standard` / `deep`. Fact-derived only — every claim traces to a source; no invented skill claims; honest about thin work (agents with zero history get a minimal résumé, not padded). Regenerated freely; conductor commits if they want it tracked. Spec: `tools/team-resume.md`.
- **`/hacky-hours team reflect <agent-id> | --all`** — agent self-reflection. Opt-in, conductor-invoked. Agent walks own `history.md` + `feedback.md` + `profile.md` and produces three outputs:
  - **Track record section** — silent auto-append/replace in `profile.md` Bio. One paragraph per project, third-person past-tense, cites by count. No conductor review (same semantics as forward-capture history append). Committed silently.
  - **Prose updates** — proposed refinements to Background / How I work / What I produce sections. Each warranted revision writes a `kind: prose_update` pending entry to `~/.hacky-hours/sessions/<id>/pending/<agent-id>.md` with a `target_section` field, reviewed via existing `team update` accept/edit/reject/defer flow.
  - **Self-observations** — strengths the agent sees in own work + gaps to close. Printed; conductor names items to stash as behavior feedback for next session.

  Spec: `tools/team-reflect.md`. Cadence: opt-in only (not part of Stash phase). Hybrid editing model conductor-confirmed: silent (metrics, track record), conductor-reviewed (prose updates), conductor-initiated (self-observations).

- **`tools/team-update.md`** now accepts `kind: prose_update` pending entries in addition to `behavior_feedback` and `prompt_edit` — same accept/edit/reject/defer flow per section.
- **`tools/team.md` + `SKILL.md`** — routing + help text for `team resume` and `team reflect` subcommands; argument-hint updated.
- **Every multi-role verb's Stash step 4** updated to bundle metrics refresh with history append in a single commit.
- **`references/capture-format.md`** — new sections §§"Derived metrics", "Level derivation", "Resume composition", "Reflection semantics". Implementation-responsibilities step 5 added (metrics refresh) with bundled commit pattern.

**Design + project artifacts:**

- `V4_DESIGN.md` §4.22 — full design rationale
- ADR `02-design/decisions/2026-05-17-agent-representation.md` — captures the four-piece decision, hybrid editing rationale, and rejected alternatives (single combined verb, conductor-set levels, separate metrics file, auto-rewrite without review)
- V4_QA.md Test 12 — 10 sub-tests covering metrics refresh post-verb, resume generation per agent, reflection three-output flow, hybrid bio editing semantics, team-site rendering of history/lessons/badges/résumé links

### Deferred to v4.1+ from Slice 13

- History compaction (shared deferral with Slice 12)
- Agent-to-agent skill recommendation
- Résumé export to non-Markdown shapes (LinkedIn JSON / PDF)
- Per-project skill maps + cross-project skill inference
- Reflection auto-cadence triggers

### Backward compatibility

- All v3 verbs (`step`, `review 1..3`, `learn 1..3`, `update 1..2`, `tools upgrade|mode|walkthrough`) continue to work in v4
- Existing v3 projects function without modification
- Migration story for v3 → v4 will land in `tools/upgrade.md` updates as subsequent slices complete
- `disable-model-invocation` removal is a behavioral change but not a breaking install — v3 projects that never relied on context-driven invocation are unaffected
- **Slice 11 (team chat):** existing `~/.hacky-hours/settings.yml` files without `team_chat:` are treated as `team_chat: minimal` until the user sets it explicitly. No breaking change to first-time invocation.
- **Slice 12 (team learning capture):** existing teams without prior `history.md` entries are unaffected — the auto-append just starts adding entries from this point forward. Existing `~/.hacky-hours/sessions/` (empty pre-Slice-12) is similarly unaffected; the `.current-session` marker is created on first capture. No data migration required.

---

## [3.0.0] — 2026-05-06

**Breaking install path change.** The `hacky-hours` framework now ships as a Claude Code Skill (`SKILL.md` format) instead of a single slash command file. `/hacky-hours` continues to work exactly the same — only the install location changes, from `~/.claude/commands/hacky-hours.md` to `~/.claude/skills/hacky-hours/`. The installer handles the migration automatically (downloads new structure, removes old file).

> **To upgrade:** Re-run the install script from the README. The installer detects and removes the v2.x file. **Restart Claude Code** after install for the new top-level `.claude/skills/` directory to be watched.

### Added

- **SKILL.md skill format** — `hacky-hours` is now a Claude Code Skill with bundled supporting files. SKILL.md is a small entrypoint (~600 lines, down from 1500); per-step / per-review / per-tool guidance lives in `steps/`, `reviews/`, `learn/`, `update/`, `tools/` subdirectories under `${CLAUDE_SKILL_DIR}` and is loaded only when invoked. Pre-approves a narrow set of read-only Bash + Read tools via `allowed-tools` to reduce permission prompts during sessions. See [ADR: Migrate to SKILL.md format](hacky-hours/02-design/decisions/2026-05-06-migrate-to-skill-format.md).
- **Two-tier design templates** — Each design doc is now a deep dive (`<DOC>-deep.md` — the actual blueprint, source of truth, what Step 4 builds from) plus a one-screen summary (`<DOC>-summary.md` — a faithful condensation for quick gut-checks and as an onramp for non-technical readers). The deep dive is built first; the summary is generated from it and never adds new information. Prototype currently exists for ARCHITECTURE only; DATA_MODEL, USER_JOURNEYS, SECURITY_PRIVACY, etc. follow in a v3.x release once the pattern is validated in real sessions. See `${CLAUDE_SKILL_DIR}/templates/design/README.md` for the pattern.

### Changed

- **Install path:** `~/.claude/commands/hacky-hours.md` → `~/.claude/skills/hacky-hours/` (a directory)
- **Install script:** now downloads the GitHub repo tarball (instead of a single file), extracts the skill directory tree, transforms SKILL.md frontmatter from dev shape to installed shape, and removes the old v2.x slash command file if present
- **`tools upgrade` Flow A:** drafts the deep dive first (`<DOC>-deep.md`) for inferred design docs, then generates the `<DOC>-summary.md` as a faithful condensation; reads `templates/design/README.md` first to confirm the workflow
- **`tools upgrade` Flow C:** scaffold table adds row for two-tier templates (v3.0.0 introduction)
- **`review 1` audit:** design-doc scorecard handles both single-tier (legacy) and two-tier docs; flags missing deep dives, missing summaries, and summary drift from the deep dive
- **`review 2` optimize, `review 3` pivot:** updated for the two-tier model (deep dive as source of truth — changes land in the deep dive first, summary regenerates)
- **`learn 1` tour:** uses summaries as onramps for non-technical readers, with cross-links to drill into specific deep-dive sections on demand
- **`tools walkthrough`:** Step 2 description correctly describes "deep first, summary derived"
- **`steps/04-build`:** explicitly directs Claude to read `-deep.md` docs (not summaries) for implementation

### Backward compatibility

- Slash command surface (`.claude/commands/`) remains supported by Claude Code; this migration affects only how `hacky-hours` itself ships
- Existing user projects with single-tier design docs continue to work without modification — `tools upgrade` Flow C will surface the two-tier templates as a v3.0.0 scaffold gap users can opt into
- Users on v2.x continue working until they re-run the installer

---

## [2.1.0] — 2026-04-18

`tools upgrade` now detects and fixes stale framework-authored boilerplate in existing `hacky-hours/` docs.

### Added

- **`tools upgrade` Flow C — Step 2b: Boilerplate migration** — scans all files under `hacky-hours/` (plus `.claudeignore` and `CLAUDE.md`) for pre-v2.0.0 patterns: "Level X" headers and old command names (`/hacky-hours audit`, `sync`, `upgrade`, `mode`, `onboard`, `link`, etc.). Reports findings grouped by file with suggested replacements. `/hacky-hours link` references are flagged for manual review rather than auto-replaced (command was removed in v2.0.0). Confirms before writing anything.

### Fixed

- **Self-documentation sweep** — applied the new boilerplate migration to this repo's own `hacky-hours/` artifacts: Level → Step headers in `PRODUCT_OVERVIEW.md`, `BACKLOG.md`, `02-design/README.md`, `ACCESSIBILITY.md`, `LICENSING.md`, `TESTING.md`; old command names in `ACCESSIBILITY.md`, `TESTING.md`, `ARCHITECTURE.md`, `SECURITY_PRIVACY.md`, and `PRODUCT_OVERVIEW.md`; removed dead Risk #4 (`link` command) from `SECURITY_PRIVACY.md` and renumbered remaining risks

---

## [2.0.2] — 2026-04-18

Fix hardcoded version strings in the `tools upgrade` skill prompt.

### Fixed

- **Version string in skill prompt** — `description`, help message, version marker written to users' `CLAUDE.md`, and completion report all hardcoded `v2.0.0`; now correctly reflects the current release

---

## [2.0.1] — 2026-04-18

Documentation sweep: all template docs, runbooks, and the README brought up to date with v2.0.0 terminology and command surface.

### Fixed

- **Level → Step language** — all template docs (`01-ideate/`, `02-design/`, `03-roadmap/`, `04-build/`), step READMEs, and runbooks now consistently use "step" instead of "level"
- **Stale v1.x command references** — `install-as-command.md` command table, `cross-tool-usage.md`, `github-action-sync.md`, `document-hygiene.md`, and `04-build/README.md` updated to v2.0.0 command surface (`step`, `review`, `learn`, `update`, `tools`)
- **"four-level" → "five-step"** in README, FAQ, `import-as-resource.md`, and `cross-tool-usage.md`
- **Removed `/hacky-hours link` reference** from `02-design/README.md` Claude Guidance — command was removed in v2.0.0
- **Removed `/hacky-hours checklist` reference** from `02-design/TESTING.md` — now points to `/hacky-hours help step 4`

### Added

- **README: Command Reference section** — full command breakdown organized by the five parent groups, added after the install section
- **README: Step 5 — Iterate in the diagram** — Mermaid diagram now shows all five steps with the loop-back arrow from Step 5 to Step 4
- **README: Five Steps table** — replaces the old Four Levels table, includes Step 5

### Changed

- **README: "paralyzed" → "stuck in endless planning"** — inclusive language follow-up to PR #2
- **README: Diagram labels** — subgraph labels updated from `L1–L4 "Level N"` to `S1–S5 "Step N"`

---

## [2.0.0] — 2026-04-11

**MAJOR VERSION — breaking changes to all command entry points.** See [ADR: v2.0.0 Command Surface Redesign](hacky-hours/02-design/decisions/2026-04-11-v2-command-surface-redesign.md) for the full rationale and migration table.

Users upgrading from v1.x: run `/hacky-hours tools upgrade` after installing to update CLAUDE.md references. All v1.x commands still exist as guidance sections — only the entry point syntax changed.

### Breaking Changes

- **Command surface fully reorganized** into five parent groups: `step`, `review`, `learn`, `update`, `tools`
- **`/hacky-hours ideate|design|roadmap|build`** → `/hacky-hours step 1|2|3|4` (named aliases still work: `step ideate`, `step build`, etc.)
- **`/hacky-hours iterate`** → `/hacky-hours step 5` (or `step iterate`) — iteration is now a first-class step
- **`/hacky-hours dry-run`** → `/hacky-hours step 0` — dry-run is step zero
- **`/hacky-hours audit`** → `/hacky-hours review 1` (or `review audit`)
- **`/hacky-hours optimize`** → `/hacky-hours review 2` (or `review optimize`)
- **`/hacky-hours pivot`** → `/hacky-hours review 3` (or `review pivot`)
- **`/hacky-hours learn [tour|onboard|quiz]`** → `/hacky-hours learn [1|2|3]` (named aliases still work)
- **`/hacky-hours sync`** → `/hacky-hours update 1` (or `update version`)
- **`/hacky-hours sync --issues`** → `/hacky-hours update 2` (or `update project`)
- **`/hacky-hours upgrade|migrate|adopt`** → `/hacky-hours tools upgrade` (detects context)
- **`/hacky-hours mode`** → `/hacky-hours tools mode`
- **`/hacky-hours mode default`** → `/hacky-hours tools mode 1` (or `tools mode builder`)
- **`/hacky-hours mode engineer`** → `/hacky-hours tools mode 2`
- **`/hacky-hours status`** → bare `/hacky-hours` (surveys and reports)
- **`/hacky-hours version`** → listed in `/hacky-hours help` header
- **`/hacky-hours checklist`** → documented in `/hacky-hours help step 4`
- **`/hacky-hours link` and `link --sync`** → **removed** (use monorepo + `--root` instead)
- **"Level" language replaced with "Step"** throughout the command prompt, CLAUDE.md, and all scaffold templates

### Added

- **Global Values section** in the command prompt — the framework's first-class values (human as driver, free before paid, privacy-first, accessible by default, licensing hygiene) declared once at the top and governing all commands
- **`/hacky-hours tools walkthrough`** — new command: narrative overview of how all commands work together, designed for framework adopters
- **`step 0`** — dry-run mode, lives naturally before step 1
- **`step 5`** — iteration promoted as a first-class step in the cycle
- **Numbered aliases** throughout: `step 1–5`, `review 1–3`, `learn 1–3`, `update 1–2`, `tools mode 1–2`
- **`tools mode builder`** — "builder" replaces "default" as the plain language mode name

### Changed

- **Command prompt reduced** from ~2,100 lines to ~1,470 lines (~30% reduction) through structural consolidation and removal of link/migrate/adopt sections
- **`tools upgrade`** absorbs `migrate` (layout migration) and `adopt` (new codebase onboarding) — detects context and runs the appropriate flow
- **`review`** with no argument runs `review 1` (audit) by default, then offers to run review 2 and 3
- **Version string** bumped to v2.0.0 in routing table, help message, and command description

### Removed

- **`/hacky-hours link`** and **`link --sync`** — multi-repo coordination removed; guidance updated to recommend monorepo + `--root`
- **`/hacky-hours migrate`** standalone — absorbed into `tools upgrade`
- **`/hacky-hours adopt`** standalone — absorbed into `tools upgrade`
- **`/hacky-hours status`** standalone — behavior incorporated into bare command
- **`/hacky-hours version`** standalone — version shown in help message header
- **`/hacky-hours checklist`** standalone — content in `help step 4`

### Design doc updates

- **`ARCHITECTURE.md`** — lifecycle diagram updated to five-step cycle, command surface section updated, Known Fragility updated
- **`CLAUDE.md`** — "Level" → "Step" throughout, command references updated (`review 1`/`update 1` instead of `audit`/`sync`)
- **ADR: v2.0.0 Command Surface Redesign** — documents all thirteen decisions with rationale, tradeoffs, and breaking changes migration table

---

## [1.8.0] — 2026-04-11

Learn suite, upgrade command, testing design doc, and expanded audit scorecard.

### Added

- **`/hacky-hours learn [tour|onboard|quiz]`** — new learning suite for knowledge transfer and onboarding. Three modes: guided tour of the project (scoped to focus area), hands-on task scoping for engineers new to an area, and knowledge quiz (broad or scoped). All modes work as Claude Code conversations; tour and quiz optionally generate a shareable Astro static site. Conversation-first design means the feature always works even without Node.js.
- **`/hacky-hours upgrade`** — brings existing project artifacts up to date with the current command version. Detects missing scaffold folders, new doc templates, and `.claudeignore` entries introduced since the project was last scaffolded. Absorbs the v0.x → v1.0 folder migration previously handled by `migrate`. Read-only until the user confirms. Writes a `<!-- hacky-hours: vX.Y.Z -->` version marker to `CLAUDE.md` after running.
- **`02-design/TESTING.md` template** — new Level 2 design doc for test strategy, test types, definition of done, and test environments. Scaffolded by default alongside ACCESSIBILITY.md and LICENSING.md.
- **`hacky-hours/learn/` and `hacky-hours/feedback/`** — new scaffold folders. `learn/` holds generated tour/quiz Astro sites (tour/, quiz/, personal/<username>/). `feedback/` holds user-submitted feedback files (`feedback-<username>-<timestamp>.md`) from learn sessions.
- **Feedback loop** — `iterate` Step 1 Capture now checks `hacky-hours/feedback/` for feedback files from learn sessions before asking the user to brain-dump. Surfaces them as additional input.
- **Expanded audit scorecard (Phase 2)** — now checks all design doc types (ARCHITECTURE, DATA_MODEL, USER_JOURNEYS, STYLE_GUIDE, ACCESSIBILITY, MARKET_FIT, BUSINESS_LOGIC, SECURITY_PRIVACY, LICENSING, TESTING, RELATED_REPOS) with a consistent per-domain format: exists? filled in? specific gap if not. Reports as a table with ✓/✗/⚠ indicators.
- **ADR: Learn Suite Architecture** (`02-design/decisions/2026-04-11-learn-suite-architecture.md`) — documents the conversation-first/site-optional design, Astro stack selection, and sub-subcommand grouping decision.

### Changed

- **Scaffold structure** — `learn/` and `feedback/` folders added. `02-design/TESTING.md` added. `hacky-hours/learn/` added to `.claudeignore` defaults.
- **`help design`** — TESTING added to available docs list.
- **`hacky-hours/02-design/README.md`** — TESTING.md added to the design doc index.
- **Version bumped** to v1.8.0 in routing table, help message, and command description.

### Design doc updates

- **`ARCHITECTURE.md`** — Learn Suite section, Static Site Generation section (Astro), Upgrade Command section, Known Fragility updated
- **`SECURITY_PRIVACY.md`** — `onboard` automated git push, user-generated content in feedback files, Astro/Node.js supply chain surface
- **`ACCESSIBILITY.md`** — scope updated to include generated web UI; v1.8.0 command notes; WCAG 2.1 AA evaluation flagged as outstanding
- **`TESTING.md`** — created for hacky-hours-docs: testing layers, pre-release checklist, eval coverage, v1.8.0 testing notes

---

## [1.7.0] — 2026-04-04

Voice mode — non-technical plain language is now the default conversation style, with an opt-in engineer mode for technical users.

### Added

- **`/hacky-hours mode`** — new command to toggle conversation voice between `default` (plain language) and `engineer` (technical). Persists to `CLAUDE.md` across sessions. Toggles without an argument; accepts `mode engineer` or `mode default` explicitly.
- **`help mode`** — subcommand help entry documenting mode usage, both voices, and persistence behavior
- **Voice mode in scaffold** — new projects get a `## Hacky Hours Voice` section in their generated `CLAUDE.md`, defaulting to plain language, with a one-line note on how to switch

### Changed

- **Default conversation style is now non-technical** — tradeoffs explained through outcomes, analogies, and consequences; no jargon without plain-language definition. Engineers opt in to technical mode rather than non-technical users having to ask for simpler explanations.
- **`ARCHITECTURE.md`** — Voice Mode section added documenting mode as a persistent config concept
- **`ACCESSIBILITY.md`** — non-technical default documented as an explicit accessibility decision with rationale
- **Version bumped** to v1.7.0 in routing table, help message, and command description

---

## [1.6.0] — 2026-03-30

Readability and accessibility pass — making every document approachable for non-technical users.

### Added

- **"What is this?" intros** on all Level 2 design doc templates — plain-language explanations of what each document type is and why it exists, so non-technical users aren't put off by terms like "architecture" or "data model"
- **Beginner bridges** on advanced docs — `import-as-resource.md`, `github-action-sync.md`, and `install-as-command.md` now explain prerequisites and audience before diving into instructions
- **Pre-push git hook** — blocks tag pushes if CHANGELOG.md doesn't have a matching version entry, preventing the version drift that happened with v1.5.1/v1.5.2

### Changed

- **`runbooks/document-hygiene.md`** — full rewrite replacing engineer jargon (Hot/Warm/Cold tiers, ADRs, append-only ledger) with plain-language equivalents; added note that `/hacky-hours` handles most of this automatically
- **`runbooks/getting-started/03-git-basics.md`** — expanded "Working with Branches" section with plain-language explanations of what branches are, why you'd use them, and what flags like `-b` and `-u origin` do
- **`runbooks/getting-started/07-linux-setup.md`** — added context for `curl | sudo bash` pattern and step-by-step explanation of the npm permissions workaround
- **`runbooks/getting-started/02-claude-code.md`** — explained why Claude Pro is required (vs free account) and what `npm install -g` does
- **`runbooks/cross-tool-usage.md`** — added one-line descriptions of Cursor, Windsurf, MCP, and Claude.ai Projects for readers unfamiliar with them
- **`README.md`** — added context line before Mermaid diagram; marked advanced sections (slash command install, import-as-resource) with callouts directing beginners elsewhere
- **`runbooks/getting-started/05-windows-setup.md`** — linked PATH error to glossary with inline explanation
- **`02-design/ACCESSIBILITY.md`** — reformatted header to match other Level 2 templates (added attribution line, replaced inline intro with "What is this?" callout)
- **`02-design/LICENSING.md`** — removed redundant intro paragraph (replaced by "What is this?" callout)

### Fixed

- **`runbooks/costs.md`** — replaced Google Domains reference (shut down) with Squarespace Domains
- **`CHANGELOG.md`** — added missing entries for v1.5.1 and v1.5.2

---

## [1.5.2] — 2026-03-30

Cross-reference fixes and `.claudeignore` from optimize run.

### Fixed

- **CLAUDE.md** — fixed broken path to SECURITY_PRIVACY.md, removed reference to nonexistent `04-build/README.md`
- **ARCHITECTURE.md** — updated prompt size metric, fixed stale optimize description in lifecycle diagram
- **Non-linear lifecycle ADR** — noted optimize redesign from v1.5.1
- **`.claudeignore`** — created (was missing — archived docs were loading into context unnecessarily)
- Removed empty `03-roadmap/` directory

---

## [1.5.1] — 2026-03-30

Optimize command redesign and milestone housekeeping.

### Changed

- **`/hacky-hours optimize`** — redesigned from metrics-only dashboard to substantive review comparing design intent vs. current reality. For code projects, reads planning docs AND the codebase. For docs-only projects, analyzes the command prompt against design docs.

### Fixed

- **SECURITY_PRIVACY.md** — added GitHub API surface (`sync --issues`), cross-repo writes (`link`), and audit secret scanning limitations
- **ACCESSIBILITY.md** — added v1.5.0 new command evaluation notes
- **PRODUCT_OVERVIEW.md** — fixed stale version reference (v1.0.1 → v1.5.0), updated non-goals
- **CLAUDE.md** — added Project State Machine section (eating our own dogfood)

### Housekeeping

- Archived CHANGELOG entries v0.1.0–v0.8.0 to `archive/changelog/`
- Archived completed `ITERATION.md` (v1.5.0) and unused `ROADMAP.md` stub

---

## [1.5.0] — 2026-03-30

Non-linear lifecycle: product pivot, doc efficiency optimization, and two-way GitHub Issues sync.

### Added

- **`/hacky-hours optimize`** — new command that evaluates framework documentation efficiency. Scans all docs for token cost (estimated), staleness (last modified vs. last commit reference), density (placeholder vs. real content), and cross-reference usage. Generates actionable recommendations: archive, consolidate, trim, or fill in. Optionally saves results as an optimization report in `audits/`. Also integrated as a lighter check in iterate Step 2 — flags oversized/stale docs during synthesis.
- **`/hacky-hours pivot`** — new lifecycle path for product re-ideation with full context. Reads all existing artifacts, walks through Level 1 questions with awareness of current state, produces a structured diff of what changed, and cascades changes through Levels 2-4. Includes doc structural refactoring (merge, split, retire) and ADR generation for significant direction changes. Use when the product direction itself needs rethinking, not just refinement.
- **`/hacky-hours sync --issues`** — two-way reconciliation between BACKLOG.md and GitHub Issues. Push: creates Issues from BACKLOG items without `#<number>` annotations. Pull: surfaces open Issues with `[hacky-hours]` label not in BACKLOG. Diverged items shown side-by-side for human resolution. Last-write-wins conflict model — every change requires explicit confirmation. Creates `[hacky-hours]` label automatically if missing.
- **ADR: Non-Linear Lifecycle** (`02-design/decisions/2026-03-30-non-linear-lifecycle.md`) — documents the shift from a strictly linear four-level lifecycle to one with backward arcs via `pivot` and self-evaluation via `optimize`.
- **ADR: Two-Way GitHub Issues Sync** (`02-design/decisions/2026-03-30-issues-two-way-sync.md`) — documents the last-write-wins conflict resolution model, identity linking (`#<number>` in BACKLOG, `[hacky-hours]` label on Issues), and the decision to keep neither source canonical.

### Changed

- **Lifecycle model** — the framework is no longer strictly linear. ARCHITECTURE.md now includes a Mermaid diagram showing the iterate → pivot backward arc and the optimize self-evaluation loop.
- **ARCHITECTURE.md** — added Lifecycle Model section, GitHub Issues Integration section, updated command prompt size metric.
- **Iterate guidance (Step 2)** — now includes a lightweight efficiency check that flags oversized/stale docs during synthesis, with a suggestion to run `/hacky-hours optimize` for full analysis.
- **Sync command** — now has two modes: `sync` (releases, unchanged) and `sync --issues` (issue reconciliation). Routing and help updated accordingly.
- **Help message** — added `optimize`, `pivot`, and `sync --issues` entries.
- **Subcommand help** — added `help optimize`, `help pivot`, and `help sync --issues` entries.

---

## [1.4.0] — 2026-03-21

Cross-repo linking: connect related repos, generate RELATED_REPOS.md in both, and re-sync when the authoritative repo changes.

### Added

- **`/hacky-hours link`** — new command for connecting two related repos. Run in the dependent repo, pointing at the authoritative repo's local path. Reads both repos' design docs, infers the relationship and source-of-truth boundary, asks clarifying questions, and generates `RELATED_REPOS.md` in both repos plus a `## Related Repositories` section in this repo's `CLAUDE.md`. `--sync` flag re-reads the authoritative repo's current design docs and surfaces what's changed since the link was established — without auto-updating anything.
- **`RELATED_REPOS.md` template** (`02-design/RELATED_REPOS.md`) — new Level 2 design artifact for documenting cross-repo relationships. Contains: relationship table (role + source-of-truth boundary per repo), Decision Routing Table (design question → doc in other repo), and cross-repo coordination protocol. Single file with one `## Repo:` section per related repo.

### Changed

- **Level 2 guidance** — added `RELATED_REPOS.md` to the "which docs does your project need?" table, prompted when `ARCHITECTURE.md` indicates a multi-repo split. Also added `link` suggestion to the Claude Guidance section of `02-design/README.md`.
- **Help message** — added `--- Multi-repo ---` section with `link` entry.
- **Subcommand help** — added `help link` entry documenting both initial link and `--sync` usage.

---

## [1.3.0] — 2026-03-21

Accessibility audit, glossary expansion, version bump check, and CLA resolution.

### Added

- **Pre-release version bump check** — the audit flow (Phase 2) now checks whether version strings in the command prompt match the latest CHANGELOG version before tagging. Flags mismatches as warnings.
- **19 new glossary entries** — ARIA, CCPA, copyleft, frontmatter, GDPR, GPL, HIPAA, MCP, NVDA, OAuth, OWASP Top 10, screen reader, submodule, symlink, tag, VoiceOver, WCAG, YAML, and backend. All terms were found used in runbooks or templates without definition.

### Changed

- **ACCESSIBILITY.md** — updated with audit findings: 21 terms addressed, remaining gaps documented (screen reader navigation, i18n, shell-specific instructions).
- **LICENSING.md** — CLA checklist item resolved: not needed for a Markdown-only MIT project. Revisit only if commercial product or relicensing is considered.

---

## [1.2.0] — 2026-03-21

Cross-tool support, CHANGELOG deduplication, and architecture documentation.

### Added

- **Cross-tool usage runbook** (`runbooks/cross-tool-usage.md`) — documents how to use the framework in Cursor, Windsurf, Claude.ai Projects, or any LLM tool that reads project context. The slash command is a Claude Code convenience; the framework works anywhere via CLAUDE.md project instructions.
- **Release Process section in ARCHITECTURE.md** — documents the dev → installed publish cycle, version bump strategy (patch/minor/major), and the three places version strings need updating.
- **Cross-Tool Support section in ARCHITECTURE.md** — explains how the framework works without the slash command: artifacts + CLAUDE.md project state machine.

### Changed

- **CHANGELOG deduplication** — `hacky-hours/04-build/CHANGELOG.md` is now a symlink to the root `CHANGELOG.md`, eliminating duplicate changelogs. The adopt flow now detects existing CHANGELOGs and creates symlinks instead of new files.
- **ARCHITECTURE.md Known Fragility** — updated to reflect v1.1.0 harmonization work; remaining fragility items are now: no gradual rollout, single-file architecture, cross-tool portability.
- **Adopt flow** — now detects existing `CHANGELOG.md` files and creates a symlink to them instead of creating a duplicate. Includes explicit guidance on computing relative symlink paths.

---

## [1.1.0] — 2026-03-21

Subcommand help, persistent audit scorecards, and command prompt harmonization.

### Added

- **`/hacky-hours help <command>`** — detailed per-command help for all 10 commands (ideate, design, roadmap, build, iterate, audit, sync, adopt, migrate, dry-run). Shows what the command does, when it's done, and what to run next.
- **Audit scorecards (Phase 5)** — after running `/hacky-hours audit`, optionally save results as a persistent Markdown scorecard in `audits/`. Scorecards capture secrets scan, doc readiness, git status, and next steps in a standardized, dated format (`YYYY-MM-DD-audit.md`).
- **`audits/` directory** — added to scaffold structure and `.claudeignore` defaults. Stores persistent audit scorecards.
- **Context preambles** — Iterate, Sync, Audit, Adopt, and Migrate workflows now have "Context to read before starting" sections, matching the pattern already used by Levels 1–4.
- **`hacky-hours/` framework artifacts** — dogfooding: the framework's own PRODUCT_OVERVIEW, ARCHITECTURE, SECURITY_PRIVACY, LICENSING, ACCESSIBILITY, ROADMAP, BACKLOG, and CHANGELOG now live under `hacky-hours/`.

### Changed

- **Scaffold structure** — now creates `audits/` directory alongside `archive/`.
- **Generated `CLAUDE.md`** — scaffold now notes that paths should be substituted when ROOT_PATH differs from `hacky-hours/`.
- **Adopt file list** — now matches what Scaffold creates: includes `02-design/README.md`, `02-design/decisions/`, `03-roadmap/ROADMAP.md`, and `audits/`.
- **Help message** — updated to show `help <cmd>` option and audit scorecard description.

---

## [1.0.1] — 2026-03-20

### Fixed

- **`/hacky-hours iterate`** — `ITERATION.md` was being created at the project root instead of under ROOT_PATH (`hacky-hours/` by default). Archive path was also pointing to `archive/` instead of `ROOT_PATH/archive/`. Both paths now correctly follow ROOT_PATH, consistent with all other framework artifacts.

---

## [1.0.0] — 2026-03-20

Safety-first design philosophy, licensing as a first-class artifact, and `hacky-hours/` subfolder as the default scaffold location.

### Added

- **`02-design/LICENSING.md`** — new design document template covering product license choice (MIT, Apache, GPL, proprietary, etc.), third-party dependency license compatibility, business model implications, and a pre-build checklist. Scaffolded by default alongside `ACCESSIBILITY.md`.
- **`/hacky-hours audit`** — new read-only release readiness command: (1) secrets and sensitive file scan with heuristic pattern matching, (2) framework doc readiness checks, (3) git status translated into plain language, (4) numbered next-steps to-do list ordered by severity. Never modifies any files. The recommended step before `/hacky-hours sync`.
- **`/hacky-hours adopt`** — new command for bringing an existing codebase into the framework. Reads README, package manifests, directory structure, schema files, auth files, env var references, git log, and TODO comments to infer artifact stubs for PRODUCT_OVERVIEW, ARCHITECTURE, SECURITY_PRIVACY, and BACKLOG. Asks clarifying questions for what can't be inferred. Always confirms before writing. Hands off to `iterate` as the natural next step.
- **`/hacky-hours migrate`** — new command that moves existing root-level framework artifacts into the `hacky-hours/` subfolder using `git mv` (preserving history). Updates `.claudeignore`, `CLAUDE.md`, and flags any `hacky-hours-sync.yml` GitHub Action path changes needed. Shows exactly what it will do before doing anything. Commits framework files only — not `git add -A`.
- **Constraints & Values section in `PRODUCT_OVERVIEW.md`** — captures licensing intent, privacy stance, infrastructure preference, and accessibility commitment at Level 1, seeding Level 2 design decisions before any code is written.
- **Safety-first design philosophy** — documented in `CLAUDE.md` and embedded throughout Level 2 guidance: free before paid, less infrastructure before more, privacy-preserving before data-rich, accessible by default, fewer dependencies before more. Claude leads with the simplest safe option and explains tradeoffs before suggesting complexity.
- **Licensing questions at Level 1** — the Level 1 → Level 2 transition now explicitly includes licensing intent questions so that dependency choices in Level 2 are made with license compatibility in mind.
- **Context-reading preambles on every level command** — each level command (`ideate`, `design`, `roadmap`, `build`) now explicitly states which prior artifacts to read before starting. Claude won't ask users to repeat what's already written.

### Changed

- **Default scaffold location** — framework artifacts now default to `hacky-hours/` subfolder instead of the project root. Pass `--root .` to operate at the root as before. The survey step falls back to the root automatically for existing projects and suggests running `migrate`.
- **No-arg behavior** — `/hacky-hours` (no argument) now runs the full guided session (survey + orient + act) instead of printing the help message. Use `help` for the help message. This makes the no-arg path the natural "just run this and it'll figure out where you are" on-ramp for new users.
- **Help message** reorganized into logical groups: Getting started, Navigate the framework, Release workflow, Utilities. Clearer description of each command's purpose.
- **`/hacky-hours sync`** — redesigned. Now does one thing: publish a GitHub Release from the latest CHANGELOG entry. BACKLOG→Issues and milestone creation removed — these created maintenance burden without meaningful value for the core audience. Sync now: checks `gh` auth, confirms the tag, previews exactly what will be published, and publishes on explicit confirmation.
- **Milestone-complete flow** — when BACKLOG.md empties, now suggests `audit` before `sync` so users catch issues before publishing.
- **Generated project `CLAUDE.md`** — paths updated to `hacky-hours/` prefix; now also suggests `audit` before `sync` on milestone completion.
- **`.claudeignore` defaults** updated to use `hacky-hours/` prefixes.
- **`ARCHITECTURE.md` Claude Guidance** — strengthened with explicit safety-first defaults: managed/hosted before self-hosted, fewer external services, established open-source libraries, cost and data residency implications flagged.
- **`SECURITY_PRIVACY.md`** — added Dependency Security and License Hygiene section; Claude Guidance updated to recommend OAuth/magic links over custom auth, and to cross-reference `LICENSING.md`.
- **`ACCESSIBILITY.md` Claude Guidance** — added "start simple, stay semantic" principle and note on accessible-first UI library selection.
- **`02-design/README.md`** — added `LICENSING.md` row; Claude Guidance updated to read Constraints & Values section first and apply safety-first defaults throughout.
- **Version** bumped to v1.0.0.

---

## [0.9.0] — 2026-03-20

Dogfooding support, sync upgrades, project state machine, and GitHub Action template.

### Added

- **`--root <path>` flag** — all commands now accept `--root <path>` to scaffold and operate in a subdirectory instead of the project root (e.g. `/hacky-hours ideate --root meta/` for dogfooding the framework within its own repo)
- **Generated project `CLAUDE.md`** — scaffolded alongside the level folders; contains state machine instructions so Claude automatically checks GitHub Issues at session start, removes completed items from BACKLOG.md, adds them to CHANGELOG.md, closes linked issues, and prompts the release process when the milestone is done
- **GitHub Action template** — `runbooks/templates/hacky-hours-sync.yml`: a copy-paste workflow that calls the Claude API on PR merge to remove the completed item from BACKLOG.md and add it to CHANGELOG.md automatically
- **`runbooks/github-action-sync.md`** — setup guide for the Action template, including cost, matching logic, and troubleshooting

### Changed

- **`sync` guidance** — upgraded with deduplication (checks for existing issues before creating), issue URL back-linking (records GitHub URL into BACKLOG.md after creation), pre-flight `gh auth status` check, and a post-sync summary

---

*Older entries (v0.1.0–v0.8.0) archived to `hacky-hours/archive/changelog/`.*
