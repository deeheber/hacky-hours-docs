# Document Hygiene

As a project grows, its documentation can become a liability — bloated files make it harder for Claude to give accurate, focused answers, documents start contradicting each other, and it becomes unclear what's actually true right now. This runbook describes how to keep the framework documents lean, accurate, and useful over time.

---

## The Core Principle

Documents should reflect **current state**, not accumulated history. Git is the historical record. The docs are the working set.

---

## Hot / Warm / Cold Tiers

Not all documents need to be in context at all times. Organize your mental model — and your `.claudeignore` — around three tiers:

| Tier | Documents | When to read |
|------|-----------|--------------|
| **Hot** | `04-build/BACKLOG.md`, active design docs, `01-ideate/PRODUCT_OVERVIEW.md` | Always — these define what you're doing right now |
| **Warm** | `03-roadmap/ROADMAP.md`, `CHANGELOG.md` | On demand — useful for planning and review |
| **Cold** | `01-ideate/IDEATION.md`, `archive/`, superseded design decisions | Rarely — historical reference only |

Move documents to a colder tier as they become less relevant. Don't delete them — archive them.

---

## Per-Document Lifecycle

### BACKLOG.md — strict queue

BACKLOG.md is a **queue**, not a ledger. It holds only what is left to build.

- Add items at triage (from `iterate` or planning sessions)
- Remove items when their PR is merged — don't mark them done, delete the line
- An empty BACKLOG means the milestone is complete
- Never use BACKLOG as a record of completed work — that's what CHANGELOG is for

### CHANGELOG.md — append-only, trimmed periodically

CHANGELOG.md is a **ledger**. Completed work lands here with a version tag and date.

- Append a new entry for each merged milestone
- Keep only the **last 3 releases** in the file — move older entries to `archive/changelog/`
- GitHub Releases holds the canonical history; the file is a quick human reference

### Design docs — amend with decision records

Design documents (ARCHITECTURE.md, DATA_MODEL.md, etc.) describe **how the product works today**. When a design decision changes:

- Do **not** rewrite the original document in place — this loses the reasoning behind the original decision
- Instead, write a small **Architecture Decision Record (ADR)** — a short note recording what changed and why — in `02-design/decisions/`
- Name it by date and topic: `2026-03-20-switch-to-postgres.md`
- Keep the original doc accurate by updating only the affected sections, with a note: `See decisions/2026-03-20-switch-to-postgres.md`

ADR format:

```markdown
# [Decision title]

**Date:** YYYY-MM-DD
**Status:** Accepted

## Context
What was true before, and what changed?

## Decision
What did we decide?

## Consequences
What does this mean for the product going forward?
```

### PRODUCT_OVERVIEW.md — living document

Update PRODUCT_OVERVIEW.md whenever the core who/what/where/when/why changes. It should always reflect the product as it is now, not as it was envisioned at the start.

### IDEATION.md — archive after Level 1 is complete

Once PRODUCT_OVERVIEW.md is finalized, move IDEATION.md to `archive/`. It served its purpose. Keeping it in the working set adds noise without value.

### ROADMAP.md — trim completed milestones

When a milestone is complete, move its section from ROADMAP.md to `archive/roadmap/`. The active roadmap should show only what's ahead.

---

## The archive/ Folder

```
archive/
  changelog/        # Old CHANGELOG entries (pre-last-3-releases)
  roadmap/          # Completed milestone sections
  decisions/        # (or keep these in 02-design/decisions/ — your call)
  IDEATION.md       # Moved here after Level 1 is complete
```

`archive/` is not a graveyard — it's cold storage. Everything in it is accessible via git anyway, but keeping it in a named folder makes it findable without being noisy.

---

## .claudeignore

The `.claudeignore` file is a convention — not a natively enforced feature. To make it work, add a line to your `CLAUDE.md`:

```markdown
When building context, skip any files or folders listed in `.claudeignore`.
```

With that instruction in place, Claude will respect the file. The scaffold creates a default `.claudeignore` — adjust it as your project evolves.

Default contents:

```
archive/
CHANGELOG.md
01-ideate/IDEATION.md
```

Add files to `.claudeignore` when:
- They're historical (no longer reflect current state)
- They're large and rarely relevant to active work
- They're causing Claude to give outdated or confused answers

Remove files from `.claudeignore` when you're specifically working on them.

---

## Housekeeping Checklist (run at end of each milestone)

```
[ ] Remove completed items from BACKLOG.md
[ ] Append milestone entry to CHANGELOG.md
[ ] Move CHANGELOG entries older than 3 releases to archive/changelog/
[ ] Move completed roadmap milestone to archive/roadmap/
[ ] Update any design docs that changed — write ADRs for significant decisions
[ ] Move IDEATION.md to archive/ if Level 1 is complete and it hasn't been already
[ ] Review .claudeignore — anything newly cold that should be excluded?
```

---

## Related

- [BACKLOG.md template](../04-build/BACKLOG.md)
- [CHANGELOG.md template](../04-build/CHANGELOG.md)
- [contributing.md](./using-this-repo/contributing.md)
