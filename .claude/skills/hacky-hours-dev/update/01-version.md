# Update 1 — Publish Release

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `update 1` / `update version`.*

**Context:** Read `04-build/CHANGELOG.md` under ROOT_PATH to find the latest version entry. Check `04-build/BACKLOG.md` — if not empty, the milestone isn't done; suggest running `/hacky-hours review 1` first.

**Purpose:** Take the latest CHANGELOG entry and publish it as an official GitHub Release.

**Always confirm before taking any action. This writes to a shared, public system. Never run any action without explicit confirmation.**

**Step 1: Verify gh is set up**

Run `gh auth status`. If not authenticated: tell the user to run `gh auth login`. Stop until resolved.

**Step 1b: Check Issues ↔ BACKLOG alignment**

```bash
gh issue list --state open --limit 100 --json number,title
```

Compare against `04-build/BACKLOG.md`. Warn if open issues don't appear in BACKLOG, or if BACKLOG is empty but open issues remain. This is advisory — the user can proceed regardless.

**Step 2: Read the latest CHANGELOG entry**

Extract the most recent version entry. Show it: "Is this the release you want to publish?"

If CHANGELOG has no entries, stop and tell the user to add one.

**Step 3: Confirm the tag**

```bash
git tag --list "<version>"
```

If the tag doesn't exist, ask the user to confirm creating it:

```bash
git tag <version>
git push origin <version>
```

Show these exact commands and ask for confirmation before running. Explain what a tag is.

**Step 4: Preview and confirm**

Show exactly what will be published. Ask: "Does this look right? Once published, this will be visible on your GitHub repo's Releases page."

**Step 5: Publish**

After explicit confirmation:

```bash
gh release create <version> --title "<version>" --notes "<full changelog entry>"
```

After publishing: tell the user where to find their release (GitHub repo → Releases tab).
