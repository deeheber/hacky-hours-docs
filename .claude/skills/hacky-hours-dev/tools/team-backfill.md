# /hacky-hours team backfill — retroactive history population

For projects that existed before Slice 12 (or that ran on Slice 12 without conducting `team update`), agents' `history.md` files are blank even though the team has done real work. `team backfill` walks the bound project's CHANGELOG or git log, classifies each entry by which discipline(s) it touched, and lets the conductor batch-review per-agent history proposals.

This is the **one-shot retroactive companion** to forward-capture (Stash phase in multi-role verbs). After backfill, the agents' `history.md` files reflect the project's lifetime, not just post-Slice-12 activity. The team site comes alive on day-one of v4.0.0 install for already-mature projects.

Contract source: `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Backfill semantics".

---

## Step 0 — Pre-flight

1. **Active team:** read project `AGENTS.md` for `team:` field. Default to `default` if absent.
2. **Team repo exists:** `~/.hacky-hours/teams/<active>/agents/` must exist. If not: print *"No team to backfill into — run `/hacky-hours team init` first."*
3. **Source detection:** check (in order of preference):
   - `CHANGELOG.md` (or `hacky-hours/04-build/CHANGELOG.md`) — structured, slice-based, low classification noise
   - `git log` (if `.git/` exists) — finer-grained, more noise, recommended for projects without a CHANGELOG
   - If neither exists: print *"Need a CHANGELOG.md or a git repo to backfill from. Nothing to work with here."* and exit.
4. **Argument parsing:** `/hacky-hours team backfill [flags]`
   - `--source changelog|git|both` — override auto-detection (default: prefer changelog, fall back to git)
   - `--since <YYYY-MM-DD>` — only backfill entries from this date forward (default: full history)
   - `--dry-run` — show the proposed history without writing or committing
   - `--agent <agent-id>` — restrict to one specific agent (useful for incremental backfill)

## Step 1 — Surface the plan and confirm scope

Print a summary before doing any reads:

> *"Backfill plan:*
> *  - Source: <CHANGELOG.md | git log | both>, <N> entries detected*
> *  - Date range: <since> → today*
> *  - Target team: <team-name> at `~/.hacky-hours/teams/<team>/`*
> *  - Agents in scope: <list> (<count> total)*
> *  - Current state: <count> agents already have history entries (will append, not replace); <count> are blank*
>
> *Backfill is read-only on your project. It writes per-agent batches to the team repo after you accept each one. Existing entries are preserved; backfilled lines are tagged with `(backfilled, <commit-or-changelog-anchor>)` so they're distinguishable from forward-captured entries.*
>
> *Proceed? (yes / dry-run / cancel)"*

Wait for confirmation.

## Step 2 — Read and parse the source

### Source: CHANGELOG.md

Parse CHANGELOG by Markdown headings. Each `### Added (<topic>)` or `### Changed` section under a version (`## [Unreleased]` or `## [X.Y.Z]`) is one **entry**. Bulleted list items inside are the entry's details.

For each entry, extract:
- Date — from the version's `## [X.Y.Z] — YYYY-MM-DD` header (or `## [Unreleased]` → today's date)
- Topic — from the `### Added (<topic>)` parenthetical, falling back to the `###` heading text
- File paths mentioned — grep for backticks containing `/` or `.md`/`.py`/`.ts`/etc. in the bullet content
- Keywords — discipline-tagging keywords (see classification table below)
- Anchor — anchor link to the entry: `CHANGELOG.md#<version-slug>`

### Source: git log

```bash
git log --since="<since>" --pretty=format:"%h|%ad|%s|%b" --date=short --name-only
```

For each commit, extract:
- SHA (short)
- Date
- Subject line
- Body (for slice references)
- Files changed (`--name-only`)
- Keywords from message + files

### Source: both

Read changelog first, then walk git log for the period covered. Cross-reference: if a CHANGELOG entry mentions a slice number that maps to a commit, attach the SHA to that CHANGELOG entry rather than producing a separate git-derived entry.

## Step 3 — Classify each entry by agent

For each entry, determine which agents in the active team's tier.yml were involved. Use this classification table as the primary signal; LLM judgment fills gaps.

