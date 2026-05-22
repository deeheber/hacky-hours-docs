# /hacky-hours team update — promote session changes into the team repo

Captures behavior feedback and prompt edits made during the current session, then promotes accepted changes into the team repo as durable updates with a git commit.

This is **how agents learn**. Without it, agents are frozen at their starter prompts. With it, the team gets better the more you work together.

## What gets captured during a session

Pending changes for agents accumulate at `~/.hacky-hours/sessions/<session-id>/pending/<agent-id>.md`. The capture contract — what shape the file takes, how the session ID is resolved, when capture fires — is canonical in **`${CLAUDE_SKILL_DIR}/references/capture-format.md`**. Read it before promoting if you need to understand schema.

Two ways an entry lands:

- **End-of-verb Stash prompt (the primary path).** Every multi-role verb (`step 1–5`, `audit`, `adopt`, `arbitrate`) ends with a stash phase that asks the conductor: *"Anything you said during this run that should change how an agent works in future sessions?"* Free-form by agent, or `none` to skip. Whatever the conductor names lands as one pending file per agent named.
- **Direct prompt edit.** If the conductor runs `/hacky-hours team show <agent-id> --edit` and modifies the system prompt mid-session, the diff is staged as a `prompt_edit` kind pending entry for the next `team update` cycle. (`--edit` flag and this hook are scaffold for v4.1+; v4.0.0 honors the schema but the entrypoint is the Stash prompt above.)

Each pending change is one file per agent per verb invocation. If the conductor stashes feedback for the same agent twice in one verb (rare), entries append to the same file separated by `---`.

History append is the *other* slot Stash writes to (silent, no review needed) — see `references/capture-format.md` for the distinction. `team update` is only the promoter for behavior-feedback pending entries; history.md commits land directly at end-of-verb without going through this review loop.

## Step 0 — Pre-flight

1. Check `~/.hacky-hours/sessions/` for any session folders with pending entries.
2. If no pending entries: print *"Nothing to promote. Agents are unchanged from the team repo."* and exit.

## Step 1 — Collect pending changes (v4.1: stakes-bucketing)

Read every `~/.hacky-hours/sessions/<id>/pending/<agent-id>.md` from active sessions.

**Bucket by `stakes:` field** (v4.1+; see `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Stakes rubric"):

- **Auto-bucket:** `stakes: low` AND `features.auto_promote_low_stakes: true` in `~/.hacky-hours/settings.yml`.
- **Review-bucket:** everything else — `stakes: high`, `stakes` absent (defaults to high), or auto-promote flag disabled.

For each agent with **review-bucket** pending changes, structure them as:

```
Agent: <name> (<role>)
Pending changes (review queue):
  1. [behavior feedback · high] <one-line summary> — from session <id>, <date>
  2. [prompt edit · high]       <one-line summary> — from session <id>, <date>
  ...
```

Auto-bucket entries are NOT walked through individually — they land silently in Step 4's commit with a footer summary.

If both buckets are empty: print *"Nothing to promote. Agents are unchanged from the team repo."* and exit.

If only the auto-bucket has entries (no review needed): skip Step 2's "ready?" confirmation; jump straight to Step 4's silent commit with the auto-promote footer.

## Step 2 — Present to conductor (v4.1: review-bucket only)

Print a summary:

> *"<N> agents have pending changes from <M> sessions.*
>
> *Review queue (`stakes: high`):*
> *  <agent 1>: <count> change(s)*
> *  <agent 2>: <count> change(s)*
> *  ...*
>
> *Auto-promote queue (`stakes: low`, will commit silently): <count> change(s) across <N> agents*
>
> *I'll walk you through the review queue. For each change you can: **accept** (lands in team repo), **edit** (revise then accept), **reject** (drops the change), **defer** (keeps pending for next time), or — for accepted changes — **propagate** (offer the principle to peer agents).*
>
> *Ready?"*

Wait for confirmation.

When `features.auto_promote_low_stakes: false` or absent, the auto-promote queue is folded into the review queue (everything is reviewed). The summary still distinguishes the buckets for owner visibility but the walk-through covers all.

## Step 3 — Per-change review

For each pending change (review-bucket only), present:

```
=== <agent-name> — change <N>/<total> ===
Kind:    <behavior | prompt-edit>
Stakes:  <low | high>          (v4.1+; defaults to high when absent)
Captured: <date>, session <id>
Propagated from: <agent-id>    (v4.1+; only if this was a cross-role propagation)
Context: <brief — what was happening when this was captured>

Current state in team repo:
  <relevant lines from agent's system-prompt.md or feedback.md>

Proposed change:
  <the pending content>

Resulting state (if accepted):
  <unified diff or after-snippet>

What to do?
  a) accept       (apply this change)
  e) edit         (revise before accepting)
  r) reject       (drop this change, no record kept)
  d) defer        (keep pending; review again next time)
