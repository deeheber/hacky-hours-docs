# /hacky-hours feedback — capture session friction (local-only)

Captures friction during real sessions and writes structured notes to `~/.hacky-hours/feedback/`. The local feedback corpus is the input to `/hacky-hours meta`, which clusters patterns into framework improvement patches.

All local-only by default. No telemetry. Opt-in upstream submission via `/hacky-hours issue`.

## Three kinds of friction

Every feedback note is one of these kinds. Be explicit — the kind matters for `/hacky-hours meta` clustering.

- **`tool`** — a verb felt clunky, slow, confusing, or wrong-shaped (e.g., "adopt asks 4 questions but I only had answers to 2", "audit's scorecard math felt off at Tier 1")
- **`seam`** — a handoff between two roles or two verbs was lossy (e.g., "design→implement lost the journey context", "audit findings didn't make it into the next BACKLOG.md")
- **`role`** — an agent's output was wrong, over-cautious, under-cautious, jargon-y, off-voice, missed something obvious (e.g., "Alex over-flagged at Tier 1", "Maya kept asking the 5Ws after I'd already answered")

## Step 0 — Pre-flight

If `~/.hacky-hours/feedback/` doesn't exist: create it (mkdir -p). It's an empty folder until friction accumulates.

## Step 1 — Parse arguments or prompt

Argument shape: `/hacky-hours feedback [<kind>] [<message>]`

- **Full form:** `/hacky-hours feedback tool "audit's three-lane fan-out asked for confirmation twice"` → capture directly
- **No args:** prompt the user:

  > *"What kind of friction? (tool / seam / role)"*
  > *"What happened? (one or two sentences — what felt wrong, what you'd expect instead)"*

  Then optionally: *"Which tool/role/seam specifically?"*

## Step 2 — Compose the feedback note

Write to `~/.hacky-hours/feedback/<YYYY-MM-DD>-<kind>-<short-slug>.md`:

```markdown
---
captured: <ISO datetime>
kind: <tool | seam | role>
target: <verb name | role id | "from→to" for seams>
session_id: <session id if available, else "unknown">
project: <cwd if in a repo, else "global">
framework_version: <read from ~/.hacky-hours/version>
team: <active team name if applicable>
---

# Feedback: <one-line summary>

## What happened
<user's description>

## What I expected
<inferred or asked: what would have been better?>

## Context
- Verb being run: <if applicable>
- Role(s) involved: <if applicable>
- Tier of the project: <if known>

## Tags
<comma-separated tags for clustering — auto-generated from text if possible>
```

## Step 3 — Confirm and exit

Print:

> *"Captured to `~/.hacky-hours/feedback/<file>`.*
> *Local-only — won't leave your machine unless you explicitly submit via `/hacky-hours issue`.*
> *Run `/hacky-hours meta` periodically to cluster accumulated feedback into framework patches."*

Don't elaborate. Friction capture should be fast — anything more than two lines of acknowledgment is itself friction.

## Implicit feedback capture

Beyond explicit `/hacky-hours feedback` calls, the framework should also capture implicit signals during sessions:

- When the conductor overrides an agent's recommendation, log it as a role-friction note (the override might mean the agent was wrong)
- When a verb is abandoned mid-flow, log it as a tool-friction note
- When the conductor expresses frustration in chat ("ugh", "this isn't working", "wait that's not right"), surface a "want to capture this as feedback?" prompt

These implicit captures are surfaced to the conductor for confirmation before writing — never silently logged. v4.0.0 implements explicit `/hacky-hours feedback` only; implicit capture is a follow-on enhancement.

## Privacy

The feedback corpus accumulates patterns about your projects. Treat it as sensitive:
- Never auto-upload anywhere
- `/hacky-hours issue` is the only path to send anything upstream, and it always asks per-submission
- The `~/.hacky-hours/feedback/` folder is already inside the user-private global setup
- If you want to share with teammates (e.g., a shared team improvement log), you can manually copy specific files to a shared location — but the framework never does it for you

## Notes for the assistant

- Don't editorialize. The user's words are the data; your job is to structure them, not improve them.
- Don't ask "do you want to also submit this as a GitHub issue?" automatically — that's `/hacky-hours issue`, run separately.
- If multiple feedback items come in rapid succession with overlapping subjects, suggest consolidating after the third one: *"Looks like you're catching multiple things about audit — want to combine these into one larger feedback note?"*
