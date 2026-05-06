# Learn 2 — Onboard

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `learn 2` / `learn onboard [area]`.*

**Context:** Read the design docs and codebase relevant to the requested area. Don't ask the user to tell you things you can read.

**Purpose:** Get an engineer hands-on with a specific area through a real but safely scoped task.

**Phase 1: Determine scope**

If an area was specified, confirm and proceed. If not: read the codebase and BACKLOG.md. Pick an area that is well-documented, not in active development, and self-contained enough for a clear starter task. Present your choice and ask for confirmation.

**Phase 2: Orient**

Give a 3-5 paragraph orientation: what this area does, how it connects to other parts, what the main files are, what the tricky parts are.

**Phase 3: Scope a starter task**

Propose a task that is small, has clear success criteria, teaches something real, and won't break existing functionality. Read `SECURITY_PRIVACY.md` (or its summary + deep pair) and `TESTING.md` before proposing.

**Phase 4: Create GitHub Issue (optional)**

If `gh` is available and the user says yes: create with `hacky-hours` + `onboarding` labels.

**Phase 5: Wrap up and save feedback**

Ask about anything confusing. Save feedback to `ROOT_PATH/feedback/feedback-<username>-<timestamp>.md`.

Then: "I'll commit and push the feedback file so it's captured for the next iteration cycle."

Before pushing: show the exact content, stage only the feedback file (never `git add -A`), confirm, warn if the repo is public. Then: `git add <path>`, `git commit -m "feedback: onboard session for <area> by <username>"`, `git push`.
