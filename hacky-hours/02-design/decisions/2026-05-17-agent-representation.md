# ADR: Agent representation — team site history + auto-evolving profile + synthetic resume + reflection (Slice 13)

**Date:** 2026-05-17
**Status:** Accepted
**Slice:** 13 (v4.0.0)
**Arbitration mode:** decide (conductor + framework synthesis)

## Context

Slice 12 closed the v4 thesis's *persistence* loop: every multi-role verb captures behavior feedback and history; backfill retroactively populates existing projects; `team update` promotes pending changes. After Slice 12, the data exists.

But the data is invisible. The team site reads `profile.md` and renders static bios. Agents accumulate history with no way to see it. The "agents that learn and grow with context" headline is true in the data layer and false in the user-facing surface. The conductor surfaced this during the Slice 12 confirmation: *"the point of the team site and having these team avatars are that they are learning and growing with context... I want to treat these AI agents like human team members. They will want to make sure they highlight their skills and experience, have reflection, and learn from their work and level up."*

The v4 thesis closes only when the persistence loop *manifests* — when agents appear to a conductor as teammates whose representations reflect what they've done, not static personas with attached logs.

## Roles involved

- **🎨 Felix (Design)** — the user-facing surface. Team site rendering of history (chronological timeline), lessons (durable corrections), and résumés is a design problem before it's a backend one. Cards on the index page surface a level badge; profile pages get track-record and lessons sections; résumés render as standalone pages.
- **🏗️ Priya (Architect)** — schema decisions: where the metrics block lives, what gets derived vs. stored, when refresh fires. Co-locating metrics refresh with history append (same Stash phase, same commit) keeps the team repo log readable. Single `metrics:` block in `profile.md` frontmatter, refreshed by every history-writing operation.
- **📊 Maya (Product)** — scope discipline: the conductor asked for "synthetic resumes" and "treat agents like teammates" with "reflection" and "level up." This expands to four pieces: site rendering, auto-metrics, resume verb, reflection verb. Push for the smallest coherent shipment that delivers all four; defer compaction, agent-to-agent collaboration, and other v4.1+ candidates.
- **📈 Yuki (Data)** — derived fields schema. Level is derived from history count + breadth bumps; projects list is derived from history; verb counts are derived. Conductor doesn't edit metrics — anything they write gets overwritten. Display-only layer, not a source of truth.

## Decision

Slice 13 ships four coordinated pieces, all in v4.0.0:

### 1. Derived metrics block (`metrics:` in profile.md frontmatter)

Auto-managed schema in every agent's `profile.md` frontmatter — `level` (0-5 with breadth bumps), `history_entries`, `projects`, `verbs_run`, `by_verb` counts, `feedback_count`, `last_active`, `metrics_refreshed`, `reflected_at`. Refreshed at end of every multi-role verb's Stash phase (bundled into the same git commit as the history append), and at end of `team backfill` (per-agent batch) and `team reflect`. Spec in `references/capture-format.md` §"Derived metrics" + §"Level derivation".

### 2. Team-site renders history + lessons + résumés + level badges

Un-defer the v4.1+ item. The Python-stdlib generator (`templates/team-site/generate.py`) reads `history.md`, `feedback.md`, the `metrics:` block, and `resume.md` per agent. Profile pages gain:
- Level + contribution count in the header metadata line
- "Recent track record" section with timeline rendering of the last 10 history entries
- "Lessons applied" section with durable feedback notes
- Résumé link (when `resume.md` exists) opening a standalone page

Index page cards gain a level badge (`lvl 3 · 18 contributions · 1 project`) below the existing card body. Agents with no history get no badge — keeps fresh team grids clean.

### 3. Synthetic résumé generation (`/hacky-hours team resume`)

New verb writes `agents/<id>/resume.md` composited from `profile.md` + `system-prompt.md` + `history.md` + `feedback.md` + `preferences.yml`. Structure: header (name, role, level/contributions), summary (distilled from bio + system-prompt), skills (aggregated by verb-type from history), experience (grouped by project, chronological), recent learnings (paraphrased from feedback), profile (verbatim bio). Three style presets: `minimal`, `standard`, `deep`. Fact-derived only — every claim traces to a source; honest about thin work. Spec: `tools/team-resume.md`. Output is a derived artifact — regenerated freely, conductor commits explicitly if they want it tracked.