```

Wait for conductor input. Process accordingly:

- **accept:** apply to the agent's files in `~/.hacky-hours/teams/<active>/agents/<agent-id>/`. Behavior feedback → appended to `feedback.md`. Prompt edits → applied to `system-prompt.md`. Always preserve the existing structure. **After accept, if `stakes: high` AND `features.cross_role_propagation: true`, run the propagation peer-ask (see below).**
- **edit:** prompt for the revision, then re-present and re-ask
- **reject:** mark the pending file with `outcome: rejected, reason: <optional>` and move it to `~/.hacky-hours/sessions/<id>/resolved/<agent-id>.md`
- **defer:** leave the pending file in place; it stays around for the next `/hacky-hours team update`

### Cross-role propagation peer-ask (v4.1+)

Fires after `accept` when:
- The accepted entry has `stakes: high` (framing-level principles propagate; craft-level patterns don't), AND
- `features.cross_role_propagation: true` in settings.yml.

Ask the conductor:

> *"This principle is framing-level. Should any peer agents also adopt it? Free-form list of agent IDs (e.g., `product, design`), or `none`."*

For each peer named, write a new pending file at `~/.hacky-hours/sessions/<id>/pending/<peer-id>.md` with:

```yaml
---
captured_at: <now ISO 8601>
session_id: <current session>
project: <current project>
verb: team-update
kind: behavior_feedback
agent: <peer-id>
stakes: high
propagated_from: <original-agent-id>
status: pending
---

## Context

Propagated from <original-agent-id> during team update on <date>. Original principle (lightly rewritten to apply to <peer-id>'s role):

<the accepted change content, lightly rephrased for the peer's discipline>

## Proposed change

<the proposed change content; the conductor can edit during the next review cycle>
```

These peer pending files surface in the **next** `team update` cycle for normal review. Not auto-applied — the framework proposes; the conductor decides.

If `features.cross_role_propagation: false` or absent: skip the peer-ask entirely; `accept` is just `accept`.

## Step 4 — Apply auto-bucket + commit to team repo

**Auto-bucket apply (v4.1+, silent):** for each entry in the auto-bucket, apply directly to the agent's `feedback.md` or `system-prompt.md` without per-entry review. Move the pending file to `resolved/`.

After auto-bucket apply AND review-bucket walk-through, group all accepted changes (both buckets) into a single commit on the team repo:

```bash
cd ~/.hacky-hours/teams/<active>/
git add agents/
git commit -m "<descriptive message>"
```

Commit message template (v4.1+ stakes-aware):

```
Update <N> agent(s) — <date>

Auto-promoted (stakes: low):
- <agent-name>: <one-line summary>
- ...

Reviewed + accepted (stakes: high):
- <agent-name>: <one-line summary>
- ...

Cross-role propagated:
- <peer-agent>: principle from <original-agent>'s accepted entry queued for next review

Updated by /hacky-hours team update.
Source sessions: <session ids>
```

Omit any section that's empty. When `features.auto_promote_low_stakes` is off, all accepts fold under "Reviewed + accepted" regardless of `stakes` field.

If the team has a git remote configured (`git remote -v` shows one), ask:

> *"Push to <remote> now? (yes / no — you can push later with `cd ~/.hacky-hours/teams/<active>/ && git push`)"*

Never auto-push without explicit yes.

## Step 5 — Clean up

Move all accepted pending files to `~/.hacky-hours/sessions/<id>/resolved/`. Deferred files stay in place. Rejected files moved to resolved with their rejection annotation.

If a session's pending folder becomes empty, leave the resolved folder for audit but the session is "settled."

## Step 6 — Print confirmation (v4.1+: stakes-aware footer)

> *"Done.*
> *  Auto-promoted: <N> (stakes: low)*
> *  Reviewed + accepted: <N> (stakes: high)*
> *  Cross-role propagated: <N> (queued for next team update)*
> *  Deferred: <N>*
> *  Rejected: <N>*
> *  Commit: <sha>*
>
> *Your team is now smarter. Next time you run a verb, the affected agents will use these updated prompts and feedback notes."*

Omit any line with count 0. When `features.auto_promote_low_stakes` is off, the auto-promoted line is hidden (everything was reviewed); when `features.cross_role_propagation` is off, the propagated line is hidden.

## Multi-session race conditions

If two Claude Code sessions are running simultaneously and both have pending changes for the same agent:

- The first to call `/hacky-hours team update` and accept wins.
- The second session's pending change will be reviewed against the now-updated agent state. The conductor will see what was already changed and can decide whether the second change still applies.
- v4.0.0 surfaces this honestly: *"This change is against an earlier version of <agent>'s prompt — the prompt has changed since this was captured. Here's the current state and the proposed change. Still applies?"*

## Discard / Restart

If you want to throw away all pending changes:

```
/hacky-hours team update --discard-all
```

Asks for confirmation, then moves all pending → resolved with `outcome: discarded`. No git commit.

## Notes for the assistant

- **Never silently overwrite system prompts.** Always show the diff and require explicit accept.
- **Preserve git history.** Each `team update` is one git commit, with a clear message tying it to source sessions.
- **The team repo is the source of truth.** Pending changes are drafts; the team repo is canonical. After promote, the pending entry is resolved — no way to accidentally re-promote.
- **Help users build the habit.** When a session ends with un-promoted pending changes, suggest: *"You've got pending changes for <agents>. Run `/hacky-hours team update` whenever you're ready."*

## What this verb completes

Without team update, the persistent-team claim is structural-only — the files exist but never change. With team update, the team genuinely accumulates knowledge across sessions and projects. The dogfood loop closes at the team level (per-agent improvement) in addition to the framework level (`/hacky-hours meta`).
