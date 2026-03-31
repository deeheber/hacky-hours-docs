# Keeping Your Docs Clean

As your project grows, its documentation can become a liability — bloated files make it harder for Claude to give accurate answers, documents start contradicting each other, and it becomes unclear what's actually true right now. This runbook describes how to keep your framework documents lean, accurate, and useful over time.

> **Good news:** If you're using the `/hacky-hours` command, most of this happens automatically. The `iterate`, `audit`, and `optimize` commands handle archiving, cleanup, and consistency checks for you. This runbook explains the *why* behind what those commands do — and covers manual maintenance for people who don't use the command.

---

## The Core Principle

Documents should reflect **current state**, not accumulated history. Git already keeps a complete record of every version of every file. Your working docs are the *current* version — not the archive.

---

## Which Documents Matter Right Now?

Not every document needs to be front-and-center at all times. Think of them in three groups:

| Group | Documents | When you need them |
|-------|-----------|-------------------|
| **Active** | `BACKLOG.md`, the design docs you're currently building from, `PRODUCT_OVERVIEW.md` | Every session — these define what you're doing right now |
| **Reference** | `ROADMAP.md`, `CHANGELOG.md` | When planning or reviewing — useful but not always needed |
| **Historical** | `IDEATION.md`, completed milestone notes, old decision records | Rarely — background context only |

As documents become less relevant to your current work, move them to the `archive/` folder. Don't delete them — just move them out of the way so they don't clutter things up.

---

## How Each Document Works

### BACKLOG.md — your to-do list

BACKLOG.md holds only what's left to build. It's a queue, not a history.

- Add items when you're planning what to work on next
- Remove items when the work is done and merged — don't mark them as complete, just delete the line
- When the backlog is empty, the milestone is done
- Completed work goes in CHANGELOG.md, not here

### CHANGELOG.md — your release history

CHANGELOG.md records what you shipped. Each release gets an entry with a version number and date.

- Add a new section each time you finish a milestone and tag a release
- Keep only the **last 3 releases** in the file — move older entries to `archive/changelog/`
- GitHub Releases holds the full history; this file is a quick reference

### Design documents — keep them current

Documents like ARCHITECTURE.md, DATA_MODEL.md, etc. describe how your product works *today*. When a design decision changes:

- Don't rewrite the whole document — you'll lose the reasoning behind the original choice
- Instead, write a short **decision record** (a note explaining what changed and why) in `02-design/decisions/`
- Name it by date and topic: `2026-03-20-switch-to-postgres.md`
- Update only the affected sections of the original doc, with a note like: "See `decisions/2026-03-20-switch-to-postgres.md` for why this changed"

A decision record looks like this:

```markdown
# [What changed]

**Date:** YYYY-MM-DD
**Status:** Accepted

## Context
What was true before, and what prompted the change?

## Decision
What did you decide?

## Consequences
What does this mean going forward?
```

### PRODUCT_OVERVIEW.md — always up to date

Update this whenever your core who/what/where/when/why changes. It should describe the product as it is now, not as you originally imagined it.

### IDEATION.md — archive after Level 1

Once PRODUCT_OVERVIEW.md is solid, move IDEATION.md to `archive/`. It did its job. Keeping it in the active set adds noise.

### ROADMAP.md — trim completed milestones

When a milestone is done, move its section to `archive/roadmap/`. The active roadmap should only show what's ahead.

---

## The archive/ Folder

```
archive/
  changelog/        # Old CHANGELOG entries
  roadmap/          # Completed milestone sections
  IDEATION.md       # Moved here after Level 1 is complete
```

`archive/` is cold storage, not a graveyard. Everything in it is still accessible through git, but keeping it in a named folder makes it findable without cluttering your working docs.

---

## Telling Claude What to Skip

The `.claudeignore` file lists files and folders that Claude should skip when building context for a session. This keeps Claude focused on what matters right now instead of getting distracted by historical documents.

The framework creates a default `.claudeignore` when you scaffold a project:

```
hacky-hours/archive/
hacky-hours/audits/
hacky-hours/04-build/CHANGELOG.md
hacky-hours/01-ideate/IDEATION.md
```

**Add files to `.claudeignore` when:**
- They're historical and no longer reflect how things work today
- They're large and rarely relevant to what you're building right now
- Claude keeps referencing outdated information from them

**Remove files from `.claudeignore` when** you're specifically working on them and need Claude to read them.

---

## End-of-Milestone Checklist

Run through this when your backlog is empty and you're ready to call a milestone done:

```
[ ] Remove completed items from BACKLOG.md
[ ] Add a milestone entry to CHANGELOG.md
[ ] Move CHANGELOG entries older than 3 releases to archive/changelog/
[ ] Move the completed roadmap milestone to archive/roadmap/
[ ] Update any design docs that changed — write decision records for significant changes
[ ] Move IDEATION.md to archive/ if it hasn't been already
[ ] Review .claudeignore — anything newly historical that should be excluded?
```

---

## Related

- [BACKLOG.md template](../04-build/BACKLOG.md)
- [CHANGELOG.md template](../04-build/CHANGELOG.md)
- [contributing.md](./using-this-repo/contributing.md)