### 4. Agent self-reflection (`/hacky-hours team reflect`)

New verb. Agent walks their own `history.md` + `feedback.md` + `profile.md` and produces three outputs:
- **Track record section** (silent, fact-of-record) — auto-appended/replaced in `profile.md` Bio. One paragraph per project, third-person past-tense, cites by count. No conductor review (same semantics as forward-capture history append).
- **Prose updates** (conductor-reviewed) — refined Background / How I work / What I produce sections. Each warranted revision writes a `kind: prose_update` pending entry with `target_section` field, reviewed via existing `team update` accept/edit/reject/defer flow.
- **Self-observations** (printed, opt-in to land as behavior feedback) — strengths agent sees in own work, gaps to close. Conductor names items to stash as behavior feedback for next session.

Opt-in only — conductor invokes when they want the look. Not part of Stash phase (which fires automatically end-of-verb). Spec: `tools/team-reflect.md`.

## Rationale

**Why all four in v4.0.0 instead of staged.** The persistence loop is invisible without the user-facing manifestation. Shipping v4.0.0 with Slice 12 alone leaves the headline claim ("orchestra that learns and grows with context") unsupported in the team-site experience. The conductor evaluated and chose "all four" explicitly — same shape as the Slice 11 decision (orchestra audible) and Slice 12 (orchestra remembering): v4.0.0 ships when the thesis is *complete*, not when the underlying mechanics are correct.

**Why hybrid bio editing (auto-rewrite prose + appended track record + derived metrics) instead of one or the other.** The conductor's call. The hybrid balances:
- *Auto-rewrites* keep the bio current with accumulated experience (the "level up" piece) — but require conductor review per section to prevent voice drift
- *Appended track record* is silent and refreshes freely — captures factual project summaries without burdening review
- *Derived metrics* is structured display data, refreshed by every verb without ceremony

Together they cover three review semantics — silent (metrics, track record), conductor-reviewed (prose), and conductor-initiated (self-observations) — matched to the editorial nature of each.

**Why metrics live in `profile.md` frontmatter (not a separate file).** Profile is what the team-site generator already reads. Co-locating metrics avoids a second file read per agent and keeps the canonical "what describes this agent" surface in one place. Conductors who `cat profile.md` see everything about an agent in one place.

**Why metrics refresh fires in the same commit as history append.** Two commits per verb (history + metrics separately) would double team-repo log noise without any review benefit (both are silent). Bundling them keeps the log readable: one commit per verb run, clearly named.

**Why level derivation is breadth-bumpable.** A 100-entry single-project single-verb agent is grindy, not senior. A 20-entry agent across 4 projects and 6 verb types has demonstrated range. The breadth bumps reward range without inflating raw counts. Cap at 5 because levels above that read as fake.

**Why résumés are derived (regenerable) rather than primary artifacts.** A résumé that hand-edits drift independently of the underlying data is a maintenance liability. Deriving from sources means the résumé is always current and can be regenerated freely. Conductors who want a snapshot commit it; conductors who treat it as ephemeral never commit and regenerate on demand.

**Why reflection is opt-in instead of automatic.** Auto-reflection at end-of-verb would add a token-expensive step to every multi-role verb. Reflection's value is in *looking at accumulated work*, which doesn't accrue meaningfully per-verb — it accrues per-week or per-milestone. Conductor-initiated is the right cadence.

**Why prose updates go through `team update` review.** Profile bio is the agent's voice anchor. Auto-rewriting without review risks drift from the starting persona over time. Channeling rewrites through the existing pending-review flow gives conductor a checkpoint per section.

## Consequences

**What changes downstream:**

