# Team Learning Capture — contract

Canonical format spec for v4's team-learning persistence. Referenced by every multi-role verb. **Read this before completing any verb that fans out to roles.**

This file specifies *how* feedback and history get captured so that `/hacky-hours team update` (and the silent `history.md` writer) work end-to-end. Without these mechanics, agents never learn — the slots exist, the team site renders bios, but the bios never change. With them, the team grows.

Design source: `hacky-hours/02-design/V4_DESIGN.md` §4.21.

---

## What capture covers

Two distinct things, captured at the same moment (end of every multi-role verb):

| Slot | Goes to | Review required? | Why |
|------|---------|------------------|-----|
| **Behavior feedback** | `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` | Yes — conductor must accept via `/hacky-hours team update` | A behavior change is editorial. The conductor's intent at capture time may not be their intent days later. |
| **Project history** | `~/.hacky-hours/teams/<active-team>/agents/<agent-id>/history.md` | No — silent append | A history entry is a fact ("Maya worked on adopt at hacky-hours-docs on 2026-05-17"). You can't reject a fact. |

Behavior feedback goes through the team-update review loop. History entries land directly in the agent's `history.md` in the team repo and are committed at end-of-verb.

---

## Session ID resolution

Capture writes to `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md`. The session ID is stable for the duration of a Claude Code session, then a new one is generated.

Resolution algorithm (run on first capture or first history-append in a verb invocation):

1. Read `~/.hacky-hours/sessions/.current-session` if it exists.
2. Check the file's `mtime`. If absent OR older than **4 hours**, treat the session as stale.
3. If stale or missing: generate a new session ID — format `YYYY-MM-DD-HHMM-<4hex>` (e.g. `2026-05-17-2214-a1b2`). Write it to `.current-session`. Touch the mtime.
4. If fresh: reuse the existing session ID. Touch the mtime so the 4h window slides forward.
5. Ensure `~/.hacky-hours/sessions/<session-id>/pending/` and `.../resolved/` exist (`mkdir -p`).

**Why 4 hours and not something tied to the Claude Code process lifetime?** Skills can't reliably detect process boundaries. 4 hours is long enough that a normal work session stays cohesive, short enough that yesterday's stash doesn't get conflated with today's. The mtime touch on every capture means an active session keeps its ID indefinitely; a gap of 4+ hours starts a fresh one.

A conductor can force a new session anytime by deleting `.current-session`. The framework does not surface this — it's an escape hatch for users who notice the mechanic.

---

## `pending/<agent-id>.md` schema

`<agent-id>` is the folder name from `~/.hacky-hours/teams/<team>/agents/` — i.e. the lowercase role name: `architect`, `security`, `product`, `ai-ml`, etc. **Use the folder name, not the character's first name.** This is the same identifier `team-update.md` reads and the same one used in tier.yml.

Schema:

```markdown
---
captured_at: 2026-05-17T22:14:00-07:00
session_id: 2026-05-17-2214-a1b2
project: hacky-hours-docs        # basename of cwd
verb: audit                       # the verb that fanned out
kind: behavior_feedback           # behavior_feedback | prompt_edit
agent: architect                  # role folder name
stakes: high                      # low | high — drives team-update auto-promote behavior (v4.1+)
propagated_from: ~                # optional: agent-id this entry was propagated from (v4.1+ cross-role)
status: pending                   # pending | accepted | rejected | deferred
---

## Context

<one paragraph: what the conductor was doing when this got captured — pulled from the verb's run, not invented. E.g., "During audit of hacky-hours-docs at Tier 1, Priya was the architect lane reviewing the v4 persistence story. Conductor noted that her report leaned hard on schema talk before any concrete file paths, which slowed the read.">

## Proposed change

<the conductor's actual words from the Stash prompt, lightly transcribed for clarity but never invented or expanded. If the conductor said "Priya — lead with file paths next time," that's what goes here, verbatim or near-verbatim.>
```

