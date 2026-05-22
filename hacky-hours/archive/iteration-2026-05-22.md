# ITERATION — post-v4.0.1 cycle (2026-05-22)

**Status:** Phase 1 — Capture
**Triggered from:** v4.0.1 release (Hacky Hours #7 fix shipped); three open issues remain on the upstream tracker.
**Conductor:** bjamba

This iteration is unusual in that the dogfooded project IS the framework itself, and the founder has filed structural critiques against the framework via the framework. Three issues are open and assigned, and they're tightly coupled in ways the original filing didn't fully surface.

---

## Source signals

### A. Open GitHub issues against `empathetech/hacky-hours-docs`

#### A1 — #11 Team interaction model: the conductor should orchestrate, not micromanage

Filed today, 2026-05-22. The team is structurally a *contractor team* — agents speak only when invoked; the conductor (Claude) routes everything through the owner; documents are walls of text. Owner has no offstage space for the team to interrogate framing.

Evidence: two recent projects had framing-level misses (video-game-pomodoro's "Mario" vs. SMB2 USA Subcon, reciprocator's "pathing tool" vs. "explorer with pathing"). Both required the founder to catch, not the team.

**Six proposed changes** (coupled):
1. Workroom-style verb runs — multi-turn agent conversation among themselves, owner sees digest
2. Status updates + agent-initiated escalation, not approval requests
3. Continuous agent-to-agent learning, auto-promote low-stakes / queue high-stakes
4. Three artifact layers: deep docs (existing) + presentations (new) + status updates (new)
5. Discovery/framing inside the workroom + lo-fi homepage prototype gate before architecture
6. Anti-drift mechanism — skeptic role + framing-level review queue

#### A2 — #10 Token cost + plan-aware defaults

Filed 2026-05-20 by founder. Hacky Hours has been dogfooded on Claude Max only. Pro-plan feasibility unknown. Eleven concrete deliverables: benchmark methodology, instrumentation, plan-aware defaults via `profile.plan` schema, preflight cost estimate, graceful degradation, cheaper-model defaults for cheap roles (Haiku), cache-aware sequencing, `features:` toggle block, published per-verb cost data.

The `features:` block is THE foundational deliverable — it lets the framework feature-flag heavier mechanisms (`multi_role_fan_out`, `phase_n_stash`, etc.). Trunk-based development with feature flags is the natural release pattern for the v4.1 cycle.

#### A3 — #8 RFC: Browser companion

Filed 2026-05-20. Build a local browser companion as a workspace around the conversation. **Hard constraint: zero additional API spend.** Python stdlib generator, vanilla HTML/CSS, vendored Mermaid, optional HTMX. Eight surfaces: home, team browser, project workspace, schema-aware fillable forms, backlog kanban, audit timeline, diagram gallery, session monitor.

Phased: read-only workspace → forms → backlog write-back → session monitor.

#### A3.1 — Owner addition (2026-05-22, iterate Phase 1): Slack-style team chat surface

The browser companion should include a **read-only Slack-style chat surface** as a new (9th) primary surface. Shape:

- **Workspace = repo / project.** The active project is the workspace; team-memory contains the other workspaces the user can switch between (multi-workspace switcher in the chrome, like Slack's workspace bar).
- **Channels = sessions.** Each `~/.hacky-hours/sessions/<session-id>/` becomes a channel. Channel name and description are derived from the session metadata (verb + project slug + date — e.g., `#design-reciprocator-may19`). Description quickly tells you what was being worked on.
- **Messages = multi-agent dialogue + status updates.** When `team_chat: minimal | full`, the multi-role voice turns get persisted as channel messages with attribution. Status updates (the new #11 artifact type) appear as messages in the relevant session channel. Threads emerge naturally where agents reply to each other.
- **Per-agent identity is highly distinguishable.** Each agent has:
  - **A pixel-art avatar** generated at team-init time (one-time bootstrap, no per-use API cost — fits the "zero-API-spend" constraint). Style instinct: 16×16 or 24×24, palette informed by the role (e.g., security in muted slate, design in warm pastel, ops in toolbox-industrial). Stored in the team repo at `~/.hacky-hours/teams/<name>/agents/<id>/avatar.png` and committed with the rest of the agent's files.
  - **Name + role in a header signature** for every message (e.g., *"🏗️ Priya Chen · Architect"*).
  - **Consistent color band or per-agent accent** so the eye can pick out who's speaking without re-reading the signature.
- **Read-only.** No write-back. The companion never injects messages into a conversation — it only renders what the framework already produced.
- **Searchable** (Cmd-F in the browser is enough at MVP; vanilla JS index for V1+).
- **Persists.** Conversations don't expire — old channels stay browsable even after the conversation has been compacted in the agent loop. The session folder is the source of truth.

Why this is load-bearing for #11:

- **Solves transcript-vs-digest** elegantly: chat IS the transcript; presentations IS the digest. The owner doesn't have to choose at design time — both are produced, the owner picks which to look at when.
- **Solves "show your work":** the team's multi-agent conversation is preserved and scrollable, attributable, threaded.
- **Solves status-update artifact:** status updates are channel messages.
- **Solves the "team feels like consultants, not a team" critique:** seeing your team in Slack-shape makes them feel like coworkers in a way reading their bios doesn't.

Implementation hooks:
- Pixel-art generation is a **one-time bootstrap** during default-team-init (or `team new`). Could use the same one-shot LLM pass that creates the team in the first place — counts as install cost, not per-use cost.
- Channel population requires the multi-role conversation transcripts to actually be *persisted* to disk per-verb-run, which today only partially happens. Probably wants its own pending-message-shape in `sessions/<id>/messages.jsonl` or similar.
- Multi-workspace switching needs the companion to enumerate available teams from `~/.hacky-hours/teams/` and projects from somewhere (project index? probably a new file at `~/.hacky-hours/projects.yml`?).

### B. Insights from this iteration cycle's dogfooding

#### B1 — #8 and #11 are two views of one capability

**#11 defines new artifact types:** presentations (review checkpoints), status updates (day-to-day).
**#8 is the natural rendering surface:** project workspace, diagram gallery, session monitor.

You can't ship #11 without #8 (presentations rendered as markdown in scrollback defeat their purpose). You don't want to ship #8 without #11 (you'd render existing artifacts beautifully but never add the new artifact types the framework actually needs). They're one capability, two issues.

#### B2 — #10's `features:` block is the cross-cutting discipline

Every new mechanism #11 adds is MORE multi-role fan-out, which is exactly what #10 wants to feature-toggle. If we build #11 without #10's discipline, we make the framework less accessible on Pro — the opposite of #11's intent (owner cognitive load reduced; not shifted to wallet load).

`features:` should land *first* — before any #11/#8 mechanism — so every subsequent piece ships behind an off-by-default flag. The v4.1.0 release becomes "flip the defaults to true," not a big-bang merge.

#### B3 — #8 partially solves #10's cost problem

Schema-aware forms (#8 surface 4) move structured design-doc input out of LLM turns entirely. That's a direct cost win for the cost problem #10 names. The two efforts compound — #10 references this explicitly.

#### B4 — Release strategy: trunk-based with feature flags, NOT long-lived feature branch

Long-lived `feat/v4.1` would cost a lot in drift, conflicts, and "review the whole thing at once" reviewer fatigue. The featureflag layer (from #10) is the better-shaped lever:

- v4.0.x patches ship #7-style fixes during the v4.1 cycle
- Every #11/#8 piece lands on main as a small PR behind an off-by-default flag
- v4.1.0 release just flips the defaults

#### B5 — Branch protection / signing / CI for the upstream repo

Currently nothing prevents direct-to-main pushes on the upstream repo. For a release-engineering framework, the upstream repo itself should model the discipline it teaches:
- Branch protection on `main` requiring PR review (one-person rule: I can self-approve via gh CLI overrides if needed, but the default is PR-required)
- Required CI checks before merge
- Signed tags for releases

Light task but worth doing alongside the bigger work.

### C. Specific frictions observed during this session

#### C1 — `team update` interaction is fully owner-driven

Every behavior-feedback note has to be conductor-nominated and owner-approved. No auto-promotion of low-stakes patterns. No cross-role propagation (Felix learned a principle on pomodoro; Maya didn't get it because the update mechanism only modifies one bio at a time).

#### C2 — Behavior-feedback file path can be silently clobbered

Wrote `~/.hacky-hours/sessions/2026-05-19-reciprocator/pending/security.md` twice in this session (once with regulated-practice content, once with scaffold-time-security content). The second write overwrote the first. The first write had already been promoted, so no data loss this time — but the pattern is dangerous.

Fix: behavior-feedback pending files should be append-suffixed (`security-1.md`, `security-2.md`) or timestamped (`security-2026-05-22T1330.md`).

#### C3 — `claude resume` skill-reload behavior was unknown

Took some back-and-forth to determine that `claude resume` re-reads skill files on restore. This should be documented somewhere. Probably in `tools/v4-first-run.md` or `tools/upgrade.md` (or a new note in CHANGELOG-of-CHANGELOG).

#### C4 — Conductor lacks an in-band way to opt OUT of process ceremony

When the owner says "do the thing that protects us in the future" (a clear directive), the conductor still asks "a a / a r / r a / defer?" instead of just executing. Need a "trust me, just do it" affordance that's distinct from "yes/no."

This is half a #11 issue and half a separate friction. May factor naturally into #11's status-update / escalation model.

#### C5 — `references/team-preflight.md` was a small extraction win

The #7 fix introduced a shared-preamble pattern (`references/team-preflight.md` imported by 7 verbs). This is a good precedent: more cross-cutting concerns could be similarly extracted. Candidates: chat-format.md inclusion (current — already extracted), capture-format.md inclusion (current — already extracted). Next candidate: a `verb-prelude.md` that combines preflight + chat-format + capture-format references in one include.

#### C6 — Pending-file overwrite isn't the only silent-clobber risk

Other places where multiple writes to the same path could silently overwrite: amendment writes during iterate, ADR writes if two cycles share a date, history.md (currently append-only, safe). Worth a small audit.

### D. Open questions — to be answered during synthesis / amendment

These are open at capture time but per owner directive (2026-05-22) must be answered during the iterate cycle, not deferred:

- **Transcript vs. digest persistence:** ✅ resolved by A3.1 above — both are produced. Transcript lives in the Slack-style chat surface; digest is the presentation artifact (#11 piece 4). Owner picks which to consult.
- **Auto-promote stakes boundary** (from #11): what's "craft" vs. "framing"? Likely a `stakes:` field in the pending-file frontmatter — `low` auto-promotes, `high` queues for review. Synthesis decides on the categorization rubric.
- **Skeptic role** (from #11): real 13th role, or modal flag any role can adopt? Implementation-shape matters — affects whether team rosters need a new agent definition.
- **Discovery as a Step 1.5 vs. integrated into Step 1:** new step that fires between Step 1 and Step 2, or a new phase inside Step 1?
- **`features:` block schema:** flat (each feature is a bool) or hierarchical (groups of related features)? Hierarchical is more flexible but more cognitive overhead.
- **Pixel-art generation pipeline** (from A3.1): one-shot LLM during team init? Pre-generated avatars committed to the framework repo? Per-team-tier palette?
- **Multi-workspace index** (from A3.1): where does the list of projects-the-team-has-worked-on live? `~/.hacky-hours/projects.yml`? Derived from team `history.md` aggregation?
- **Message persistence schema** (from A3.1): `sessions/<id>/messages.jsonl` per-verb-run? When? Who writes? Today the multi-agent dialogue is *not* persisted to disk except as fragments (Stash notes, audit findings); a load-bearing change for #11+#8 unified is producing structured per-message records.

---

## Notes for synthesis (Phase 2)

When synthesizing, the design docs most likely to need amendment:

- **`02-design/V4_DESIGN.md`** — the load-bearing one. §4 (Locked Decisions) probably needs new entries for: workroom mechanic (#11 piece 1), three-tier artifact model (#11 piece 4), feature-flag layer (#10), browser companion (#8). Possibly amends or supersedes existing decisions.
- **`02-design/ARCHITECTURE.md`** — possibly needs a new section for the browser companion (#8) and how it interacts with the skill files on disk.
- **`02-design/SECURITY_PRIVACY.md`** — probably stable; browser companion's "zero API spend" and "no LLM calls" is a feature-level decision, not a privacy posture change.
- **`02-design/TESTING.md`** — possibly needs a new section on benchmark methodology + token instrumentation (#10).
- **`tools/team-update.md`** — needs the auto-promote / queue / cross-role propagation flow from #11 piece 3.

ADRs anticipated:
- `2026-05-22-feature-flag-layer.md` — adopt trunk-based-with-feature-flags as the v4.1 release pattern
- `2026-05-22-workroom-mechanic.md` — multi-role workroom verbs that produce digests + open-question lists
- `2026-05-22-three-artifact-model.md` — deep docs + presentations + status updates
- `2026-05-22-browser-companion-phase-1.md` — read-only project workspace as the first piece of #8

---

---

## Phase 2 — Synthesis findings (2026-05-22)

For each captured item, the design-doc surface that needs amendment and the rough shape. Many items co-locate into single new sections; some need cross-cuts.

### Amendments to `02-design/V4_DESIGN.md`

V4_DESIGN.md is the load-bearing target. §4 already runs through §4.22; v4.1 work adds new locked decisions:

| New § | Title | Drives | ADR | Captures |
|---|---|---|---|---|
| 4.23 | Feature-flag layer | #10 deliverable: `features:` block in settings.yml + per-feature defaults | `2026-05-22-feature-flag-layer.md` | A2, B2, B4 |
| 4.24 | Workroom mechanic — team-as-workroom, owner-as-reviewer | #11 piece 1 | `2026-05-22-workroom-mechanic.md` | A1 (1), B1 |
| 4.25 | Three-artifact model — deep docs + presentations + status updates | #11 piece 4 | `2026-05-22-three-artifact-model.md` | A1 (4), B1, A3.1 |
| 4.26 | Automated agent-to-agent learning + auto-promote/queue split + cross-role propagation | #11 piece 3 | `2026-05-22-automated-team-learning.md` | A1 (3), C1, D (stakes boundary) |
| 4.27 | Status-update artifact + agent-initiated escalation | #11 piece 2 | (folds into §4.25 ADR) | A1 (2), C4 |
| 4.28 | Browser companion — architecture overview, zero-API-cost constraint, phased delivery | #8 RFC | `2026-05-22-browser-companion.md` | A3, A3.1, B1, B3 |
| 4.29 | Slack-style team chat surface (sub-decision under §4.28 or peer-decision; need to decide during amendment) | #8 new owner addition | (folds into §4.28 ADR) | A3.1, D (multi-workspace index, message persistence) |
| 4.30 | Discovery / framing-interrogation phase | #11 piece 5 | `2026-05-22-discovery-phase.md` | A1 (5), D (Step 1.5 vs. integrated) |
| 4.31 | Skeptic role / anti-drift mechanism | #11 piece 6 | (folds into §4.30 ADR or stands alone — decide during amendment) | A1 (6), D (skeptic shape) |

**§5 (Role Roster) amendment:** if §4.31 lands the skeptic as a 13th role, the Core 12 becomes Core 13 (or Core 12 + 1 modal). Otherwise no roster change.

**§6 (Operations & State Files) amendments:**
- Add `sessions/<id>/messages.jsonl` — structured per-message persistence for the workroom mechanic + Slack-style chat surface (captures D-message-persistence).
- Add `~/.hacky-hours/projects.yml` — multi-workspace index (captures D-multi-workspace).
- Add `companion/` output path under `~/.hacky-hours/` for browser-companion static build.

**§8 (Deferred to v4.1+) amendments:**
- Most items remain deferred to v4.2+ (Notion/Confluence exporters, multi-team-per-project binding, i18n, multi-user collaboration).
- Promote IN: feature-flag layer, presentations artifact, status-update artifact, automated team learning, browser companion phase 1, slack-style chat surface.
- §8 should be re-stratified as v4.1 / v4.2 / v4.3+ buckets.

**§10 (Risks Being Held Consciously) amendments:**
- Add: "Cost-of-fan-out for workroom mode" (mitigated by feature flags + the Pro-feasibility framing from #10).
- Add: "Trust-as-default failure mode" — when the team gets it wrong, the owner has to catch it via the presentation layer; recovery path needs spec (captures D-trust-failure).
- Add: "Pixel-art bootstrap as one-time cost" — if a user runs `team new` and pixel art can't be generated (no API, network down), team is still functional. Document the fallback.

### Amendments to `02-design/ARCHITECTURE.md`

- New section: **"Browser Companion"** — describes the static-HTML generator (Python stdlib), the read-only/write-back boundary, the handoff patterns to Claude (clipboard, `pending-input.json`, marker-file polling). Includes the Slack-style chat surface as a sub-component.
- **"Key Components"** gets a feature-flag layer entry — describes how `features:` block is consumed by verb files and skill includes.
- **"Release Process"** gets a note about trunk-based-with-feature-flags being the v4.1 release pattern (and the rationale — coupling concerns from #11+#8+#10).

### Amendments to `02-design/TESTING.md`

- New section: **"Cost benchmarking + token instrumentation"** — methodology, instrumentation hooks, representative-project taxonomy, feasibility matrix shape. Captures #10's first three deliverables.
- **"Testing Layers"** gets an entry for the new workroom verbs — how a workroom multi-turn agent conversation is testable (probably: snapshot-style transcript fixtures with role attribution).
- **"What We Don't Test"** stays honest — we don't test the LLM output itself, only the framework's plumbing around it.

### Amendments to `tools/team-update.md`

Significant rework for #11 piece 3 (auto-promote / queue / cross-role propagation):
- Step 1 (Collect pending changes) — read `stakes:` field from each pending file; bucket into `auto-promote` and `review-required`.
- Step 2 (Present to conductor) — show review-required items only; auto-promote items committed silently with a footer summary.
- Step 3 (Per-change review) — only for review-required. Adds new option: "propagate to peer" — when accepting, ask "which other agents should consider this principle?" and write parallel pending files for those agents.
- Step 6 (confirmation footer) — distinguish auto-promoted count vs reviewed count.

### Amendments to `references/capture-format.md`

- Add `stakes: low | high` to the pending-file frontmatter schema (default `high` for safety).
- Add `propagated_from: <agent-id>` annotation when an entry is created via cross-role propagation.
- Add a "Stakes rubric" section: what counts as craft (`low`, auto-promotable) vs framing (`high`, queue for review).

### Smaller / housekeeping items

- **C2 (pending-file clobber risk):** verb files writing to `pending/<agent-id>.md` should append-suffix on collision. Update `references/capture-format.md` §"Per-verb implementation responsibilities" to specify timestamp-suffixed filenames when a pending file already exists for that agent in the same session.
- **C3 (`claude resume` skill-reload behavior unknown):** add a one-paragraph note to `tools/v4-first-run.md` (or a new `references/installation-faq.md`) documenting that `claude resume` re-reads skill files on restore.
- **C5 (`references/team-preflight.md` precedent):** consider extracting a `references/verb-prelude.md` that bundles preflight + chat-format + capture-format includes. Defer to v4.2; not load-bearing for v4.1.
- **C6 (other silent-overwrite risks):** audit `tools/iterate.md` (ITERATION.md write protocol), ADR writes (date-collision shape), audit scorecard writes. Probably small fixes — could land as a v4.0.x patch alongside v4.1 work.
- **B5 (branch protection on upstream):** light task. Set up `main` branch protection on `empathetech/hacky-hours-docs` requiring PR review + green CI before merge. Not a framework change; an ops change. Land as soon as it's safe (after v4.1 work doesn't need direct-to-main pushes).

### Items that don't need a doc amendment

- **A1 piece 6 — anti-drift mechanism:** if it stands alone (§4.31), then yes — own ADR. If folded into §4.30, no new amendment.
- **D (transcript vs digest):** ✅ resolved by A3.1 (chat = transcript; presentation = digest). No additional amendment needed beyond §4.25 + §4.28.
- **B3 (#8 partially solves #10's cost problem):** captured implicitly in §4.27 (forms move structured input out of LLM turns). No standalone doc change.

### Synthesis summary

- **5 new ADRs:** feature-flag-layer, workroom-mechanic, three-artifact-model, automated-team-learning, browser-companion, discovery-phase. Potentially a 6th for skeptic role if it stands alone (workroom-mechanic ADR can absorb otherwise).
- **9 new V4_DESIGN.md locked-decision sections** (§4.23 through §4.31).
- **3 other design docs amended** (ARCHITECTURE, TESTING, team-update).
- **2 reference files amended** (capture-format, possibly verb-prelude added in v4.2).
- **2 housekeeping notes** (clobber-suffix protocol, claude-resume FAQ) plus the **upstream branch protection ops task**.

This is a substantial v4.1 design surface. Even with feature flags allowing incremental ship, it's ~6 weeks of v4.1.x patches before the v4.1.0 "flip defaults" release.

---

## Phase 3 — Prioritize (2026-05-22)

Three buckets per the iterate spec. Release pattern is **trunk-based with feature flags** — every v4.1 piece lands on `main` disabled-by-default; v4.1.0 release flips defaults. The feature-flag layer (F1) is the prerequisite that unlocks everything else; landing it first is non-negotiable.

### 🔥 Hotfix queue (ships in v4.0.x patches, parallel to v4.1 work)

These are small, no-feature-flag, ship-when-ready:

| Item | Source | Effort | Notes |
|---|---|---|---|
| **HF1 — Pending-file clobber-suffix protocol** | C2 (silent-overwrite risk) | 1 PR, hours | Update `references/capture-format.md` §"Per-verb implementation responsibilities" to require timestamp-suffixed filenames when a pending file already exists for the same agent + session. v4.0.2 patch. |
| **HF2 — `claude resume` FAQ note** | C3 (skill-reload behavior was unknown) | 1 PR, hours | One-paragraph addition to `tools/v4-first-run.md`. v4.0.2 patch. |
| **HF3 — Branch protection on `main`** | B5 (upstream repo discipline) | Ops task, not a code change | Configure on GitHub: require PR review + green CI. Land *before* v4.1 work to model the discipline we teach. |

### 🎯 Next milestone — v4.1.0

Sequenced into tiers. Items within a tier are independent and can land in any order; tiers depend on the previous one.

#### Tier 0 — Foundation (must land first; blocks v4.1 work)

| # | Item | Source | Captures | ADR |
|---|---|---|---|---|
| **F1** | `features:` block in `settings.yml` + per-feature defaults + loader machinery in SKILL.md preamble | #10 deliverable | A2, B2, B4 | feature-flag-layer |
| **F2** | Token instrumentation hooks (per-verb, per-role, per-phase) → local log for self-audit | #10 deliverable 2 | A2 | (part of feature-flag-layer ADR) |
| **F3** | `stakes:` field in pending-file frontmatter + Stakes rubric in `capture-format.md` | A1 piece 3, D | C1 | (folds into automated-team-learning ADR) |

#### Tier 1 — Cheap individual features (each behind a flag)

| # | Item | Depends on | Feature flag |
|---|---|---|---|
| **T1.1** | Discovery phase added to Step 1 (§4.30) — owner-facing "what does the user do today" questions before synthesis | F1 | `features.discovery_phase` |
| **T1.2** | Skeptic-mode flag (`--skeptic` any role can invoke) (§4.31) | F1 | `features.skeptic_mode` |
| **T1.3** | Status-update artifact format spec + agent-initiated escalation heuristic (§4.27) | F1 | `features.status_updates` |
| **T1.4** | Presentations artifact format spec (§4.25 partial — schema only, render comes with browser companion) | F1 | `features.presentations` |
| **T1.5** | Plan-aware defaults — `profile.plan` schema + cheap-role model overrides (Haiku for licensing/a11y) | F1 | (always-on; not flagged) |
| **T1.6** | Cross-role `propagated_from:` annotation + `team-update` Step 3 propagation peer-ask | F3 | `features.cross_role_propagation` |

#### Tier 2 — Workroom + automated learning (the structural #11 changes)

| # | Item | Depends on | Feature flag |
|---|---|---|---|
| **T2.1** | Workroom verb shape — multi-turn agent dialogue persisted to `sessions/<id>/messages.jsonl` (§4.24) | F1, T1.3, T1.4 | `features.workroom_mode` |
| **T2.2** | Auto-promote/queue split in `team-update` (Step 1: bucket by stakes; Step 2: present queue only) | F3 | `features.auto_promote_low_stakes` |
| **T2.3** | End-of-verb self-debrief — automatic, agent-to-agent, produces zero or more proposed bio updates | T2.1, T2.2 | `features.auto_debrief` |

#### Tier 3 — Browser companion (#8 — can start in parallel with T1; depends on T2.1 for chat content)

| # | Item | Depends on | Feature flag |
|---|---|---|---|
| **T3.0** | Python stdlib generator scaffolding extended for project workspace (extends `team site`) | F1 | (no flag — opt-in via `team site project`) |
| **T3.1** | Read-only project workspace (#8 Phase 1) — markdown + Mermaid render of `01-ideate/`, `02-design/`, `03-roadmap/`, `04-build/` | T3.0 | (no flag) |
| **T3.2** | Diagram gallery (#8 surface 7) | T3.0 | (no flag) |
| **T3.3** | Audit timeline (#8 surface 6) | T3.0 | (no flag) |
| **T3.4** | Pixel-art avatar bootstrap — one-time generation at team-init or via `team avatars` opt-in | T3.0 | (no flag; one-time API cost) |
| **T3.5** | Slack-style chat surface (§4.29) — channels=sessions, workspaces=projects, pixel-art identities | T2.1 (messages.jsonl), T3.4 (avatars) | (no flag — opt-in via `team site project --chat`) |
| **T3.6** | Multi-workspace switcher + `~/.hacky-hours/projects.yml` index | T3.0 | (no flag) |
| **T3.7** | Schema-aware fillable forms + `pending-input.json` handoff (#8 Phase 2 — cost-saver per B3) | T3.0 | `features.forms_writeback` |
| **T3.8** | Backlog kanban with drag-to-reorder write-back (#8 Phase 3) | T3.0 | `features.backlog_writeback` |
| **T3.9** | Session monitor surface (#8 Phase 4 — tails pending/ + history.md) | T2.1, T3.0 | `features.session_monitor` |

#### Tier 4 — v4.1.0 release prep

| # | Item |
|---|---|
| **R1** | Cost benchmarks run against representative projects (small / medium / large) per #10 deliverable 3. Publish feasibility matrix (verb × plan-tier × green/yellow/red) in `02-design/COST_MODEL.md`. |
| **R2** | Update V4_DESIGN.md re-stratification (§8 deferral lists, new locked decisions reflect what shipped) |
| **R3** | Flip feature-flag defaults in `settings.yml` template — confirmed-stable features default ON in v4.1.0 |
| **R4** | Version bump v4.0.x → v4.1.0 across SKILL.md, VERSION, footer strings, etc. |
| **R5** | Tag v4.1.0 + GitHub release notes |

### 📋 Backlog (v4.2+, not v4.1.0)

Items captured as relevant but explicitly NOT in v4.1.0:

- **History compaction** (carried from v4.0.0 deferral) — needs design for trigger + review cadence
- **Skeptic as 13th role** (escalation from T1.2 modal if signal warrants)
- **`verb-prelude.md` reference extraction** (C5 — DRY win, not load-bearing)
- **Audit additional silent-overwrite risks** (C6 — iterate doc writes, ADR date-collision, audit scorecard writes)
- **Notion / Confluence exporters** (carried from v4.0.0 deferral)
- **i18n / cross-language** (carried)
- **Multi-team-per-project binding** (carried)
- **Multi-user collaboration on shared teams** (carried)
- **Agent-to-agent skill recommendation** ("Maya needs an architecture review; Priya is level 4. Engage her?") — carried from §4.22
- **Résumé export to LinkedIn JSON / PDF** — carried
- **Per-project skill maps + cross-project skill inference** — carried
- **Reflection auto-cadence triggers** — carried

### Estimated v4.1.0 timeline

At solo-developer pace with feature-flag-protected incremental ship:

| Block | Duration | Output |
|---|---|---|
| Tier 0 (F1+F2+F3) | ~1 week | First v4.1.x patches; foundation lands |
| Tier 1 (T1.1–T1.6) | ~2 weeks | Six small patches; most pieces parallelizable |
| Tier 2 (T2.1–T2.3) | ~2 weeks | Workroom + auto-debrief; the biggest structural change |
| Tier 3 (T3.0–T3.9) | ~3 weeks | Browser companion in phased deliverables; pixel-art generation is a one-shot |
| Tier 4 (R1–R5) | ~1 week | Benchmarks, defaults flip, release |
| **Total** | **~9 weeks** | v4.1.0 ships |

The slack-style chat surface (T3.5) is the *headline* of v4.1.0 — most visible to users, biggest demo-able win. Sequencing makes it land roughly in week 7 of the cycle.

*End of Phase 3 — Prioritize. Moving to Phase 4 — Amend design docs + ADRs.*
