# /hacky-hours team update — promote session changes into the team repo

Captures behavior feedback and prompt edits made during the current session, then promotes accepted changes into the team repo as durable updates with a git commit.

This is **how agents learn**. Without it, agents are frozen at their starter prompts. With it, the team gets better the more you work together.

## What gets captured during a session

The framework collects pending changes to agents in `~/.hacky-hours/sessions/<session-id>/pending/`. Captured automatically when:

- **You give behavior feedback to an agent.** E.g., during a session you say "Alex, be terser when flagging at Tier 1." That's a behavior note staged for Alex.
- **You directly edit an agent's prompt.** E.g., you run `/hacky-hours team show alex --edit` and modify their system prompt or profile.
- **You override an agent's recommendation more than once in similar shape.** Implicit signal that the agent's defaults need adjustment.

Each pending change is one file in the session's pending folder: `<agent-id>.md` containing the proposed change.

## Step 0 — Pre-flight

1. Check `~/.hacky-hours/sessions/` for any session folders with pending entries.
2. If no pending entries: print *"Nothing to promote. Agents are unchanged from the team repo."* and exit.

## Step 1 — Collect pending changes

Read every `~/.hacky-hours/sessions/<id>/pending/<agent-id>.md` from active sessions. Group by agent.

For each agent with pending changes, structure them as:

```
Agent: <name> (<role>)
Pending changes:
  1. [behavior feedback] <one-line summary> — from session <id>, <date>
  2. [prompt edit]       <one-line summary> — from session <id>, <date>
  ...
```

## Step 2 — Present to conductor

Print a summary:

> *"<N> agents have pending changes from <M> sessions:*
>
> *  <agent 1>: <count> change(s)*
> *  <agent 2>: <count> change(s)*
> *  ...*
>
> *I'll walk through each. For every change you can: **accept** (lands in team repo), **edit** (revise then accept), **reject** (drops the change), or **defer** (keeps pending for next time).*
>
> *Ready?"*

Wait for confirmation.

## Step 3 — Per-change review

For each pending change, present:

```
=== <agent-name> — change <N>/<total> ===
Kind: <behavior | prompt-edit>
Captured: <date>, session <id>
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

- **accept:** apply to the agent's files in `~/.hacky-hours/teams/<active>/agents/<agent-id>/`. Behavior feedback → appended to `feedback.md`. Prompt edits → applied to `system-prompt.md`. Always preserve the existing structure.
- **edit:** prompt for the revision, then re-present and re-ask
- **reject:** mark the pending file with `outcome: rejected, reason: <optional>` and move it to `~/.hacky-hours/sessions/<id>/resolved/<agent-id>.md`
- **defer:** leave the pending file in place; it stays around for the next `/hacky-hours team update`

## Step 4 — Commit to team repo

After all changes are resolved, group accepted changes into a single commit on the team repo:

```bash
cd ~/.hacky-hours/teams/<active>/
git add agents/
git commit -m "<descriptive message>"
```

Commit message template:

```
Update <N> agent(s) — <date>

<For each modified agent:>
- <agent-name>: <one-line summary of accepted changes>

Updated by /hacky-hours team update.
Source sessions: <session ids>
```

If the team has a git remote configured (`git remote -v` shows one), ask:

> *"Push to <remote> now? (yes / no — you can push later with `cd ~/.hacky-hours/teams/<active>/ && git push`)"*

Never auto-push without explicit yes.

## Step 5 — Clean up

Move all accepted pending files to `~/.hacky-hours/sessions/<id>/resolved/`. Deferred files stay in place. Rejected files moved to resolved with their rejection annotation.

If a session's pending folder becomes empty, leave the resolved folder for audit but the session is "settled."

## Step 6 — Print confirmation

> *"Done. <accepted> change(s) committed to team repo (<commit-sha>).*
> *<deferred> deferred for next time.*
> *<rejected> rejected.*
>
> *Your team is now smarter. Next time you run a verb, the affected agents will use these updated prompts and feedback notes."*

## Multi-session race conditions

If two Claude Code sessions are running simultaneously and both have pending changes for the same agent:

- The first to call `/hacky-hours team update` and accept wins.
- The second session's pending change will be reviewed against the now-updated agent state. The conductor will see what was already changed and can decide whether the second change still applies.
- v4.0.0-dev surfaces this honestly: *"This change is against an earlier version of <agent>'s prompt — the prompt has changed since this was captured. Here's the current state and the proposed change. Still applies?"*

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
