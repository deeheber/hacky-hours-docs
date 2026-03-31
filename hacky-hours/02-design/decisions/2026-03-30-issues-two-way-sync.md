# ADR: Two-Way GitHub Issues Sync with Last-Write-Wins

**Date:** 2026-03-30
**Status:** Accepted
**Relates to:** ARCHITECTURE.md, command prompt (`sync` command)

## Context

BACKLOG.md is the local source of truth for hacky-hours users. But collaborators who don't use hacky-hours (or work outside Claude Code sessions) track work via GitHub Issues. There's no bridge between the two — items added in one place don't appear in the other, and drift accumulates silently.

The existing `sync` command only publishes GitHub Releases from CHANGELOG entries. The backlog item for "GitHub Issues ↔ BACKLOG reconciliation" has been in the Future section since v1.4.0.

## Decision

Expand `sync` with a `--issues` flag that performs two-way reconciliation:

**Push (BACKLOG → Issues):**
- Items in BACKLOG.md without a `#<number>` annotation get created as GitHub Issues
- Items with an annotation get compared; if the BACKLOG text differs from the Issue body, show the diff
- Created Issues get a `[hacky-hours]` label for filtering

**Pull (Issues → BACKLOG):**
- Open Issues with the `[hacky-hours]` label that aren't in BACKLOG.md get proposed for addition
- Issues without the label are ignored (they're outside the framework's scope)

**Conflict resolution: last-write-wins with human confirmation.**
- When both have changed, show both versions side-by-side
- User picks which version to keep (or edits manually)
- No automatic resolution — every conflict requires explicit confirmation

**Identity linking:**
- BACKLOG.md items include `#<number>` after the item description
- GitHub Issues include `[hacky-hours]` label
- Matching is by issue number, not by title fuzzy match

## Consequences

- `sync` now has two modes: `sync` (releases, unchanged) and `sync --issues` (issue reconciliation)
- The `[hacky-hours]` label must be created in the repo (sync can offer to create it)
- BACKLOG.md format gains a convention: `#<number>` suffix links to an Issue
- Neither source is canonical — this is a deliberate tradeoff favoring flexibility over consistency
- Conflict resolution adds friction to the sync process, but prevents silent data loss
