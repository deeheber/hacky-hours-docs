# BACKLOG.md

**Step 4 — Build** | hacky-hours-docs

Queue of work. Items added during Step 3 / Step 5, removed when their PR merges. Completed work moves to [CHANGELOG.md](./CHANGELOG.md).

Previous milestone (v4.0.0) archived to `archive/BACKLOG-v4.0.0.md`.

---

## 🔥 Hotfix queue (v4.0.x patches, parallel to v4.1 work)

- [ ] **HF1 — Pending-file clobber-suffix protocol.** Update `references/capture-format.md` §"Per-verb implementation responsibilities" to require timestamp-suffixed filenames when a pending file already exists for the same agent + session. v4.0.2 patch. Source: ITERATION-2026-05-22 §C2.
- [ ] **HF2 — `claude resume` skill-reload FAQ note.** One-paragraph addition to `tools/v4-first-run.md` documenting that `claude resume` re-reads skill files from disk. v4.0.2 patch. Source: ITERATION-2026-05-22 §C3.
- [x] ~~**HF3 — Branch protection on `main`.**~~ Done 2026-05-22 — `main` now requires PR; admins included (no escape hatch); force-push + branch-deletion blocked; 0 required approving reviews (solo-maintainer); required-status-checks placeholder for when CI lands. Ops task, no release artifact. Source: ITERATION-2026-05-22 §B5.

---

## 🎯 Next Milestone — v4.1.0

Release pattern: **trunk-based development with feature flags**. Every v4.1 piece lands on `main` disabled-by-default. v4.1.0 release flips defaults to `true` for confirmed-stable features.

Items within a tier are independent and can land in any order; tiers depend on the previous one.

### Tier 0 — Foundation (must land first)

- [ ] **F1 — `features:` block in `~/.hacky-hours/settings.yml`.** Flat schema (see ADR `2026-05-22-feature-flag-layer.md`). Loader machinery in SKILL.md preamble — verbs that branch on a flag read settings and fallback if absent. Default-off in v4.1.x. Adds `profile.plan: pro | max5x | max20x | unspecified` schema with v4-first-run prompt. ADR: feature-flag-layer.
- [ ] **F2 — Token instrumentation hooks.** Per-verb / per-role / per-phase log entries to `~/.hacky-hours/sessions/<id>/cost-log.jsonl`. Schema in `references/cost-instrumentation.md` (new). Always-on; not feature-flagged. Sets up benchmarking for R1. ADR: feature-flag-layer §3.
- [ ] **F3 — `stakes:` field in pending-file frontmatter.** Add `stakes: low | high` (default `high`) to `references/capture-format.md` schema. Add "Stakes rubric" section to the same file. ADR: automated-team-learning §1, §2.

### Tier 1 — Cheap individual features (each behind a flag)

