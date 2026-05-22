# v4 First-Run — global user-level setup

This file is invoked from SKILL.md when `~/.hacky-hours/` does not exist. Its job is to create the global, user-level skeleton that v4 requires before any project-level work can happen.

This runs **once per user**, not once per project. After completion, control returns to whatever the user was trying to do (`/hacky-hours team`, `/hacky-hours adopt`, etc.) — or to the no-arg guided session.

---

## Step 1 — Greet and explain

Print:

> *"Welcome to Hacky Hours v4.0.1 🛠️🤗 — first time using v4 on this machine.*
>
> *Before we do anything project-specific, I'll create a small global setup under `~/.hacky-hours/`. That's where your **persistent team** of AI agents lives, along with your personal settings. It's yours — private by default, never shared, separate from any project repo.*
>
> *This takes 30 seconds. Ready?"*

Wait for confirmation. If declined, stop and exit cleanly.

## Step 2 — Detect and confirm

Run `ls ~/.hacky-hours/ 2>/dev/null` to double-check it doesn't exist. If it does (race condition or partial install), skip ahead to **Step 5 — Audience profile** and treat as a resume.

## Step 3 — Create the skeleton

Create the following directory structure under `$HOME/.hacky-hours/`:

```
~/.hacky-hours/
├── version                 ← installed framework version (file contents: "4.0.1")
├── settings.yml            ← user preferences (see template below)
├── feedback/               ← local feedback corpus (empty for now)
├── sessions/               ← transient session state (empty)
├── teams/                  ← team repos go here (empty; default team created next)
└── versions/               ← prior framework version snapshots for rollback (empty)
```

Use `mkdir -p` for safety. Write `version` with the literal text `4.0.1` (no trailing newline beyond one).

## Step 4 — Write settings.yml

Write `~/.hacky-hours/settings.yml` with this template:

```yaml
# Hacky Hours user-level settings
# Edit anytime. See V4_DESIGN.md §6 for full schema.

# Budgets (token counts for session-scope cost tracking)
session_budget_warn: 50000
session_budget_hard: 200000

# Default model used by agents (per-role overrides below)
default_model: claude-opus-4-7

# Per-role model overrides (cheap roles can use smaller models to save tokens)
role_models:
  licensing: claude-haiku-4-5
  # security: claude-opus-4-7
  # design: claude-sonnet-4-6

# Voice baseline — overridden per project via VOICE.md
voice_default: builder    # builder (plain language) | engineer (technical)

# Team chat — how visible the orchestra is during multi-role verbs
# See references/chat-format.md and V4_DESIGN.md §4.20
team_chat: minimal        # off | minimal | full
# off     — single narrator, no team voices (cheapest)
# minimal — speaker attribution at meaningful moments only (default)
# full    — closed-captioned multi-agent dialogue (substantially more tokens)

# Audience modeling — informs how every role adapts its communication to you
profile:
  technical_background: unspecified    # non_engineer | engineer | mixed | unspecified
  plan: unspecified                    # pro | max5x | max20x | unspecified — affects defaults below
  role_fluency:
    # Set your fluency per discipline so each role calibrates appropriately.
    # Levels: novice | intermediate | expert
    # Anything not listed defaults to "intermediate".
    # Examples — edit to reflect you:
    # product: expert
    # security: novice
    # frontend: intermediate

# Feature flags — v4.1+; gated mechanisms ship disabled-by-default
# See references/feature-flag-loader.md for the pattern + flag list
# See ADR 2026-05-22-feature-flag-layer.md for the design
features:
  # Workflow (v4.1 Tier 1)
  discovery_phase: false              # Discovery phase in Step 1 + lo-fi homepage gate
  skeptic_mode: false                 # --skeptic flag on any role
  status_updates: false               # agent-initiated escalation + status messages
  presentations: false                # presentation artifact alongside deep docs

  # Team learning (v4.1 Tier 1 + Tier 2)
  cross_role_propagation: false       # team-update Step 3 propagate-to-peer
  auto_promote_low_stakes: false      # team-update auto-bucket by `stakes` field
  auto_debrief: false                 # end-of-verb agent-to-agent self-debrief

  # Workroom (v4.1 Tier 2)
  workroom_mode: false                # multi-turn agent dialogue → messages.jsonl

  # Browser companion write-back (v4.1 Tier 3)
  forms_writeback: false              # browser fillable-forms → pending-input.json
  backlog_writeback: false            # browser kanban drag-to-reorder
  session_monitor: false              # browser session-monitor surface

# Workroom bounds (v4.1+; see ADR 2026-05-22-workroom-mechanic.md)
workroom_max_turns: 24
workroom_role_budget: 2000

# Privacy
share_feedback_with_empathetech: false   # opt-in only; /hacky-hours issue still works individually
auto_update_check: false                  # never auto-update; explicit /hacky-hours update only
```