**Frontmatter rules:**
- `captured_at` — ISO 8601 with timezone.
- `kind` — `behavior_feedback` for "do X differently next time"; `prompt_edit` only if the conductor explicitly edited an agent's `system-prompt.md` mid-session.
- `stakes` (v4.1+) — `low` (craft / convention / tooling preference; auto-promotable when `features.auto_promote_low_stakes: true`) or `high` (framing / judgment / architectural default; queue for owner review). **Default `high`** when absent. See "Stakes rubric" section below.
- `propagated_from` (v4.1+, optional) — when this pending entry was created via cross-role propagation in `team update` Step 3, the original agent-id whose accepted entry triggered the propagation. Surfaces in review so the conductor can see the chain.
- `status` — always starts `pending`. `team update` writes the other values during accept/reject/defer.
- One file per agent per verb invocation. If the conductor stashes feedback for the same agent twice in one verb, append to the same file with a `---` separator between entries.

---

## Stakes rubric (v4.1+)

The `stakes` field determines whether `team update` auto-promotes an entry (low stakes, when `features.auto_promote_low_stakes` is enabled) or queues it for owner review (high stakes, always reviewed).

**`stakes: low` — auto-promotable when the flag is on.** The entry describes *how* an agent works at a craft / convention / tooling level. Examples:

- *"Use absolute paths in shell commands."*
- *"Prefer `npm ci` over `npm install` in CI."*
- *"Format git commit messages with a body explaining why."*
- *"When the team has multiple agents review, render attribution per turn even at `team_chat: off`."*
- *"Quote source URLs with `<SourceLink>` not raw `<a>`."*

Pattern: doesn't change *what* the agent decides, prioritizes, or recommends — only *how* they execute.

**`stakes: high` — always queues for owner review.** The entry describes *what* an agent decides, prioritizes, or holds as a principle. Examples:

- *"When the user names a specific anchor, verify every addition belongs to that anchor."* (framing)
- *"Don't conflate regulated-practice violation with standard informational disclaimer hygiene."* (judgment)
- *"For products whose core data is small + public, default to client-side engine + JSON snapshot."* (architectural default)
- *"Distinguish between owner-as-co-author and owner-as-reviewer roles."* (interaction model)
- *"Land cheap infrastructure during scaffold, not as follow-up."* (cross-cutting principle)

Pattern: shapes future client work; the owner needs to see it before it lands.

**When in doubt: `high`.** Auto-promote is the optimization; queue-for-review is the correct default. False positives (low classified as high) cost an unnecessary review; false negatives (high classified as low) silently shape future client work in ways the owner didn't see. The asymmetry is real.

