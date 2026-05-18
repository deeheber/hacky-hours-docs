# /hacky-hours team reflect — agent self-reflection and prose evolution

Agents review their own accumulated work and propose changes to how they present themselves. This is the "learn from work and level up" piece — the framework feature that makes the orchestra act like teammates who grow rather than static personas with growing logs.

When invoked, the named agent reads their own `history.md`, `feedback.md`, and current `profile.md`, then produces:

1. **A "Track record" summary** — auto-appended to `profile.md` Bio (silent, fact-of-record, refreshed at every reflect). Concise per-project summaries of what they've actually done.
2. **Proposed prose updates** — refined Background / How I work / What I produce sections that reflect accumulated experience. Conductor reviews via the same `team update` pending flow used for behavior feedback (accept / edit / reject / defer per section).
3. **Self-identified pattern observations** — strengths the agent sees in their work, gaps they'd want to close. Surfaced for conductor awareness; can land as behavior feedback for next session if conductor agrees.

Reflection is **opt-in per agent.** It does not run automatically at end-of-verb (Stash phase handles that for history append + behavior feedback). Reflection is the conductor saying *"go look at yourself"* — a deliberate moment, not a per-verb tax.

Contract source: `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Reflection semantics".

---

## Step 0 — Pre-flight

1. **Active team:** read project `AGENTS.md` for `team:` field; default to `default`.
2. **Argument parsing:** `/hacky-hours team reflect [flags]`
   - `<agent-id>` — positional; required unless `--all`
   - `--all` — reflect all agents on the team in sequence
   - `--since <YYYY-MM-DD>` — restrict reflection to history entries since this date (default: since last reflection if a `reflected_at` field is in profile.md metrics; otherwise all history)
   - `--track-record-only` — skip prose proposal and self-observation; just refresh the appended Track record section
3. **Agent exists + has history:** for non-`--all`, verify the agent's folder exists and `history.md` has at least one structured entry. If history is empty: print *"Nothing to reflect on yet — `<agent-id>` has no history entries. Run multi-role verbs (audit, design, adopt, etc.) so the agent accumulates work, then reflect."* and exit.

## Step 1 — Read the sources

Read for the active agent:
- `agents/<id>/profile.md` — current full content (frontmatter + Background + How I work + What I produce + any prior Track record section)
- `agents/<id>/system-prompt.md` — for voice anchor; do not modify
- `agents/<id>/history.md` — entries since `--since` (or full file)
- `agents/<id>/feedback.md` — durable corrections (factor into prose proposal)
- `agents/<id>/preferences.yml` — for declared focus areas (factor into Track record)

## Step 2 — Compose the Track record section (always)

Generate a `## Track record` section to append (or replace, if a prior one exists) in `profile.md` Bio. Structure:

```markdown
## Track record

*Auto-refreshed by `/hacky-hours team reflect` on <YYYY-MM-DD>. Reflects <N> history entries across <K> project(s).*

**<project-slug-1>** — <date-range>
<2-3 sentence summary in past tense, third person. What this agent has actually done on this project. Cite by count where useful: "Authored 8 ADRs", "Reviewed 5 audits", "Co-authored DATA_MODEL.md across 3 iterations". Honest about scope and depth.>

**<project-slug-2>** — <date-range>
<...>

<For each project the agent has history in, one paragraph. Ordered most-recent-active first.>
```

**Rules:**

- One paragraph per project. Max 3 sentences each.
- Third person, past tense — reads like a teammate's quarterly self-evaluation, not first-person reflection.
- Cite by count where useful (specific numbers > vague claims).
- Honest about depth: if 80% of contributions on a project were `build:*` commits and 0 were `audit`, don't claim "deep review experience" on that project.
- **No bullets in this section.** Paragraphs read more like teammate prose; bullets read like task lists.

Insert immediately after `## What I produce` (or whichever Bio section is last). If a prior `## Track record` exists, replace it cleanly (everything from `## Track record` to the next `##` heading or end-of-file).

**This section is silent.** No conductor review. It's a fact-summary derived from history, same as the metrics block. Conductor sees it after refresh, can edit `profile.md` directly if it gets anything wrong.

## Step 3 — Refresh derived metrics

Update `profile.md` frontmatter `metrics:` block per `references/capture-format.md` §"Derived metrics". Specifically the `reflected_at` field gets stamped to today's date so future `--since` defaults work correctly.

## Step 4 — Propose prose updates (conductor-reviewed)

If `--track-record-only` was passed, skip this step.

Read the current Background / How I work / What I produce sections. For each section, decide if accumulated history + feedback warrants a revision. Heuristics:

