# Tools: Upgrade

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `tools upgrade`.*

**Context:** Read the user's `CLAUDE.md` for a version marker. Read ROOT_PATH/02-design/ and the scaffold to compare against what the current version expects. For new codebases, read as much of the existing code as possible before asking questions.

**Purpose:** Unified command for framework artifact management. Detects context and runs the appropriate flow.

**Always confirm before writing any files.**

---

**Context detection (run first):**

1. Check if `hacky-hours/` (or ROOT_PATH) exists and has content
2. Check if root-level `01-ideate/`, `02-design/`, etc. exist (old layout)
3. Check `CLAUDE.md` for a `<!-- hacky-hours: vX.Y.Z -->` version marker

Then route to the appropriate flow:

---

### Flow A: New codebase (no hacky-hours/ yet)

**Step 1: Read the codebase**

Gather context from: README.md, package manifests (package.json, pyproject.toml, Cargo.toml, go.mod), directory structure, existing docs, database/schema files, auth-related files, environment variable references, recent git log (`git log --oneline -20`), open TODOs.

**Step 2: Infer artifact stubs**

Draft stubs for:
- **PRODUCT_OVERVIEW.md** — infer 5Ws from README; mark Constraints & Values as "needs input"
- **ARCHITECTURE-deep.md** + **ARCHITECTURE-summary.md** (v3.0.0 two-tier pattern, deep first) — infer the deep dive from directory structure and package manifest, then generate the summary as a faithful condensation. Read `${CLAUDE_SKILL_DIR}/templates/design/README.md` first to confirm the workflow (deep is source of truth; summary is derivative).
- **SECURITY_PRIVACY-summary.md** + **SECURITY_PRIVACY-deep.md** — infer from auth files and env vars; leave threat model blank
- **BACKLOG.md** — seed from TODO/FIXME comments, README "coming soon" language, recent WIP commits

**Step 3: Clarifying questions**

Always ask:
1. "What's the most important thing a new team member should know that isn't obvious from the code?"
2. "Is this open source or closed source? Do you plan to charge for it?"
3. "What does a user do on day one?"
4. "What are the most fragile parts of the codebase right now?"
5. "What's the next thing you were planning to build?"

**Step 4: Show and confirm before writing**

Present a summary of all files to be created. Note: if the project already has a CHANGELOG.md, create `04-build/CHANGELOG.md` as a symlink to it (compute the relative path). Ask for confirmation.

**Step 5: Hand off to iterate**

After writing: "Your framework artifacts are ready. They're a starting point — review each one, especially LICENSING.md, ACCESSIBILITY.md, and the Constraints & Values section. When ready, run `/hacky-hours step 5` to triage what to build next."

---

### Flow B: Old layout (root-level framework folders)

**Step 1: Survey root**

Look for: `01-ideate/`, `02-design/`, `03-roadmap/`, `04-build/`, `archive/`, `.claudeignore`

Report exactly what you find and what you plan to move. Ask to confirm.

**Step 2: Execute migration**

```bash
mkdir -p hacky-hours
for dir in 01-ideate 02-design 03-roadmap 04-build archive; do
  if [ -d "$dir" ]; then
    git mv "$dir" hacky-hours/
  fi
done
```

If `git mv` fails, fall back to plain `mv` and note that history won't be preserved.

**Step 3: Update .claudeignore and CLAUDE.md**

Show before/after diff for path updates. Confirm before writing.

Common updates: `archive/` → `hacky-hours/archive/`, `CHANGELOG.md` → `hacky-hours/04-build/CHANGELOG.md`, `01-ideate/IDEATION.md` → `hacky-hours/01-ideate/IDEATION.md`

**Step 4: Check for GitHub Action**

If `.github/workflows/hacky-hours-sync.yml` exists, read it and flag lines that need updating. Do not edit automatically — show exactly what to change.

**Step 5: Report and commit**

Summarize what was moved and updated. Show exact commit commands — don't run automatically:

```bash
git add .claudeignore CLAUDE.md
git commit -m "chore: migrate hacky-hours artifacts to hacky-hours/ subfolder"
```

---

### Flow C: Existing project (gap detection and fill)

**Step 1: Determine versions**

Read current command version from the SKILL.md frontmatter description. Check `CLAUDE.md` for `<!-- hacky-hours: vX.Y.Z -->` marker. Report the gap.

**Step 2: Compare scaffold**

| Item | Version introduced |
|------|-------------------|
| `learn/` folder | v1.8.0 |
| `feedback/` folder | v1.8.0 |
| `02-design/TESTING.md` | v1.8.0 |
| `.claudeignore` entry for `hacky-hours/learn/` | v1.8.0 |
| `CLAUDE.md` voice section | v1.7.0 |
| Updated command references (step/review/update/tools) | v2.0.0 |
| `CLAUDE.md` uses `review 1` / `update 1` instead of `audit` / `sync` | v2.0.0 |
| Boilerplate migration in Flow C | v2.1.0 |
| Two-tier design templates (`<DOC>-summary.md` + `<DOC>-deep.md`) | v3.0.0 |

**Step 2b: Scan for stale boilerplate**

Scan all files under `hacky-hours/` (and `.claudeignore`, `CLAUDE.md` at project root) for framework-authored patterns that changed across versions. Do not modify files — collect findings only.

**Level language (introduced: v2.0.0 renamed "Levels" to "Steps"):**

| Old pattern | New pattern |
|-------------|-------------|
| `Level 1 — Ideate` | `Step 1 — Ideation` |
| `Level 2 — Design` | `Step 2 — Design` |
| `Level 3 — Roadmap` | `Step 3 — Roadmap` |
| `Level 4 — Build` | `Step 4 — Build` |

**Old command names (introduced: v2.0.0 redesigned the command surface):**

| Old command | New command |
|-------------|-------------|
| `/hacky-hours audit` | `review 1` |
| `/hacky-hours optimize` | `review 2` |
| `/hacky-hours pivot` | `review 3` |
| `/hacky-hours sync --issues` | `update 2` |
| `/hacky-hours sync` | `update 1` |
| `/hacky-hours upgrade` | `tools upgrade` |
| `/hacky-hours mode` | `tools mode` |
| `/hacky-hours iterate` | `step 5` |
| `/hacky-hours dry-run` | `step 0` |
| `/hacky-hours onboard` | `learn 2` |
| `/hacky-hours link` | *(removed — flag for manual review, do not auto-replace)* |

Report each finding as: file path, line number, old text, suggested replacement. Group by file.

**Step 3: Present gap list and confirm**

Show two sections:

1. **Scaffold gaps** — missing folders, files, or CLAUDE.md sections (from Step 2)
2. **Stale boilerplate** — framework-authored patterns that need updating (from Step 2b)

For each item, show what version introduced the change. Ask the user to confirm before writing anything. They may confirm all, some, or none.

**Step 4: Apply confirmed changes**

Apply scaffold changes first, then boilerplate fixes:

- Scaffold: create missing folders, create missing doc stubs, add missing `.claudeignore` entries, update CLAUDE.md sections
- Boilerplate: for each confirmed boilerplate finding, apply the replacement in-place. For `/hacky-hours link` findings: do not replace — report the location and ask the user to decide what to do

**Step 5: Write version marker**

Add or update at the end of `CLAUDE.md`:

```markdown
<!-- hacky-hours: v3.0.0 -->
```

Report: "Upgrade complete. Your project is now up to date with v3.0.0."