| Signal | Likely agent(s) |
|--------|------------------|
| Files in `02-design/ARCHITECTURE*` or `02-design/decisions/` | Architect |
| Files in `02-design/SECURITY_PRIVACY*` or `audits/` security findings | Security |
| Files in `02-design/ACCESSIBILITY*` | Accessibility |
| Files in `02-design/USER_JOURNEYS*` or `STYLE_GUIDE*` | Design |
| Files in `02-design/DATA_MODEL*` | Data + Backend (co-author) |
| Files in `02-design/TESTING*` | QA |
| Files in `02-design/LICENSING*` | Licensing |
| Files in `01-ideate/PRODUCT_OVERVIEW*` or `03-roadmap/ROADMAP*` | Product |
| Files in `runbooks/` | Ops |
| Keyword "AI/ML", "eval", model name | AI/ML |
| Files matching `*.tsx`, `*.jsx`, `components/`, `pages/`, CSS | Frontend |
| Files matching `*.py`/`*.go`/`*.ts` API handlers, `routes/`, `controllers/` | Backend |
| Commit-message prefix `feat:`/`fix:`/`docs:`/`test:`/`refactor:` | Map to discipline of changed files; if ambiguous, Product owns the user-facing slice |
| Multi-discipline slice (e.g., "Slice 11 — team chat") | All agents named in the slice description; cross-check with V4_DESIGN.md role assignments |

**Multi-agent entries are fine** — a single CHANGELOG entry can produce history lines for several agents. E.g., "Slice 2 — default team roster" touches Product (roster decisions), Design (avatar personalities), Licensing (per-agent LICENSE), and Architect (file structure).

**Unclassifiable entries** — if no signal matches, default to **Product** as the owner-of-record (Maya tracks all milestones) but flag the entry in the per-agent review as "low confidence classification" so the conductor can decline if it doesn't fit her track.

## Step 4 — Compose proposed history lines

For each (entry, agent) pair, compose a one-line history entry per the canonical format from `references/capture-format.md`:

```
- <date> · <project-slug> · <verb> (backfilled, <anchor>) · <one-sentence past-tense contribution summary>
```

Where:
- `<verb>` — best guess at which verb would have produced this entry: `adopt`, `design`, `build`, `audit`, `arbitrate`, `iterate`, etc. For a CHANGELOG slice entry, use `build:<slice-slug>`. For an unscoped commit, use `build:<short-sha>`.
- `<anchor>` — for CHANGELOG entries: `CHANGELOG#<version-anchor>`. For git entries: short SHA.
- `<summary>` — concrete contribution from this agent's lens. Not "worked on Slice 2" — instead, for Maya on Slice 2: "Defined the 12-role default team roster and per-agent ownership boundaries."

