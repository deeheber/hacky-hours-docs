# ITERATION.md — Post v1.4.0

Captured: 2026-03-30

---

## 1. `/hacky-hours optimize` — token efficiency evaluation

**Resolved:** Standalone command + lighter check within iterate Step 2.

Standalone command scans all framework docs and reports:
- Command prompt size (token estimate)
- Context load per session (how many docs does a typical command read?)
- Doc staleness (last modified vs. last referenced in commits)
- Doc density (placeholder text vs. real content)
- Suggestions: archive, consolidate, or trim

Iterate integration: during Step 2 (synthesize), flag oversized/stale docs as part of the review.

## 2. `/hacky-hours pivot` — product re-ideation cycle

**Resolved:** New command. Not iterate, not ideate — a third lifecycle path.

Reads ALL existing artifacts as context, takes the user back through Level 1 questions ("is this still true?"), and cascades changes through Levels 2-4. Produces a diff against current state. Doc refactoring (merge, split, retire) is a natural output of this process. ADRs for significant direction changes.

Lifecycle model becomes:
```
ideate → design → roadmap → build → iterate → build → ...
                                         ↓
                                       pivot → re-ideate (with context) → cascade 2/3/4
```

## 3. `/hacky-hours sync --issues` — two-way GitHub Issues sync

**Resolved:** Last-write-wins with conflict detection. Show diff, ask for confirmation before applying any changes.

- **Push:** BACKLOG.md items → GitHub Issues (create/update)
- **Pull:** GitHub Issues → BACKLOG.md (new issues get proposed for addition)
- **Identity:** Issue number annotation in BACKLOG.md (`#42`), `[hacky-hours]` label on Issues
- **Conflicts:** Show both versions side-by-side, user picks
- **Authority:** Neither source is canonical — human resolves all conflicts at sync time

Expands existing `sync` command: `sync` (releases, current behavior), `sync --issues` (issue reconciliation).

---

## Triage

All three → **v1.5.0 next milestone**

| Item | Scope |
|------|-------|
| `/hacky-hours optimize` | Full implementation |
| `/hacky-hours pivot` | Full implementation |
| `sync --issues` | Full implementation |
