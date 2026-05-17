# Hacky Hours v4.0.0 — Practical QA Script

**Branch:** `feat/v4.0.0`
**Purpose:** Walk through every v4 capability that's been built in Slices 1, 2, 4, and 5 to verify the work actually behaves as designed. Run this before merging the PR.

---

## Pre-flight

### 0a. Clean state (optional but recommended)

If you want a truly clean test, back up your existing v3 setup first:

```bash
# Backup existing installation (skip if you don't have one)
mv ~/.claude/skills/hacky-hours ~/.claude/skills/hacky-hours-v3-backup 2>/dev/null

# Back up your existing ~/.hacky-hours/ if you have one
mv ~/.hacky-hours ~/.hacky-hours-pre-v4-backup 2>/dev/null
```

Skip this if you'd rather upgrade in place — v4 is designed to be additive.

### 0b. Install v4 from the branch

```bash
HH_BRANCH=feat/v4.0.0 bash /Users/bjamba/code/github/empathetech/hacky-hours-docs/install.sh
```

Expected output:
```
Downloading hacky-hours from empathetech/hacky-hours-docs (feat/v4.0.0)...
Installed at /Users/bjamba/.claude/skills/hacky-hours
Restart Claude Code, then type /hacky-hours in any session.
```

### 0c. Verify install

```bash
head -5 ~/.claude/skills/hacky-hours/SKILL.md
```

Should show `description: Hacky Hours v4.0.0 — ...` and **no** `disable-model-invocation: true` line.

```bash
ls ~/.claude/skills/hacky-hours/tools/
```

Should include: `adopt.md  arbitrate.md  feedback.md  issue.md  meta.md  mode.md  team.md  upgrade.md  v4-first-run.md  walkthrough.md`

```bash
ls ~/.claude/skills/hacky-hours/templates/team/default/agents/
```

Should show 12 agent folders: `accessibility  ai-ml  architect  backend  data  design  frontend  licensing  ops  product  qa  security`

### 0d. Restart Claude Code

**Required.** Skills are loaded at Claude Code startup; the install won't be active until restart. Quit + relaunch (or `Cmd+Q` then reopen).

---

## Test 1 — Slice 1 verification (v4 foundation)

### 1.1 Help message shows v4

In any Claude Code session, run:
```
/hacky-hours help
```

**Expected:** Top of output reads `Hacky Hours framework assistant — v4.0.0-dev`. Lists v4 verbs prominently: `team`, `adopt`, `audit`, `arbitrate`, `feedback`, `issue`, `meta`. Lists v3 verbs as "still supported".

✅ Pass criteria: v4.0.0-dev visible; new verbs visible; v3 verbs still listed.

### 1.2 First-run flow creates global setup

If you backed up `~/.hacky-hours/` (step 0a), it should not exist now.

```
/hacky-hours team
```

**Expected:** First message should be the v4 first-run greeting:
> *"Welcome to Hacky Hours v4.0.0-dev 🛠️🤗 — first time using v4 on this machine..."*

It asks if you're ready, then asks one short audience-profile question (engineer / non-engineer / mixed).

After completion:
```bash
ls ~/.hacky-hours/
```

Should show: `feedback/  sessions/  settings.yml  teams/  version  versions/`

```bash
cat ~/.hacky-hours/version
```

Should print `4.0.0-dev`.

```bash
cat ~/.hacky-hours/settings.yml | head -30
```

Should show the populated settings template with your audience profile filled in.

✅ Pass criteria: ~/.hacky-hours/ skeleton created; settings.yml has user's chosen technical background; version file present.

### 1.3 Stub verbs route correctly

```
/hacky-hours arbitrate
```

**Expected:** Honest deferred-slice message, no fake implementation.

```
/hacky-hours feedback
```
```
/hacky-hours issue
```
```
/hacky-hours meta
```

Each should print its deferred-slice notice.

✅ Pass criteria: each stub verb fires with honest "deferred to later slice" messaging.

### 1.4 Context invocation (best-effort)