- **Background** — revise if the agent's accumulated work suggests skills, projects, or domains not in the current bio. E.g., if Priya has authored 12 ADRs on a single project, her Background should reference that depth.
- **How I work** — revise if `feedback.md` contains durable corrections that fundamentally change collaboration patterns (e.g., "I'm terser at Tier 1" should land in How I work, not stay buried in feedback).
- **What I produce** — revise if history shows the agent producing artifacts not in the current list (e.g., a new artifact type that wasn't in the starter profile).

**Conservative cadence.** Don't propose rewrites if the diff is purely stylistic or adds nothing material. The bar is: *would a reader of the bio understand the agent more accurately after the change?* If no, skip.

For each section the agent wants to revise, present the proposed change to the conductor via the team-update pending flow. Write to `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the capture-format schema, with `kind: prose_update` and `target_section: <background|how_i_work|what_i_produce>` fields added to the frontmatter:

```yaml
---
captured_at: <ISO timestamp>
session_id: <current>
project: <project-slug>
verb: team-reflect
kind: prose_update
target_section: how_i_work
agent: <agent-id>
status: pending
---

## Context
<one paragraph: what about accumulated history/feedback motivates this revision>

## Current section
<verbatim copy of the existing section content>

## Proposed section
<the agent's proposed replacement, in its own voice>

## Rationale
<one paragraph: how this revision reflects what the agent has actually done or learned>
```

The next `/hacky-hours team update` invocation reads these the same way it reads behavior feedback — accept/edit/reject/defer per section.

## Step 5 — Surface self-observations (no auto-write)

Print to the conductor (does not write to any file directly):

```
=== <Name> (<Role>) — self-observed patterns ===

Strengths the agent sees in its work:
  - <observation 1 with evidence cite>
  - <observation 2>
  ...

Gaps the agent wants to close:
  - <gap 1 with evidence cite>
  - <gap 2>
  ...

Want any of these surfaced as behavior feedback for next session?
  (Name an item or items, or 'none' to skip)
```

For each item the conductor names, write a `kind: behavior_feedback` pending entry (same path/schema as the prose updates above) — these go through `team update` per the existing flow.

## Step 6 — Commit Track record + metrics refresh

After the silent Track record refresh + metrics update:

```bash
cd ~/.hacky-hours/teams/<active>/
git add agents/<agent-id>/profile.md
git commit -m "reflect: <agent-id> @ <date> — track record + metrics refreshed"
```

One commit per agent per reflect invocation. Prose updates that go through `team update` get their own commits via the existing flow.

## Step 7 — Print summary

```
Reflection complete for <Name> (<Role>).

  ✓ Track record section refreshed (covers <N> entries across <K> projects)
  ✓ Metrics refreshed (level: <L>, contributions: <N>)
  → <count> prose updates proposed (review with `/hacky-hours team update`)
  → <count> behavior feedback items proposed (review with `/hacky-hours team update`)

Team repo: 1 commit added (silent refresh). Pending items await your review.
```

## `--all` mode

Loop Steps 1–7 for every agent in `agents/`. Skip agents with empty `history.md`. Print per-agent status as it goes. End with summary across all agents.

Reflections are independent — one agent's reflection doesn't depend on another's. Could run in parallel via Agent tool where available; sequential is fine and bounded by agent count (max 12 in default team).

## Edge cases

- **No prose updates proposed.** Common case when history is recent or thin. Footer prints "0 prose updates proposed — current profile still accurate." No pending file written.
- **All sections need rewriting.** Less common but possible (e.g., after backfilling 3 years of history). Conductor sees three pending entries in `team update` — accept/edit each independently.
- **Conflict with concurrent behavior feedback.** If a `kind: behavior_feedback` pending entry from a forward-capture Stash phase exists for the same agent, and a `kind: prose_update` lands too, `team update` shows them as separate items in the same agent's review queue. Conductor can accept both, neither, or any combination.
- **Profile.md has been hand-edited since last reflection.** Detect via `metrics.reflected_at` < file mtime. Tell conductor: *"Profile has been edited since last reflection. Proceeding will refresh the Track record section (replacing any prior). Other sections are only modified via the pending review you'll see."* Confirm before refresh.
- **Agent has only backfilled history (no forward-captured entries).** Reflection works fine — backfilled entries are valid sources. Track record summary will note dates from the backfilled span; prose updates may not trigger since recent activity is technically zero. Use `--since` if conductor wants reflection on a specific period.

## What this verb closes

Pre-Slice-13 (post-Slice-12): agents accumulate `history.md` entries silently and `feedback.md` durable notes via team update. The team site renders static `profile.md` bios that don't change. Agents have done work but don't appear to have grown.

Post-Slice-13: reflection lets agents *manifest* their growth. Track record sections in `profile.md` show what they've done; prose updates evolve how they describe themselves; self-observations surface patterns the conductor might not have noticed. Combined with the team-site changes (history rendering, level badges, resume links), the orchestra reads as teammates who've been working alongside the conductor — not static personas with attached logs.

## Notes for the assistant running this

- **Reflection is the agent's voice talking about itself.** When composing Track record paragraphs and prose updates, use the agent's `profile.md` voice as baseline — not a uniform framework voice. Maya sounds like Maya in her Track record; Priya sounds like Priya.
- **Honest over flattering.** Same rule as `team resume`. If the agent has done thin work, the Track record paragraph is short. If gaps exist, name them in self-observations.
- **Don't invent.** Every Track record claim and every proposed prose revision should trace to a source (`history.md` entry, `feedback.md` note, accumulated count). If the assistant catches itself reaching for a claim with no source, drop the claim.
- **The bar for prose updates is "more accurate," not "more elaborate."** Bio bloat is a real risk. A prose update that adds three sentences should remove three sentences worth of now-stale content too.
