# ITERATION.md

Post-release brain dump for the cycle following v1.7.0.

---

## Raw Ideas

### 1. `/hacky-hours tour` — Guided Tour

A command that takes a new person on a curated walkthrough of the project.
- Focus is selectable: design docs only, architecture, data model, everything
- Logical linear progression that encourages exploration into the root docs
- Baseline: Claude Code conversation mode
- Optional: generates a static site in `hacky-hours/learn/tour/` (general) or `hacky-hours/learn/personal/<username>/` (personalized, gitignored by default)
- Site includes a markdown editor / feedback form where the reader can write notes and submit them; submission saves a `feedback-<username>-<timestamp>.md` file to `hacky-hours/feedback/`

**Motivation:** New people are bad at getting context from other humans. A structured walkthrough beats "go read the docs."

---

### 2. `/hacky-hours onboard` — Hands-On Task Scoping

Helps engineers get hands-on with a codebase by doing real (but scoped) work.
- Without arguments: best judgment on where to start
- With arguments: scoped to a specific area ("database", "api", "the bar chart component")
- Gives a quick run-through of the relevant area, then proposes a starter task that teaches without breaking things
- Optionally creates a GitHub Issue tagged `[hacky-hours]` + `onboarding` with full context
- On wrap-up: commits and pushes any generated feedback file, optionally opens an issue
- Useful for new engineers AND experienced engineers switching to an unfamiliar part of the stack

**Motivation:** Learning by doing beats reading. A well-scoped task with context beats "figure it out."

---

### 3. `/hacky-hours quiz` — Knowledge Verification

Tests knowledge about the project or codebase.
- Can be broad (whole project) or drilled down to a specific area
- Baseline: Claude Code conversation mode
- Optional: generates a static site quiz in `hacky-hours/learn/quiz/` (general, permanent) or temp folder (gitignored, user can promote)
- Questions derived from hacky-hours docs + codebase

**Motivation:** Knowledge verification after a tour or onboarding period. Also useful as a self-check for experienced engineers picking up a new area.

---

### 4. `TESTING.md` Design Doc Template

No current testing design document exists. The pre-merge checklist mentions manual testing but there's no structured thinking about test strategy, automation, coverage goals, or TDD.
- New Level 2 design doc template: `02-design/TESTING.md`
- Scaffold should include it by default
- Audit Phase 2 should check it alongside SECURITY_PRIVACY and ACCESSIBILITY

---

### 5. Audit Scorecard — All Design Domains

Current audit Phase 2 only checks BACKLOG, CHANGELOG, LICENSE, SECURITY_PRIVACY, and ACCESSIBILITY. Should cover every design doc type the project has with a consistent per-domain format: exists? filled in? up to date? specific gaps?

Not just a checklist — actionable output per domain.

---

### 6. `/hacky-hours upgrade` — Project Artifact Migration

When the hacky-hours command is updated, existing project artifacts don't know what changed. `upgrade` diffs the installed command version against what's in the user's scaffold and walks them through adopting new artifacts (new doc templates, new scaffold folders, new `.claudeignore` entries).

Note: `/hacky-hours update` (pulling upstream) was considered and dropped — it would blow away customizations for forked repos. `upgrade` operates on the user's own project artifacts only.

---

## Settled Decisions

- **Three separate commands:** `tour`, `onboard`, `quiz`
- **Conversation mode is the baseline** for all three — always available, no dependencies. Static site is an optional richer layer on top, same content.
- **Static site stack: Astro** — better component model for interactive features (feedback form, quiz UI), Markdown-native content collections, good community momentum. Content lives in `.md` files; I regenerate content, not HTML.
- **Folder name: `hacky-hours/learn/`** — unifies tour, quiz, and personalized content under one roof. Not docs, not build artifacts — learning material.
  - `hacky-hours/learn/tour/` — general tour site
  - `hacky-hours/learn/quiz/` — general quiz site
  - `hacky-hours/learn/personal/` — gitignored; scoped to `<username>`, temp until promoted
- **Feedback folder: `hacky-hours/feedback/`** — separate from `learn/`; user input not generated content. Filename: `feedback-<username>-<timestamp>.md`. Ingested by `iterate` Step 1 Capture.
- **GitHub Issue identity model:** `onboard` uses same pattern as `sync --issues` — `[hacky-hours]` label + new `onboarding` label, `#<number>` annotation in BACKLOG.
- **`/hacky-hours update` dropped** — bad for forks. `upgrade` is the right scope.

## Open Questions

- Should `hacky-hours/learn/` be in `.claudeignore` by default? (Probably yes — generated assets.)
- Does `upgrade` belong as a standalone command or as a phase within `audit`? (Leaning standalone — audit is read-only by design.)
- What format does `upgrade` use to know what the "current version expects"? (A migration manifest in the command prompt? A `## What's new in vX.Y` section?)