**Who sets `stakes`:** the conductor at capture time. Either explicitly (via the Stash prompt's optional `[low]` / `[high]` annotation) or by default (`high`). The auto-debrief mechanism in T2.3 pre-classifies its own emissions as `low` because agents are commenting on their own craft — but the conductor can override on review.

---

## `history.md` append format

One line per agent per verb completion. Append to the existing `history.md` directly. No frontmatter. No prose. No editorializing.

```
- 2026-05-17 · hacky-hours-docs · audit · Reviewed framework's persistence story; flagged Slice 12 capture-step gap.
```

Field order (separator: ` · `):
1. **Date** — `YYYY-MM-DD`, local
2. **Project slug** — `basename` of cwd
3. **Verb** — the verb that called the role (`audit`, `adopt`, `arbitrate decide`, `step 2`, etc.)
4. **Contribution summary** — one sentence, what the agent actually did in this verb. Past-tense, concrete. Not "Reviewed code" — "Flagged P0 on input validation in auth.py:42" or "Co-authored DATA_MODEL.md with Sam." Specific.

**Append rules:**
- Insert under any existing `## Recent` heading if present; otherwise append to end-of-file under a new `## Recent` heading (created once).
- Newest entries at the top of the section.
- One newline between entries (the markdown list does the rest).

**Compaction:** when `history.md` exceeds ~500 lines or ~10k tokens (the limit specified in the template boilerplate), the framework summarizes older entries into a "Key facts and patterns" section at the top and archives raw entries to `history-archive/<YYYY-MM-DD>.md` in the team repo. v4.0.0 ships the append — compaction is a daemon-style task deferred to v4.1+. Until then, agents with long histories just have long files. Git history preserves the raw record either way.

---

## When capture fires

At the **end** of every multi-role verb, after the verb's primary work completes and before its final summary prints. Multi-role verbs are:

- `step 1` (ideate) — when more than the Product role is involved
- `step 2` (design) — always (multi-role by definition)
- `step 3` (roadmap) — when Product + Architect collaborate
- `step 4` (build) — when role review touches the implementation
- `step 5` (iterate) — when multiple roles synthesize feedback
- `reviews/audit` — always (three lanes, multi-role)
- `tools/adopt` — always (full team fan-out)
- `tools/arbitrate` — always (definitionally multi-role)

Single-role verbs (`feedback`, `issue`, `meta`, `team` subcommands, `team site`, `export`, `tools/mode`, `tools/walkthrough`, `update 1`, `update 2`) **do not** capture. They're either operational (no agent participated) or single-discipline.

The verb's tail emits one block, always in this shape:

```markdown
---

## Phase N — Stash (team learning)

Roles that participated in this verb: <list of agent-ids from the fan-out>.

**History (auto):** Appended one line to each participant's `history.md`. Summary used:
  - architect: <summary used>
  - security: <summary used>
  - ...

**Behavior feedback (optional, you decide):**

> *"Anything you said during this run that should change how an agent works in **future** sessions? Free-form — name the agent, then what should be different. Or `none` to skip."*

Wait for conductor input. For each agent named, write `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md` per the schema above.

**Footer (always print):**

> *Stashed <N> behavior note(s) for <agents>. Appended history to <count> agent(s) (commit <sha>).*
> *Promote behavior notes anytime with `/hacky-hours team update`.*
```

The phase number ("Phase N") is wherever this lands in the verb's existing phase list — Step 5's phases run 1–5, so this becomes "Phase 6 — Stash." Audit ends at Step 4, so it becomes "Step 5 — Stash." Pick the next integer in the verb's existing sequence.

---

## Implementation responsibilities (per verb)

A verb that fans out to roles must:

1. **Track participants** — keep a list of agent-ids that actually contributed during the run. Don't include roles that produced no output. The list goes into the Stash block.
2. **Compose history summaries before the Stash prompt** — one sentence per participating agent, based on what that agent actually did. Not "Maya helped with audit" — concrete: "Confirmed PRODUCT_OVERVIEW.md still reflects the project's audience after the v4 pivot."
3. **Resolve session ID** per the algorithm above before any pending file is written.
4. **Append history first**, then prompt for behavior feedback, then write any pending files. This order matters — if the conductor cancels at the feedback prompt, the history is still recorded (which is correct — the verb did happen).
5. **Refresh derived metrics** in each participating agent's `profile.md` frontmatter immediately after history append (and before the commit in step 6). Parse the agent's `history.md` (plus `history-archive/*.md` if compaction has run) to recompute the full `metrics:` block per the schema above. Stamp `metrics_refreshed: <ISO timestamp>` and `last_active: <date>`. Bump `level` per the derivation table. This keeps team-site rendering, resume composition, and `team show <agent>` output in sync without a separate refresh verb. Sub-second per agent.
6. **Commit history + metrics in a single commit** at end of verb:
   ```bash
   cd ~/.hacky-hours/teams/<active>/
   git add agents/*/history.md agents/*/profile.md
   git commit -m "history: <verb> @ <project> @ <date> — <N> agent(s)"
   ```
   No push. Team repo remains local-only by default. Bundling history + metrics in one commit keeps the team-repo log readable.
7. **Honor `team_chat` mode** for the Stash phase rendering. In `off`, the narrator runs the prompt. In `minimal`, the prompt is attributed to the conductor's voice (no role headers — this is a framework moment, not a role moment). In `full`, optionally let one role (often Maya as Product, since she tracks team rhythm) introduce the stash block. Either way, the conductor's reply is captured verbatim.

---

## Edge cases

- **Verb fanned out but produced no per-role output.** (E.g., audit ran but the doc-stranger lane errored.) Don't append history for roles that didn't actually contribute. History is a record of what happened, not what was attempted.
- **Conductor responds `none` to the behavior-feedback prompt.** No pending files written. Footer still prints with "Stashed 0 behavior note(s)" and the history append summary.
- **Conductor names an agent that wasn't in this verb's fan-out.** Allowed — capture the behavior feedback anyway. The conductor might be reflecting on past interactions. Mark the pending file with `verb: <this-verb>` (the verb that prompted the stash) and let `team update` handle it.
- **Team repo has uncommitted changes when history appends.** Surface to the conductor: *"Team repo has uncommitted changes — appending history would mix them into one commit. Stash your team changes first or proceed and they'll be bundled?"* Default: ask.
- **`~/.hacky-hours/teams/<active>/` doesn't exist** (team-binding error). Skip capture for this verb. Print: *"Could not capture history — active team `<name>` not found at `~/.hacky-hours/teams/<name>/`. Run `/hacky-hours team init` or `team switch <existing>`."*

---

## Derived metrics (profile.md frontmatter)

Slice 13 introduces a `metrics:` block in every agent's `profile.md` frontmatter. The block is auto-managed: refreshed at end of every multi-role verb (Stash phase), at end of `team backfill`, and at end of `team reflect`. **Conductors do not edit this block by hand** — anything they write gets overwritten on next refresh. Use it for read-only display (team site, resume header, `team show` output).

Schema:

```yaml
metrics:
  level: 0                  # 0-5, derived (see "Level derivation" below)
  history_entries: 0        # raw line count from history.md (excluding archived/compacted)
  projects: []              # distinct project slugs the agent has appeared in
  verbs_run: 0              # total verb participations
  by_verb:                  # counts per verb-type the agent has participated in
    audit: 0
    adopt: 0
    arbitrate: 0
    design: 0
    build: 0
    ideate: 0
    roadmap: 0
    iterate: 0
  feedback_count: 0         # durable behavior corrections promoted via team update
  last_active: null         # YYYY-MM-DD of most recent history entry
  metrics_refreshed: null   # ISO timestamp of last refresh
  reflected_at: null        # YYYY-MM-DD of last team reflect invocation
```

Refresh implementation: parse `history.md` and `history-archive/*.md` (if compaction has run); count by verb prefix; collect distinct project slugs; stamp timestamps. Sub-second operation per agent; no performance concern at typical scales.

## Level derivation

Computed from `history_entries` with optional bumps for breadth:

| `history_entries` | Base level |
|-------------------|------------|
| 0 | 0 (newcomer — no history yet) |
| 1–5 | 1 (junior — first few contributions) |
| 6–15 | 2 (intermediate) |
| 16–30 | 3 (senior) |
| 31–60 | 4 (staff) |
| 61+ | 5 (principal) |

**Breadth bumps (cumulative, cap at 5):**

- `+1` if agent has worked on 3+ distinct projects
- `+1` if agent has participated in 5+ distinct verb types (e.g., audit + adopt + design + arbitrate + iterate)

Level is honest signal, not gamification. An agent with 100 entries all from one `audit` verb on one project is still level 4 (high count, no breadth). An agent with 20 entries across 4 projects and 6 verb types could hit level 5 from the breadth bumps.

## Resume composition (Slice 13)

`/hacky-hours team resume <agent-id>` reads `profile.md` + `system-prompt.md` + `history.md` + `feedback.md` and writes `agents/<id>/resume.md`. Full spec: `tools/team-resume.md`. The resume is **derived only** — fact-based, sourced from the team repo, regenerated freely. Every line traces to a source; no invented skill claims, no embellished narrative. Three style presets (`minimal`, `standard`, `deep`) calibrate verbosity. Honest about thin work: an agent with 0 history entries gets a minimal resume (header + Profile bio) — no Skills/Experience padding.

## Reflection semantics (Slice 13)

`/hacky-hours team reflect <agent-id>` is the agent's self-look. Two slots get updated:

1. **Track record section** (silent, fact-of-record) — auto-appended/replaced in `profile.md` Bio. One paragraph per project, third-person past-tense, cites by count where useful. Same review semantics as forward-capture's `history.md` append: no conductor review (it's a fact summary). Conductor can hand-edit `profile.md` if anything's off.

