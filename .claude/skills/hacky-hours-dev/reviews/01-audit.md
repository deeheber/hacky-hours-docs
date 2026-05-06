# Review 1 — Audit

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `review 1` / `review audit`.*

**Context:** Read `02-design/LICENSING.md` to know the expected license. Read `04-build/BACKLOG.md` and `04-build/CHANGELOG.md` under ROOT_PATH. Do not ask the user for this information — read it yourself.

**Purpose:** A read-only scan that tells the user exactly what needs to happen before they can ship. Never modifies any files except the optional scorecard. Safe to run at any time.

Run all phases in order. Collect all findings, then present them together as a single prioritized report.

---

**Phase 1 — Secrets and Sensitive File Scan**

This is the highest-stakes check. Run it first and flag findings loudly.

```bash
git ls-files --others --exclude-standard | grep -E "\\.env$|\\.env\\.|id_rsa|id_ed25519|\\.pem$|\\.key$|\\.p12$|\\.pfx$|secrets\\.|credentials\\."
```

```bash
git diff HEAD | grep -inE "(api_key|secret|password|token|private_key|access_key|auth_token)\s*[=:]"
```

Check whether `.gitignore` covers: `.env`, `.env.*`, `*.pem`, `*.key`, `id_rsa*`, `id_ed25519*`, `node_modules/`, `.DS_Store`

**If anything is found:** display a prominent `⚠️ STOP — review before committing` block. Do not continue to the next-steps list until this is acknowledged.

**If nothing is found:** display `Secrets scan: no obvious issues found` with a caveat that this is a heuristic check.

---

**Phase 2 — Framework Doc Readiness**

- Is `04-build/BACKLOG.md` empty? If not, list remaining tasks
- Does `04-build/CHANGELOG.md` have an entry for the version about to be released?
- **Version string check:** Extract the version from the SKILL.md frontmatter description and compare to the latest CHANGELOG version. If they don't match, flag it.
- Is there a `LICENSE` file in the repo root?

**Design doc scorecard — check each doc under `ROOT_PATH/02-design/`:**

| Doc | Why it matters |
|-----|---------------|
| ARCHITECTURE | Are system components and key decisions documented? |
| DATA_MODEL | Is the data structure documented if the product stores data? |
| USER_JOURNEYS | Are the key user flows mapped out? |
| STYLE_GUIDE | Is the visual language defined if the product has a UI? |
| ACCESSIBILITY | Are accessibility standards and current state documented? |
| MARKET_FIT | Is the target audience and value proposition validated? |
| BUSINESS_LOGIC | Are domain rules and calculations documented? |
| SECURITY_PRIVACY | Is the risk surface and data handling documented? |
| LICENSING | Is the license chosen and dependency compatibility checked? |
| TESTING | Is the test strategy and definition of done documented? |

For docs using the v3.0.0 two-tier pattern: check that both `<DOC>-deep.md` and `<DOC>-summary.md` exist. The deep dive is the source of truth (it's what Step 4 builds from); the summary is a derivative view. Flag any of:
- Deep dive missing or placeholder-only — this is the spec and must be filled in
- Summary missing — should exist as a derivative once the deep dive is signed off
- Summary makes a claim the deep dive doesn't (summary drift) — summary needs to be regenerated from the deep dive
- Summary omits something load-bearing from the deep dive's Key Decisions or Known Constraints — same fix

Report as: `✓ Filled in` / `⚠ Placeholder only` / `✗ Missing — <specific gap>`

---

**Phase 2b — GitHub Issues ↔ BACKLOG Reconciliation**

If `gh` is available and authenticated (`gh auth status`), compare open issues against BACKLOG items:

```bash
gh issue list --state open --limit 100 --json number,title,labels,milestone
```

Report:
- **BACKLOG items with no matching Issue:** flag for visibility
- **Open Issues not in BACKLOG:** flag as potentially untracked work
- **Closed Issues still in BACKLOG:** may be done; flag for removal

If `gh` is not available, skip with a note.

---

**Phase 3 — Git Status in Plain Language**

Run `git status` and translate:
- Uncommitted changes: "You have N files with changes not saved to git yet: [list]"
- Untracked files: "These files exist but git doesn't know about them: [list]. If any are sensitive, do not commit them."
- Unpushed commits: `git log --oneline @{u}..HEAD 2>/dev/null`
- Current branch: note if on `main` or a feature branch
- No remote: warn and point to `git remote add origin <url>`

---

**Phase 4 — Next Steps, Ordered**

Based on Phases 1–3, generate a numbered plain-language to-do list. Order: blockers first, warnings second, suggestions last.

```
[STOP]  .env is not in your .gitignore — add it before doing anything else
        → How: open .gitignore and add a line: .env

[ ]  Commit your framework doc changes
     → How: git add hacky-hours/ CLAUDE.md .claudeignore
            git commit -m "docs: update framework docs for vX.Y.Z"

[ ]  Tag the release
     → How: git tag vX.Y.Z && git push origin vX.Y.Z

[ ]  Publish the release
     → How: run /hacky-hours update 1
```

If everything is clean: "Everything looks good — you're ready to run `/hacky-hours update 1`."

---

**Phase 5 — Save Scorecard (optional)**

Ask: "Would you like to save this audit as a scorecard? It'll be stored in `audits/`."

If yes, write to `ROOT_PATH/audits/YYYY-MM-DD-audit.md`. The format:

```markdown
# Audit Scorecard — YYYY-MM-DD

**Project:** <repo name>
**Branch:** <current branch>
**Commit:** <short SHA>

## Secrets Scan
- **Result:** PASS | FAIL | WARNING
- **Findings:** <list or "None">

## Framework Doc Readiness
- **BACKLOG.md:** Empty (milestone complete) | N tasks remaining
- **CHANGELOG.md:** Entry exists for vX.Y.Z | No entry found
- **Version strings:** Skill vX.Y.Z matches CHANGELOG vX.Y.Z | Mismatch
- **LICENSE:** Present | Missing

## Design Doc Scorecard
| Doc | Status |
|-----|--------|
| ARCHITECTURE | ✓ / ⚠ / ✗ |
...

## GitHub Issues Sync
- **BACKLOG-only items:** N
- **Issue-only items:** N
- **Stale BACKLOG items:** N

## Git Status
- **Uncommitted changes:** N files
- **Untracked files:** N files
- **Unpushed commits:** N commits
- **Branch:** <branch name>

## Next Steps
<copy of Phase 4 ordered list>

---
*Generated by `/hacky-hours review 1` — this is a heuristic check, not a security guarantee.*
```