- [ ] **T1.1 — Discovery phase in Step 1.** Add Phase 1.0 to `steps/01-ideate.md` (3 questions: user's current workflow / 5-second homepage gut-check / smallest first-session action). Outputs `01-ideate/DISCOVERY.md`. Add `references/discovery-questions.md`. Lo-fi homepage gate before Step 2 (`01-ideate/HOMEPAGE-SKETCH.md`). Gated by `features.discovery_phase`. ADR: discovery-phase.
- [ ] **T1.2 — Skeptic-mode flag.** Implement `--skeptic` flag any role can adopt. Modal behavior; no new role. Gated by `features.skeptic_mode`. ADR: discovery-phase §4.
- [ ] **T1.3 — Status-update artifact + agent-initiated escalation.** Add `role_event: "status"` and `role_event: "escalation"` schema to `references/capture-format.md` (or new `references/messages-schema.md`). Update each multi-role verb to permit status-update emissions. Add `references/escalation-heuristic.md` for the "when to fire" rubric. Gated by `features.status_updates`. ADR: three-artifact-model §3.
- [ ] **T1.4 — Presentations artifact format spec.** Add `kind: presentation` schema to V4_DESIGN §6 / capture-format.md. Add presentation-generation guidance to Step 2 / Step 5 / audit. Render comes with browser companion (T3.1). Gated by `features.presentations`. ADR: three-artifact-model.
- [ ] **T1.5 — Plan-aware defaults.** Wire `profile.plan` into `role_models` selection. Pro defaults Haiku for licensing + accessibility; preflight prompt fires on heavy verbs. Not flagged; always-on. ADR: feature-flag-layer §2, §3.
- [ ] **T1.6 — Cross-role propagation in `team update`.** Step 3 of `tools/team-update.md` gains "propagate to peer" option. Adds `propagated_from:` field to pending-file frontmatter schema. Gated by `features.cross_role_propagation`. ADR: automated-team-learning §4.

### Tier 2 — Workroom + automated learning (the structural #11 changes)

- [ ] **T2.1 — Workroom verb shape.** Multi-turn agent dialogue persisted to `~/.hacky-hours/sessions/<id>/messages.jsonl`. Schema for `messages.jsonl` rows. Apply to Step 2 (design) first as the proving ground; then Step 5 (iterate), then audit Lane A. Add `workroom_max_turns` + `workroom_role_budget` settings. `/hacky-hours redirect "<note>"` slash command for owner interruption. Gated by `features.workroom_mode`. ADR: workroom-mechanic.
- [ ] **T2.2 — Auto-promote / queue split in `team update`.** Step 1 buckets pending entries by `stakes`. Step 2 presents only `high`. Auto-bucket commits silently with footer summary. Step 6 footer distinguishes auto-promoted vs reviewed counts. Gated by `features.auto_promote_low_stakes`. Depends on F3. ADR: automated-team-learning §3.
- [ ] **T2.3 — End-of-verb auto-debrief.** After Phase N — Stash, run a brief agent-to-agent self-debrief. Each "I would propose…" becomes a `stakes: low` pending entry pre-classified by the agent. Persists as `role_event: "debrief"` in `messages.jsonl`. Gated by `features.auto_debrief`. Depends on T2.1. ADR: automated-team-learning §5.

### Tier 3 — Browser companion (#8)

Can start in parallel with Tier 1; chat surface (T3.5) depends on T2.1 for messages.

- [ ] **T3.0 — Python stdlib generator scaffolding.** Extend `tools/team-site.md` for project workspace output. Set up vendored deps (Mermaid MIT, optional HTMX BSD-2). No feature flag — opt-in via verb args. ADR: browser-companion §1.
- [ ] **T3.1 — Read-only project workspace.** `~/.hacky-hours/companion/<slug>/project/` renders `01-ideate/` through `05-iterate/` as Markdown + inline Mermaid. Left-rail nav. "Edit in your editor" deep-links. ADR: browser-companion §2 surface 3.
- [ ] **T3.2 — Diagram gallery surface.** All ERDs / architecture diagrams / user-journey flowcharts in one Mermaid render page. Click-to-expand. ADR: browser-companion §2 surface 7.
- [ ] **T3.3 — Audit timeline surface.** Traffic-light scorecards rendered visually with trend-over-time. Drill-down to findings. Reads from `hacky-hours/audits/`. ADR: browser-companion §2 surface 6.
- [ ] **T3.4 — Pixel-art avatar bootstrap.** One-shot LLM pass generates 24×24 PNG avatars for all team agents at `team init` time. New `tools/team-avatars.md` spec. Style per-role palette. Fallback: emoji + initials. No flag — one-time install cost. ADR: browser-companion §5.
- [ ] **T3.5 — Slack-style chat surface.** `~/.hacky-hours/companion/<slug>/chat/` renders `messages.jsonl` as Slack-shaped UX. Channel = session. Workspace = project. Per-agent avatar + name/role header + accent color. Threads via `in_reply_to`. Read-only. No flag — opt-in via verb args. Depends on T2.1, T3.4. ADR: browser-companion §3 (the headline).
- [ ] **T3.6 — Multi-workspace switcher + `projects.yml` index.** Auto-populate `~/.hacky-hours/projects.yml` when `adopt` / `ideate` runs in a new directory. Browser chrome left-sidebar lists workspaces. No flag. ADR: browser-companion §4.
- [ ] **T3.7 — Schema-aware fillable forms.** Forms for PRODUCT_OVERVIEW 5Ws, Constraints & Values, ARCHITECTURE quickstart. Submission writes `pending-input.json`; framework reads at next session preamble. Cost-saving move per #10. Gated by `features.forms_writeback`. ADR: browser-companion §2 surface 4.
- [ ] **T3.8 — Backlog kanban with write-back.** Kanban view (Next milestone / Backlog / Done-from-CHANGELOG). Drag-to-reorder writes back to `BACKLOG.md`. Gated by `features.backlog_writeback`. ADR: browser-companion §2 surface 5.
- [ ] **T3.9 — Session monitor surface.** Tails `pending/` + recent `history.md` appends. Auto-refresh. Real-time team-activity view. Gated by `features.session_monitor`. Depends on T2.1. ADR: browser-companion §2 surface 9.

### Tier 4 — v4.1.0 release prep

- [ ] **R1 — Run cost benchmarks.** Across small / medium / large representative projects per TESTING.md "Cost benchmarking" section. Publish `02-design/COST_MODEL.md` with the green/yellow/red feasibility matrix. Author `references/cost-model.yml` for preflight estimates.
- [ ] **R2 — V4_DESIGN.md re-stratification.** Update §8 deferral lists; ensure new locked decisions reflect what actually shipped. (Some Tier 3 phases may slip to v4.2.)
- [ ] **R3 — Flip feature-flag defaults.** Update `settings.yml` template to default-true for confirmed-stable v4.1 features.
- [ ] **R4 — Version bump v4.0.x → v4.1.0.** SKILL.md, VERSION, footer strings, etc. (follow the v4.0.1 pattern).
- [ ] **R5 — Tag v4.1.0 + GitHub release.** Release notes summarize v4.1's six ADRs and the trunk-based feature-flag release pattern.

---

## 📋 Backlog (v4.2+, captured during this iterate cycle)

- History compaction (carried from v4.0.0 deferral; needs trigger + review-cadence design)
- Skeptic as 13th role (escalation from T1.2 modal if signal warrants)
- `verb-prelude.md` reference extraction (DRY win on `references/team-preflight.md` + `chat-format.md` + `capture-format.md` includes)
- Additional silent-overwrite-risk audit (iterate doc writes, ADR date-collision, audit scorecard writes)
- Implicit feedback capture ("override agent N times → write pending implicitly")
- Per-verb stash-mode override in settings.yml (`team_learning.stash_prompt: end_of_verb | end_of_session | off`)
- Agent-to-agent skill recommendation
- Reflection auto-cadence triggers
- Notion / Confluence exporters (v4.3+)
- Cross-language / i18n (v4.3+)
- Multi-team-per-project binding (v4.3+)
- Multi-user collaboration on shared teams (v4.3+)
- Résumé export to non-Markdown shapes (LinkedIn JSON, PDF) (v4.3+)
- Per-project skill maps + cross-project skill inference (v4.3+)
- Hosted browser companion (v4.3+ — currently local-only)
- Marker-file polling for browser → Claude write-back (currently clipboard + `pending-input.json`)

---

## Provenance

This BACKLOG was refilled by `/hacky-hours iterate --root hacky-hours` on 2026-05-22 against the upstream framework after v4.0.1 shipped. Source: `hacky-hours/ITERATION.md` (will be archived as `archive/iteration-2026-05-22.md` when this cycle closes).

Six ADRs in `02-design/decisions/` anchor the v4.1 design:
- `2026-05-22-feature-flag-layer.md`
- `2026-05-22-workroom-mechanic.md`
- `2026-05-22-three-artifact-model.md`
- `2026-05-22-automated-team-learning.md`
- `2026-05-22-browser-companion.md`
- `2026-05-22-discovery-phase.md`