Group proposed entries per agent. Sort chronologically (oldest first within an agent — that's how `history.md` is meant to read).

## Step 5 — Per-agent batch review

For each agent with proposed entries, present a batch:

```
=== Maya Tanaka (Product) — proposed backfill: <N> entries ===

  1. 2026-04-11 · hacky-hours-docs · build:v2.0.0 (backfilled, CHANGELOG#200) · Authored v2.0.0 command surface redesign — proposed five-step parent grouping; pushed back on /link feature complexity.
  2. 2026-04-18 · hacky-hours-docs · build:v2.1.0 (backfilled, CHANGELOG#210) · Approved scope of upgrade-flow boilerplate migration as essential debt-paydown.
  3. 2026-05-06 · hacky-hours-docs · build:v3.0.0 (backfilled, CHANGELOG#300) · Confirmed two-tier design template pattern as the right Phase 2 evolution.
  ...

Confidence per entry: high · high · high · medium · high · high

Batch options:
  a) accept all       — write the whole batch to Maya's history.md
  s) select           — pick specific entries to accept; others dropped
  e) edit             — revise specific summaries before accepting
  r) reject all       — drop the whole batch
  d) defer            — keep proposals around; review next time
```

Wait for conductor input per agent. Process:

- **accept all:** append all entries to `~/.hacky-hours/teams/<active>/agents/<agent-id>/history.md` under the `## Recent` section (create the heading if absent). Sort chronologically, newest-on-top within the section per the canonical format.
- **select:** prompt for entry numbers to accept (e.g., `1, 3, 5-8`); reject unlisted; write accepted ones.
- **edit:** prompt for which entries to revise; re-present each with conductor's edits applied; ask for final accept/reject.
- **reject all:** drop everything for this agent; move to next.
- **defer:** persist the proposed batch to `~/.hacky-hours/sessions/<session-id>/backfill-pending/<agent-id>.md` so a later run can resume; move to next agent.

## Step 6 — Refresh metrics + commit per batch

After each agent's batch is resolved (not at the end of the whole verb):

1. **Refresh the agent's derived metrics** in `profile.md` frontmatter per `${CLAUDE_SKILL_DIR}/references/capture-format.md` §"Derived metrics" + §"Level derivation". Backfilled entries count the same as forward-captured ones — the `metrics_refreshed`, `last_active`, `projects`, `verbs_run`, and `level` fields all update. (The `(backfilled, ...)` annotation in `history.md` doesn't change how the line is counted; it's display-only.)
2. **Commit history + metrics together:**

```bash
cd ~/.hacky-hours/teams/<active>/
git add agents/<agent-id>/history.md agents/<agent-id>/profile.md
git commit -m "history: backfill @ <project> — <agent-id> (<N> entries from <source>)"
```

Per-agent commits keep the team-repo log clean and rewindable — if the conductor regrets one agent's batch later, they can revert just that commit without affecting other agents' backfill work. Metrics changes ride along in the same commit, so reverting an agent's backfill cleanly rolls back their level/contribution counts too.

## Step 7 — Footer summary

```
Backfill complete.

  Maya (Product):        12 entries accepted
  Felix (Design):         3 entries accepted, 1 rejected
  Priya (Architect):     18 entries accepted
  Alex (Security):        6 entries accepted, 2 edited
  Lena (A11y):            2 entries accepted
  Diego (Licensing):      1 entry accepted
  Emma (QA):              4 entries accepted
  Yuki (Data):            0 entries (no signal in source)
  Jordan (Ops):           3 entries accepted
  Sam (Backend):          0 entries (no FE/BE code in this project)
  Marcus (Frontend):      0 entries (no FE code in this project)
  Kai (AI/ML):            0 entries (no AI/ML in this project)

Team repo: <N> commits added (one per agent batch).
Team site will reflect the new history on next `team site build`.

This is a one-shot operation — subsequent project activity is captured automatically via Stash phase in multi-role verbs (per references/capture-format.md). Run /hacky-hours team backfill again later only if you want to fill in additional history (e.g., after the CHANGELOG grows further pre-Slice-12 entries you discover).
```

## Edge cases

- **Empty CHANGELOG.** Fall back to git log automatically (announce the fallback). If git is also empty: exit with *"Nothing to backfill from."*
- **Conductor selects `--dry-run`.** Skip Step 5 interactivity and Step 6 commits. Print the proposed entries grouped by agent. Useful for getting a sense of scope before committing.
- **Restricted to `--agent <id>`.** Only process classifications matching that agent. Skip per-agent review for others. Useful for "I just want to fill in Priya's history."
- **An agent's `history.md` already has entries from forward-capture.** Append backfilled entries chronologically — they'll naturally appear *before* the forward-captured ones since they predate them. The `(backfilled, ...)` annotation distinguishes them.
- **Conductor invokes backfill twice on the same project.** Second run sees existing backfilled entries (they're in `history.md` with the annotation) — skip producing duplicate proposals. Compare proposed anchor against existing entries; skip matches.
- **Cross-project backfill.** Backfill always targets the *active* project (cwd). To backfill a different project, `cd` into it first. The verb does not accept project paths as arguments — keep the scope simple.
- **Team has uncommitted changes.** Surface to conductor: *"Team repo has uncommitted changes. Backfill commits will mix with them. Stash team changes first or proceed with bundled commits?"* Default: ask.

## What this verb closes

Pre-Slice-12 projects (or post-Slice-12 projects where conductors never ran multi-role verbs through the Stash phase) start with empty `history.md` files. The team site renders agent profiles with no track record. Slice 12's forward-capture closes the loop for *future* work but leaves *past* work invisible.

Backfill closes the past-work gap as a one-shot retroactive operation. After running it on a mature project, agents on the team site show histories that match the project's lifetime — Maya's track record reflects every CHANGELOG entry she shaped, Priya's reflects every architecture decision, and so on. The team site stops looking like a brand-new team and starts looking like a team that's been here all along.

## Notes for the assistant running this

- **Per-agent batches, not per-entry prompts.** A project with 30 CHANGELOG entries × 12 agents could produce 360 entries. Per-entry review would be a slog; per-agent batch with `select` keeps it tractable.
- **Confidence is signal, not gate.** Even low-confidence classifications should be presented — the conductor's `select` action is the gate. Don't auto-drop low-confidence entries.
- **Honest summaries.** A backfilled summary should be defensible against the source it cites. If the conductor reads "Maya — Approved scope of upgrade-flow as essential debt-paydown" and the CHANGELOG entry it cites contains no scope discussion, that's a hallucinated summary. Better: stick close to what's in the source ("Authored upgrade-flow scaffold migration") and let the conductor edit.
- **Backfill is opt-in, not run-automatically.** Do not invoke from `adopt` or other verbs. The conductor must explicitly choose to retrofit history.
- **The team-update review flow is for forward-captured behavior feedback.** Backfill writes directly to `history.md` per the silent-fact-of-record contract for history — but with the per-agent batch review gate above replacing the silence, since the conductor isn't watching turn-by-turn during a one-shot bulk operation.
