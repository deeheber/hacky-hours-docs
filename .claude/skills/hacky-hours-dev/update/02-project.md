# Update 2 — Sync Issues

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `update 2` / `update project`.*

**Context:** Read `04-build/BACKLOG.md` under ROOT_PATH.

**Purpose:** Two-way reconciliation between BACKLOG.md and GitHub Issues. Neither source is canonical — the user resolves all conflicts at sync time.

**Always confirm before creating, updating, or closing anything.**

**Step 1: Verify gh is set up** — same as Update 1 Step 1.

**Step 2: Ensure the `hacky-hours` label exists**

```bash
gh label list --search "hacky-hours" --json name
```

If missing, ask to create it:

```bash
gh label create "hacky-hours" --description "Tracked in hacky-hours BACKLOG.md" --color "0E8A16"
```

**Step 3: Read both sources**

Read BACKLOG.md and parse each item. Look for `#<number>` annotations (explicitly linked items).

```bash
gh issue list --label "hacky-hours" --state open --limit 100 --json number,title,body,updatedAt
gh issue list --label "hacky-hours" --state closed --limit 50 --json number,title,body,closedAt
```

**Step 4: Sort into buckets**

1. **Push (BACKLOG → Issues):** BACKLOG items without `#<number>` annotation
2. **Pull (Issues → BACKLOG):** Open issues with `hacky-hours` label not in BACKLOG
3. **Diverged:** Linked items where text has changed in one or both
4. **Stale:** BACKLOG items linked to now-closed issues

**Step 5: Present the diff**

Show a clear summary of each bucket with proposed actions. For diverged items, show both versions side-by-side.

**Step 6: Confirm and execute**

For each bucket, ask for confirmation before acting. After all actions complete, show a summary.

**Step 7: Report**

```
Sync complete:
  Created: N new Issues
  Added to BACKLOG: N items
  Updated: N diverged items resolved
  Removed: N stale items cleaned up
  Skipped: N items (no action taken)
```