## Step 5 — Audience profile (brief)

Ask the user two short questions to seed the audience model.

**Question 1 — Background:**

> *"One quick question that helps every role talk to you the right way: are you primarily a software engineer, primarily a non-engineer (builder, founder, SME), or somewhere in the middle?"*

Update `profile.technical_background` in settings.yml accordingly. If they say "non-engineer," set `voice_default: builder` (already the default). If "engineer," set `voice_default: engineer`. If "mixed," keep `builder` but note in the profile.

**Question 2 — Claude plan tier (v4.1+):**

> *"And which Claude plan are you on? This shapes how aggressively the framework fans out across roles.*
>  *  - **Pro** — leaner defaults, cost preflight on heavy verbs, smaller models for cheap roles*
>  *  - **Max (5x or 20x)** — full fan-out, default model everywhere*
>  *  - **Not sure / prefer not to say** — Pro-flavored defaults (safer fallback)"*

Update `profile.plan` in settings.yml:

- **`pro`** — also set `team_chat: minimal` (already the default in Step 4's template — keep it), and **add or update** the per-role overrides for low-output roles:
  ```yaml
  role_models:
    licensing: claude-haiku-4-5
    accessibility: claude-haiku-4-5
  ```
- **`max5x` / `max20x`** — leave defaults as-is.
- **`unspecified`** — leave defaults as-is (template is already Pro-flavored).

These two questions are the *only* setup prompts — do not ask about role fluency per discipline at first-run. Roles will learn fluency from lived signal over time, or the user can fill it in via `~/.hacky-hours/settings.yml` whenever they want.

## Step 6 — Tell the user what just happened and what's next

Print:

> *"Done. Your setup lives at `~/.hacky-hours/`:*
> *  - settings.yml — your preferences*
> *  - teams/ — your AI team will live here (empty for now; we'll create your first team when you need it)*
> *  - feedback/, sessions/, versions/ — operational folders*
>
> *Everything is local, private, and yours.*
>
> *Now — what were you trying to do? A few common starting points:*
> *  - `/hacky-hours team` to set up your first team*
> *  - `/hacky-hours adopt` to bring an existing codebase into the framework*
> *  - `/hacky-hours ideate` to start a new project from an idea*
> *  - or just describe what you want in your own words"*

## Step 7 — Return control to routing

After printing the above, **return control to whatever the user's original argument was** (or to the no-arg guided session if there was no argument). Do not start a new flow on your own.

If the user is mid-context (e.g., they were running `/hacky-hours adopt` when first-run was triggered), proceed with their original command now that setup is complete.

---

## Idempotency

If this file is invoked again (e.g., the user manually triggered setup) and `~/.hacky-hours/` already exists, do not overwrite anything. Instead, summarize current state:

```
~/.hacky-hours/ already exists.
  Framework version on file: <contents of `version`>
  Teams installed: <count of subdirs under teams/>
  Settings: ~/.hacky-hours/settings.yml (last modified <date>)
```

And offer to `/hacky-hours team` for managing teams or `/hacky-hours update` to update the framework.