2. **Prose updates** (conductor-reviewed) — agent proposes refined Background / How I work / What I produce sections based on accumulated history + feedback. Each section that warrants revision writes a `kind: prose_update` pending entry to `~/.hacky-hours/sessions/<id>/pending/<agent-id>.md`. The pending file gains two frontmatter fields:
   - `kind: prose_update`
   - `target_section: background | how_i_work | what_i_produce`

   `/hacky-hours team update` reads these the same way it reads `kind: behavior_feedback` entries, presents accept/edit/reject/defer per section, and on accept replaces the relevant section in `profile.md`.

3. **Self-observations** (printed, opt-in to land as behavior feedback) — agent surfaces patterns it sees in its own work (strengths it wants to lean into, gaps it wants to close). Doesn't auto-write; conductor names which items to stash as behavior feedback. Those land as standard `kind: behavior_feedback` pending entries.

**Cadence:** reflection is opt-in, conductor-invoked. Not part of Stash phase (which fires automatically end-of-verb). Reflection is *"go look at yourself"* — a deliberate moment after a meaningful body of work has accumulated, not a per-verb tax.

Full spec: `tools/team-reflect.md`.

## Backfill semantics

Forward-capture (Stash phase) handles work done *after* Slice 12 lands. Long-running projects that adopted v4 mid-stride need *retroactive* population so agents' track records reflect the project's lifetime, not just post-Slice-12 activity. `/hacky-hours team backfill` is the one-shot retroactive companion. Full spec: `${CLAUDE_SKILL_DIR}/tools/team-backfill.md`.