In a **brand-new Claude Code chat** (not this conversation), type:
```
I have an idea for a recipe sharing app. Help me build it.
```

**Possibly-expected** (Claude Code's skill auto-invocation is probabilistic):
- Claude matches the `hacky-hours` skill description, invokes it
- Skill prints the three-option invitation (Engage / Sketch first / Skip)

**Acceptable alternative:** Claude responds without invoking the skill (auto-invocation didn't fire). This is a known limitation; verbs are the primary surface.

✅ Pass criteria: invitation pattern fires when invocation succeeds; failure to auto-invoke is not blocking.

---

## Test 2 — Slice 2 verification (default team)

### 2.1 Default team bootstrap

If `~/.hacky-hours/teams/default/` does not yet exist:
```
/hacky-hours team
```

**Expected:** Bootstrap message, then:
```bash
ls ~/.hacky-hours/teams/default/
```

Should show: `agents/  LICENSE  README.md  tier.yml  VERSION  .gitignore  .git/`

```bash
ls ~/.hacky-hours/teams/default/agents/
```

12 agent folders: accessibility, ai-ml, architect, backend, data, design, frontend, licensing, ops, product, qa, security.

```bash
cd ~/.hacky-hours/teams/default/ && git log --oneline
```

Should show: `<sha> Initial team — created by Hacky Hours v4.0.0-dev`

### 2.2 Team roster view

```
/hacky-hours team
```

**Expected:** One-screen roster summary showing all 12 named agents with emoji + hat + tagline. Lists subcommands at the bottom.

### 2.3 Agent profile view

```
/hacky-hours team show security
```

**Expected:** Renders Alex Davies's profile — frontmatter as header (name, pronouns, hats, tagline, specialties), then Background + How I work + What I produce sections.

Try a few more:
```
/hacky-hours team show product
/hacky-hours team show ai-ml
/hacky-hours team show accessibility
```

### 2.4 Agent system prompt view

```
/hacky-hours team show security --prompt
```

**Expected:** Full system prompt for Alex (the security agent), including discipline scope, audience adaptation rules, owned artifacts, when-to-speak-up, deferral rules, and voice baseline.

### 2.5 Team list

```
/hacky-hours team list
```

**Expected:** Lists `default` (the only team) with tier, agent count, creation date.

### 2.6 Team help

```
/hacky-hours team help
```

**Expected:** Subcommand list with descriptions, plus a "Coming in later slices" section.

✅ Pass criteria all of 2.x: default team exists with 12 agents, all profile/system-prompt views render, list and help work.

---

## Test 3 — Slice 4 verification (adopt)

For this test, use a small throwaway repo first. Create one:

```bash
mkdir -p /tmp/v4-adopt-test
cd /tmp/v4-adopt-test
git init
mkdir src
cat > src/main.py <<'EOF'
import os
DB_PASSWORD = "hunter2"  # TODO: move to env
def main():
    print(f"Connecting with password {DB_PASSWORD}")
if __name__ == "__main__":
    main()
EOF
cat > README.md <<'EOF'
# Test App
A small thing for testing v4 adoption.
EOF
git add . && git commit -m "Initial test fixture"
```

### 3.1 Adopt flow

In Claude Code, cd to that test repo (or open it as the workspace), then run:

```
/hacky-hours adopt
```

**Expected:**
1. Pre-flight passes (global setup + default team exist from earlier tests)
2. Orientation: 4 questions (what / tier / voice / denylist). Should detect this is a small/throwaway-feeling repo and recommend Tier 1.
3. Team binding: confirms `default` team
4. Role fan-out (this is the slow part — 12 agents reading the codebase). May take a few minutes.
5. Consolidated adoption assessment written to `hacky-hours/adoption-assessment-<date>.md`
6. Conductor review prompt
7. After confirmation: v4 baseline artifacts created

### 3.2 Verify generated artifacts

```bash
ls /tmp/v4-adopt-test/
```

Should now have: `AGENTS.md  CLAUDE.md  hacky-hours/  README.md  src/  .git/  .gitignore`

```bash
ls /tmp/v4-adopt-test/hacky-hours/
```

Should have: `NARRATIVE.md  STATE.md  HANDOFFS.yml  VOICE.md  adoption-assessment-<date>.md  .hacky-hours-denylist  .hacky-hours-denylist.local`

### 3.3 Verify CLAUDE.md is v4-shape

```bash
cat /tmp/v4-adopt-test/CLAUDE.md
```

Should contain the four labeled sections: Project Tier, Active Team, Voice & Style, Role-Aware Guardrails. The Guardrails table should have an entry from Security about the hardcoded `DB_PASSWORD` (which is a P0 finding the security agent should have caught).

### 3.4 Verify AGENTS.md is the roster index

```bash
cat /tmp/v4-adopt-test/AGENTS.md
```

Should show the 12-agent roster with confirmed involvement levels per the conductor's choices.

### 3.5 Verify NARRATIVE.md is a paragraph

```bash
cat /tmp/v4-adopt-test/hacky-hours/NARRATIVE.md
```

Should be 1-2 paragraphs describing the project + last action (adoption complete) + next likely action.

### 3.6 Verify adoption-assessment captures Security findings

```bash
grep -A 20 "Security" /tmp/v4-adopt-test/hacky-hours/adoption-assessment-*.md
```

Should show the Security agent flagging the committed `DB_PASSWORD = "hunter2"` as a P0 finding with file:line reference.

✅ Pass criteria all of 3.x: adopt completes end-to-end on a fresh repo; all v4 baseline files present; security finding caught; CLAUDE.md has v4 schema; AGENTS.md has 12-row roster.

---

## Test 4 — Slice 5 verification (audit)

Continuing in the same `/tmp/v4-adopt-test` repo (already adopted):

### 4.1 Audit flow

```
/hacky-hours audit
```

**Expected:**
1. Three-lane fan-out:
   - Lane A: Security, A11y, Ops, QA, Architect read the codebase
   - Lane B: Context-free Claude reads docs (`hacky-hours/02-design/` or equivalent)
   - Lane C: Cross-reference integrity check
2. Consolidation
3. Report written to `hacky-hours/audits/<date>.md`

### 4.2 Verify scorecard

```bash
cat /tmp/v4-adopt-test/hacky-hours/audits/*.md | head -30
```

Should show:
- Scorecard table with traffic lights (🟢/🟡/🔴) and 0-10 scores per dimension
- Aggregate row with computed mean
- At-a-glance section with P0/P1/P2 counts

### 4.3 Verify Lane B doc-audit ran

In the audit report, find the "Lane B — Doc audit (context-free reader)" section. Should contain the structured 6-question response from a stranger Claude (onboarding signal, comprehension gaps, voice consistency, cross-reference clarity, decision visibility, first fix).

### 4.4 Verify audit→CLAUDE.md threading

Audit report should include a "Recommended actions" section with a table of new guardrails to add to CLAUDE.md, owning role, and suggested enforcement mechanism — derived from the P0 findings.

✅ Pass criteria all of 4.x: audit produces scorecarded report with all three lanes visible.

---

## Test 5 — The dogfood test (Slice 6)

The real proof: run v4 on the framework's own repo.

### 5.1 Move to hacky-hours-docs

```bash
cd /Users/bjamba/code/github/empathetech/hacky-hours-docs
```

In Claude Code, open this repo as the workspace.

### 5.2 Adopt the framework on itself

```
/hacky-hours adopt
```

**Expected:**
- Pre-flight detects existing v3-shape `hacky-hours/` folder → handles as v3→v4 migration
- Orientation should auto-detect this is a Tier 2 or 3 project (real users, framework)
- Role fan-out across 12 roles
- Generates v4 artifacts that augment (don't replace) the existing v3 ones
- Adoption assessment file created
- The team's first impressions of the framework itself become visible

### 5.3 Audit the framework on itself

```
/hacky-hours audit
```

**Expected:** Full scorecard on hacky-hours-docs. The doc-audit Lane B is especially interesting — does a stranger Claude understand what Hacky Hours is from reading only the docs?

### 5.4 Review the dogfood output

Read the generated assessment + audit. Honest questions:
- Did the team correctly characterize what hacky-hours is?
- Did Security flag anything real?
- Did the doc-audit lane judge the docs as team-grade?
- Did A11y flag the README's lack of screen-reader-friendly markup?
- Did the audit scorecard match how you (the conductor) would have scored?

This is the bet test — if v4 can't audit hacky-hours sensibly, the thesis isn't yet delivered.

✅ Pass criteria: adopt + audit complete on hacky-hours-docs without breaking the existing v3 content; outputs feel intellectually honest about the framework's state.

---

---

## Test 6 — Slice 7 verification (improvement loop)

### 6.1 Capture feedback

```
/hacky-hours feedback tool "audit asked me to confirm fan-out twice when once would have been enough"
```

**Expected:** Captures to `~/.hacky-hours/feedback/<date>-tool-<slug>.md`. Short acknowledgment, no over-explaining.

```bash
ls ~/.hacky-hours/feedback/
cat ~/.hacky-hours/feedback/<date>-tool-*.md
```

Should show the structured note with frontmatter (kind, target, captured datetime, etc.).

### 6.2 Try the three kinds

```
/hacky-hours feedback role "Alex over-flagged a Tier 1 finding as P0 when P2 was appropriate"
/hacky-hours feedback seam "After audit, the P0 findings didn't get queued into BACKLOG.md automatically"
```

Each should create its own note with appropriate `kind:` frontmatter.

### 6.3 Submit one upstream (opt-in)

```
/hacky-hours issue --from-recent
```

**Expected:**
- Lists recent feedback files, lets you pick one
- Composes an issue body
- Shows it for review
- Four-option permission gate: `yes` / `edit` / `save draft` / `cancel`
- **Don't submit during QA** unless you want to send real feedback to empathetech. Pick `cancel` or `save draft`.

✅ Pass criteria: feedback captures locally, issue verb gates submission behind explicit yes, no auto-upload.

### 6.4 Meta clustering (requires accumulated feedback)

```
/hacky-hours meta
```

**Expected with 3+ feedback items accumulated:** clusters by kind/target, proposes diffs against framework source files, presents each cluster with apply/submit/skip/edit options.

**Expected with too few items:** notice that you need more feedback for meaningful patterns.

✅ Pass criteria: meta reads the feedback corpus and either clusters meaningfully or honestly says it needs more signal.

---

## Test 7 — Slice 8 verification (team update + arbitrate)

### 7.1 Team update with no pending

```
/hacky-hours team update
```

**Expected** (if no pending session changes): *"Nothing to promote. Agents are unchanged from the team repo."*

### 7.2 Trigger a pending change (manual)

Since session-pending capture wiring is preliminary in v4.0.0-dev, manually stage a pending change:

```bash
mkdir -p ~/.hacky-hours/sessions/test-session-001/pending/
cat > ~/.hacky-hours/sessions/test-session-001/pending/security.md <<'EOF'
[behavior feedback] Be terser when flagging at Tier 1 — single-line summary plus link to detail, not multi-paragraph explanation.

Captured during a session where Alex's audit output was overly verbose for a personal weekend project.
EOF
```

Then:
```
/hacky-hours team update
```

**Expected:** Walks through the staged change for Alex (security), offers accept/edit/reject/defer. Pick accept.

After accept:
```bash
cd ~/.hacky-hours/teams/default/ && git log --oneline -3
```

Should show a new commit `Update 1 agent(s) — <date>` with Alex's feedback applied.

### 7.3 Arbitrate (any mode)

```
/hacky-hours arbitrate decide "should we use strict CSP from launch or relax it for the MVP"
```

**Expected:** 
- Asks which roles are in disagreement (security + FE typically)
- Each role gives compressed position
- Side-by-side presentation
- Asks the conductor to decide
- Writes an ADR to `hacky-hours/02-design/decisions/<date>-csp-strictness.md`

Try `resolve` and `watch` modes too (warning: `watch` is the most expensive).

✅ Pass criteria: team update commits pending changes; arbitrate produces an ADR regardless of mode chosen.

---

## Test 8 — Slice 9 verification (static team site)

### 8.1 Build the team site

```
/hacky-hours team site build
```

(Or just `/hacky-hours team site`.)

**Expected:**
- Copies `templates/team-site/` into `~/.hacky-hours/teams/default/site/` (first run only)
- Runs `python3 generate.py`
- Output: `~/.hacky-hours/teams/default/docs/` with `index.html`, `agents/<id>.html` for each agent, `style.css`

### 8.2 Browse via file://

```bash
open ~/.hacky-hours/teams/default/docs/index.html
```

(On Linux: `xdg-open`; or just paste the path into your browser.)

**Expected:** clean team-roster page with all 12 agents as cards (emoji avatar, name, role, tagline). Click any card → navigates to that agent's profile page (background, how-I-work, what-I-produce content rendered as HTML).

### 8.3 Local serve

```
/hacky-hours team site serve
```

**Expected:** prints the command to start a local server (`cd ... && python3 -m http.server 8000`). Run that command yourself in a separate terminal, then visit http://localhost:8000.

### 8.4 Publish (don't actually publish during QA)

```
/hacky-hours team site publish
```

**Expected:** walks through GitHub Pages setup with a clear privacy gate. Don't proceed unless you want to actually publish — pick "don't publish" or cancel.

✅ Pass criteria: site builds successfully, file:// rendering works (no broken links, no missing CSS), serve command is given correctly, publish guidance is privacy-aware.

---

## Test 9 — Slice 10 verification (export verb)

In `/tmp/v4-adopt-test` (the adopted test project):

### 9.1 Markdown bundle

```
/hacky-hours export markdown-bundle
```

**Expected:**
- Lists docs to include, asks for confirmation
- Generates `hacky-hours/exports/<date>-bundle.md`
- Confirmation print with file size, line count

```bash
head -30 /tmp/v4-adopt-test/hacky-hours/exports/<date>-bundle.md
```

Should show a clean TOC + each included doc concatenated, with headings demoted appropriately.

### 9.2 Paste-test (optional)

Copy the bundle's content into a Notion page, Obsidian note, or GitHub Discussion. Verify it renders cleanly — headings hierarchy intact, links work, code blocks formatted.

### 9.3 HTML bundle deferral notice

```
/hacky-hours export html-bundle
```

**Expected:** honest deferral notice with MkDocs setup recommendation.

✅ Pass criteria: markdown-bundle generates clean concatenated docs, deferral notices are honest about what's missing.

---

## Test 10 — Slice 11 verification (team chat, tiered)

The orchestra goes from invisible to audible. Verify each tier behaves correctly, the toggle command works, the "no filler" rule holds, and `off` truly restores pre-v4 behavior.

### 10.1 Inspect the setting

```bash
grep team_chat ~/.hacky-hours/settings.yml
```

**Expected:** a `team_chat:` line with value `off`, `minimal`, or `full`. If absent, the first-run template should have added it — note as a regression if missing for a fresh install.

### 10.2 Read current mode (no argument)

```
/hacky-hours team chat
```

**Expected:** prints current mode + the three options + how to switch. No file writes.

### 10.3 Switch to `off`

```
/hacky-hours team chat off
```

**Expected:** confirmation line; `~/.hacky-hours/settings.yml` updated in place (other fields and comments preserved); no other output.

### 10.4 Run a multi-role verb with `team_chat: off`

```
/hacky-hours audit
```

(Or any multi-role verb on an adopted project.) **Expected:** output reads as a single narrator — no `**Name (Role) [HH:MM]**` headers, no per-role emoji glyphs introducing turns. Matches pre-v4 (Slice 5) audit rendering.

### 10.5 Switch to `minimal`

```
/hacky-hours team chat minimal
```

**Expected:** confirmation; settings updated.

### 10.6 Run a multi-role verb with `team_chat: minimal`

```
/hacky-hours audit
```

**Expected:** speaker attribution appears at meaningful moments only — when a role introduces a concern, when roles disagree, when control hands off. One header per moment, content flows. No turn-by-turn back-and-forth.

✅ Pass criteria: visibly more team presence than `off`, visibly less verbose than `full`. Each attributed moment adds real information.

### 10.7 Switch to `full`

```
/hacky-hours team chat full
```

**Expected:** confirmation **plus** a one-line cost caveat: "Heads up: full mode runs real per-role fan-out and costs meaningfully more tokens..." (no numeric estimate — Slice 11 explicitly defers calibration to v4.1+).

### 10.8 Run a multi-role verb with `team_chat: full`

```
/hacky-hours audit
```

**Expected:** closed-captioned multi-agent dialogue. Each role surfaces in its own voice with the canonical emoji glyph (📊 Product, 🎨 Design, 🏗️ Architect, 🛡️ Security, etc. — see V4_DESIGN.md §5). Hand-offs render as turns. Side chatter visible.

### 10.9 The no-filler audit

Re-read the `full`-mode output from 10.8. **Manually verify** no turn:
- Says only "Got it." / "Sounds good." / "Makes sense."
- Agrees without adding ("I agree with X." with nothing after)
- Restates another role's point in different words
- Manufactures disagreement that doesn't reflect actual reasoning

Any of the above is a Slice 11 regression — the "no tokens for tokens' sake" rule is load-bearing.

### 10.10 Voice distinctness

In the same `full`-mode output, can you tell which role is speaking from the *tone* alone, before reading the speaker tag? If voices feel uniform, the agents aren't using their `profile.md` baselines — flag as a regression.

✅ Pass criteria: three modes behave distinctly; `off` restores pre-v4 behavior verbatim; switching to `full` warns about cost without quoting numbers; the no-filler rule holds; voices are distinguishable.

---

## Cleanup (optional)

If you want to revert after testing:

```bash
# Remove test repo
rm -rf /tmp/v4-adopt-test

# Restore your v3 install (if you backed it up)
rm -rf ~/.claude/skills/hacky-hours
mv ~/.claude/skills/hacky-hours-v3-backup ~/.claude/skills/hacky-hours 2>/dev/null

# Restore your prior ~/.hacky-hours/ if you backed it up
rm -rf ~/.hacky-hours
mv ~/.hacky-hours-pre-v4-backup ~/.hacky-hours 2>/dev/null

# Revert any v4 changes inside hacky-hours-docs/ that adoption made (use git)
cd /Users/bjamba/code/github/empathetech/hacky-hours-docs
git status
git stash  # or git checkout -- <files>
```

---

## Reporting issues

If any test fails, capture:
- Test number
- Command run
- Expected output (from this doc)
- Actual output
- Any error messages

File against `empathetech/hacky-hours-docs` with label `v4-qa`, or just leave inline notes in this file under a new `## QA Run Log` section.

---

## Sign-off

When all nine test suites pass to your satisfaction, the branch is mergeable. Open the PR (or merge directly if you're comfortable). Suggested merge commit message:

```
feat(v4.0.0): orchestra of stakeholder-role agents

Reframes hacky-hours as a competence prosthesis for solo builders.
Engages 12 named role-agents (product, design, architect, FE, BE,
security, ops, QA, a11y, licensing, data, AI/ML) as a persistent
portable team that produces team-grade artifacts. Replaces v3's
"documentation framework" framing.

New verbs: team, adopt, audit, plus deferred stubs for arbitrate,
feedback, issue, meta. v3 verbs preserved for backward compatibility.

See hacky-hours/02-design/V4_DESIGN.md for the full design and
hacky-hours/02-design/V4_QA.md for the test plan that gated this merge.
```