- Every multi-role verb's Stash phase (step 4) now does history append + metrics refresh in a single commit
- Every agent's `profile.md` will gain a `metrics:` frontmatter block after the first multi-role verb that involves them (no migration required — block springs into existence)
- `templates/team-site/generate.py` is significantly larger (~150 lines added) but still pure stdlib
- The team site goes from "static yearbook" to "living roster" after any meaningful work — the visible manifestation of the v4 thesis
- Two new verbs (`team resume`, `team reflect`) in the `team` subcommand surface
- `tools/team-update.md` now accepts a new `kind: prose_update` in addition to `behavior_feedback` and `prompt_edit`

**What we're committed to:**

- Levels are a public surface — they appear on cards and résumés. Changing the derivation table is a breaking change for conductor expectations (an agent that was level 4 yesterday shouldn't become level 2 today unless they actually shrank). Modify the table only in major releases.
- Résumé and reflection are agent-voice operations. They depend on `profile.md` having a coherent voice baseline. If the bio is empty or generic, the derived outputs will be weak. Default team templates ship with rich bios for exactly this reason.
- Metrics block is auto-managed — conductors who hand-edit will see overwrites. Document this clearly.

**What we're not doing yet (deferred to v4.1+):**

- **History compaction.** Same deferral as Slice 12. When `history.md` exceeds ~500 lines / ~10k tokens, archive older entries. Slice 13 reads `history-archive/*.md` in metrics counts so the architecture is ready, but no archiver runs yet.
- **Agent-to-agent skill recommendation.** "Maya needs an architecture review; Priya is most experienced (level 4 in audit). Want me to engage her?" Real use case once teams accumulate enough variance, but premature now.
- **Resume export to LinkedIn-shape JSON / PDF.** Markdown is the canonical form; export bundling can use `/hacky-hours export markdown-bundle` plus future SSG.
- **Per-project skill maps** (e.g., "this project needed strong A11y review; Lena was level 1 here, suggesting future-Lena projects could benefit from this kind of work"). Cross-project skill inference is a v4.2+ candidate.
- **Reflection auto-cadence triggers.** "It's been N verbs since last reflection — run one?" Not in Slice 13; conductor-initiated.

## Alternatives considered (and not chosen)

- **Skip team-site changes, ship only the verbs.** Rejected — the visible manifestation is the load-bearing piece. Verbs without site rendering produce data files no one looks at.
- **One verb (`team grow` or `team manifest`) instead of two (`resume` + `reflect`).** Rejected — résumé generation and self-reflection have different cadences (résumé on demand vs. reflection at meaningful intervals), different sources (résumé reads everything; reflection focuses on recent history), and different outputs (one file vs. multiple). Separate verbs keep contracts clean.
- **Auto-rewrite bio prose without conductor review.** Rejected per the conductor's hybrid decision — voice drift is a real risk over a long enough timeline, and the per-section review checkpoint is cheap to add.
- **Reflection runs automatically end-of-verb.** Rejected — token cost per verb, value accrues over time, conductor-initiated is the right cadence.
- **Levels are conductor-set, not derived.** Rejected — opens conductor to assigning vanity levels that don't reflect actual work. Derived signal stays honest.
- **Metrics as a separate file (`agents/<id>/metrics.yml`).** Rejected — second file read per agent, splits canonical "describes the agent" surface across multiple files. Frontmatter in `profile.md` is the natural home.
- **Render history on profile page but NOT on cards.** Rejected — cards are the first impression. The level badge on cards is what makes the team site read as a roster of teammates with track records rather than a static directory.

## Related

- Slice 11 (`references/chat-format.md`) — orchestra audible
- Slice 12 (`references/capture-format.md`, `tools/team-update.md`, `tools/team-backfill.md`) — orchestra remembers (the data layer this slice manifests)
- Conductor's confirmation message during Slice 12 wrap-up — the catalyst for this slice
- `tools/team-resume.md`, `tools/team-reflect.md` — the two new verb specs
- `templates/team-site/generate.py` — generator updates
- `references/capture-format.md` §"Derived metrics", §"Level derivation", §"Resume composition", §"Reflection semantics" — the unified schema home