Differences from forward-capture:

| Dimension | Forward-capture (Stash) | Backfill |
|-----------|--------------------------|----------|
| Trigger | End of every multi-role verb (automatic) | Conductor invokes explicitly (one-shot) |
| Source of activity | What the current verb run actually did | Project's CHANGELOG.md or git log |
| Agent classification | Direct — the verb knows who participated | Heuristic — file paths + keywords → role |
| History line annotation | `<date> · <project> · <verb> · <summary>` | `<date> · <project> · <verb> (backfilled, <anchor>) · <summary>` |
| Review semantics for history | Silent auto-append | Per-agent batch review (conductor accepts/selects/rejects in bulk per agent) |
| Behavior feedback prompt | Always shown | Not part of backfill — backfill is about history only |
| Commit pattern | One commit per verb at end-of-verb | One commit per agent batch |
| Pending file | Yes — `pending/<agent-id>.md` for behavior notes only; history commits direct | None — `backfill-pending/<agent-id>.md` only when `defer` is chosen on a batch |

**The `(backfilled, <anchor>)` annotation is load-bearing.** It distinguishes retroactively populated entries from forward-captured ones. `<anchor>` is either a CHANGELOG section anchor (`CHANGELOG#v3-0-0`) or a short git SHA (`c66cc62`), giving the entry verifiable provenance. Future audits or `team show <agent>` outputs can filter by annotation if they need to know what the agent actually "did" in real-time vs. what was retrofit.

**Review semantics differ because the situation differs.** Forward-capture writes one history line per verb run — the conductor is right there, just watched it happen, the line is fact. Silent append is appropriate. Backfill bulk-proposes potentially dozens of entries per agent from a source the conductor hasn't been watching turn-by-turn. Per-agent batch review (with `select` for entry-level granularity when needed) gives the conductor a chance to drop entries the classifier got wrong or summaries that overreach what the source actually says.

**Backfill is opt-in only.** It does not run automatically from `adopt` or any other verb. The conductor decides when (and whether) to retrofit history.

---

## What this verb closes

Pre-Slice-12 state: every agent had `feedback.md` and `history.md` slots that nothing wrote to. `team update` existed as a reader but had nothing to read. The team site rendered bios from `profile.md` that never changed because no verb updated the source. The v4 thesis — *"orchestra that learns and grows with context"* — was structural-only.

Post-Slice-12: every multi-role verb writes one history line per participating agent (silent) and offers a stash prompt for behavior feedback (opt-in but always shown). `team update` has real work to do. Agents accumulate project tracks visible on the team site and durable behavior corrections visible in their feedback files. `team backfill` retroactively populates `history.md` for projects that did real work before Slice-12-aware capture existed — so the team site reflects project lifetime, not just post-Slice-12 activity. The orchestra learns, and remembers what it did before it could remember.

Same shape as Slice 11: a structural promise that needed a concrete render contract to actually fire.
