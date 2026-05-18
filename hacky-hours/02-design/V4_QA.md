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

## Test 11 — Slice 12 verification (team learning capture)

Closes the v4 thesis loop. Verify the end-to-end persistence chain: multi-role verb → history append + behavior pending → team-update accept → committed agent change → next session sees the updated agent. Plus the audit Lane B saturation guard (issue #6 fix). Plus tools/issue.md label-detect.

### 11.1 Pre-state: confirm sessions is empty and team has only initial commit

```bash
ls ~/.hacky-hours/sessions/ 2>/dev/null
git -C ~/.hacky-hours/teams/default log --oneline
```

**Expected:** sessions/ empty (or contains only `.current-session` from a prior test). Team git log shows only the initial-team commit (or whatever existed before this test).

### 11.2 Run a multi-role verb that fans out — capture history

On the test project from earlier suites (or hacky-hours-docs itself if you're running QA dogfood-style):

```
/hacky-hours audit
```

After the audit's normal Step 4 summary, the new Step 5 (Stash) should run:

- Auto-prints which agents participated (typically: Security, A11y, Ops, QA, Architect).
- Auto-appends one line per participant to their `history.md`. Format: `- <YYYY-MM-DD> · <project-slug> · audit · <summary>`.
- Auto-commits on the team repo with message `history: audit @ <project> @ <date> — <N> agent(s)`.
- Prompts: *"Anything you said during this audit that should change how an agent works in future sessions?"*

**Expected outputs to check:**

```bash
# History was appended
cat ~/.hacky-hours/teams/default/agents/security/history.md | tail
cat ~/.hacky-hours/teams/default/agents/architect/history.md | tail

# Team repo committed
git -C ~/.hacky-hours/teams/default log --oneline
# Should show a new "history: audit @ ..." commit

# Session ID was created
cat ~/.hacky-hours/sessions/.current-session
# Should print a YYYY-MM-DD-HHMM-xxxx string

ls ~/.hacky-hours/sessions/
# Should show .current-session + a <session-id>/ folder
```

✅ Pass criteria: history.md has new lines for each participating agent; team repo has a new commit; sessions/.current-session exists; the contribution summaries are concrete (not generic "Reviewed code") and reference what the role actually flagged.

### 11.3 Behavior feedback prompt — answer with a real correction

When the Stash phase asks for behavior feedback, respond with something like:

```
Security — be terser when flagging Tier 1 findings. Skip the threat-model framing for personal-use tools.
Architect — none
```

**Expected outputs to check:**

```bash
ls ~/.hacky-hours/sessions/<session-id>/pending/
# Should show security.md (NOT architect.md — "none" doesn't stash)

cat ~/.hacky-hours/sessions/<session-id>/pending/security.md
```

**Expected file contents:**

```yaml
---
captured_at: <ISO timestamp>
session_id: <same as .current-session>
project: <project-slug>
verb: audit
kind: behavior_feedback
agent: security
status: pending
---

## Context
<one paragraph: what was happening during the audit>

## Proposed change
<the conductor's words, verbatim or near-verbatim — "be terser when flagging Tier 1 findings. Skip the threat-model framing for personal-use tools.">
```

The footer should print: *"Stashed 1 behavior note(s) for [security]. Appended history to 5 agent(s) (commit <sha>). Promote with `/hacky-hours team update` when ready."*

✅ Pass criteria: pending file present for named agent only, schema matches `references/capture-format.md`, frontmatter complete, conductor's actual words preserved.

### 11.4 Behavior feedback prompt — answer "none"

Run another multi-role verb (e.g., `/hacky-hours arbitrate decide "should we add a new dep?"`). When asked for behavior feedback, answer `none`.

**Expected:** no new pending files written; history still appends; footer prints *"Stashed 0 behavior note(s). Appended history to <N> agent(s) (commit <sha>)."*

✅ Pass criteria: `none` is a valid silent answer; history still fires regardless.

### 11.5 team update promotes the pending change

```
/hacky-hours team update
```

**Expected:** the verb reads the pending entry from 11.3, presents it for accept/edit/reject/defer. Accept it.

```bash
# Check it landed in feedback.md
cat ~/.hacky-hours/teams/default/agents/security/feedback.md
# Should contain the new behavior note

# Check the team repo commit
git -C ~/.hacky-hours/teams/default log --oneline
# Should show a "Update 1 agent(s) — <date>" commit on top of the earlier history: commits

# Pending file moved to resolved
ls ~/.hacky-hours/sessions/<session-id>/resolved/
# Should show security.md
ls ~/.hacky-hours/sessions/<session-id>/pending/
# Should be empty (or only contain entries from other agents)
```

✅ Pass criteria: behavior note appended to security's `feedback.md`, team repo committed, pending file moved to resolved.

### 11.6 Next session uses the updated agent

Open a new Claude Code session (or simulate by waiting >4h or by deleting `.current-session` — this resets session ID; the team repo update persists regardless). Run another audit:

```
/hacky-hours audit
```

**Expected:** Security's findings should reflect the new behavior note. If you told Security to "be terser at Tier 1," Tier 1 findings should look noticeably more compact than previous audits on the same project. The persistence chain is real if you can see the agent applying yesterday's correction today.

✅ Pass criteria: visible behavior change in the agent's output that traces back to the behavior note from 11.3. The orchestra learned.

### 11.7 Session ID staleness regenerates correctly

```bash
# Manually backdate the marker file to >4 hours ago
touch -t $(date -v-5H +%Y%m%d%H%M) ~/.hacky-hours/sessions/.current-session

# Run a multi-role verb
/hacky-hours audit
```

**Expected:** during the verb's Stash phase, a *new* session ID is generated (different from the one written before the touch). Old session folder still exists with its resolved entries; new session folder is created with today's pending entries.

✅ Pass criteria: stale marker triggers regeneration; old session state preserved.

### 11.8 Audit Lane B saturation guard fires (issue #6 fix)

On a project with at least 2 prior audits in `hacky-hours/audits/` whose actionable critiques have been addressed (or simulate with a script that pre-seeds 3 audit files), run:

```
/hacky-hours audit
```

**Expected:** Lane B's traffic-light score and first 5 question answers pass through unmodified. The "First fix" item gets either:
- Passed through if the recommendation is genuinely novel and not already in the docs, OR
- **Replaced with the saturation flag note** if the conductor verifies (via Lane C cross-ref or direct Read) that the recommendation is already present in the docs the stranger just read.

In the saturated case, the Documentation dimension on the scorecard gets `· saturated (N)` appended, and a counter file `hacky-hours/audits/.lane-b-saturation` records the streak. The "At-a-glance" section frames saturation as a positive graduation indicator.

✅ Pass criteria: no more false-negative "first fix" recommendations like "add an anchor callout to README opening" when the README already has one. Saturation is named as a graduation signal, not a stuck 🟡.

### 11.9 tools/issue.md label-detect (issue #6 tail bug)

```
/hacky-hours issue
# (interactive flow — compose a minimal issue, confirm submission)
```

**Expected:** before `gh issue create` runs, the verb calls `gh label list --repo empathetech/hacky-hours-docs` to discover existing labels. If `user-feedback` and `v4` don't exist upstream, the verb:
- Omits `--label` entirely from the `gh issue create` call (so it doesn't fail wholesale).
- Adds a one-line note to the issue body footer explaining which labels were requested but absent.
- After successful submission, the confirmation line mentions which labels (if any) were applied vs. omitted.

✅ Pass criteria: a missing-label upstream state does not block submission; the issue body footer surfaces the gap for maintainers to act on.

### 11.10 Team site reflects accumulated history

After running 11.2–11.6, regenerate the team site:

```
/hacky-hours team site build
# Open the generated HTML
open ~/.hacky-hours/teams/default/docs/index.html
```

**Expected (v4.0.0-dev):** the static-site generator reads `profile.md` (which doesn't reference `history.md` directly), so the visible site is unchanged structurally. **However**, manually inspecting any agent's `history.md` file via the site's "view source" link (or directly in the team repo) shows the accumulated entries.

Surfacing history on the rendered site is a v4.1+ candidate (per V4_DESIGN.md §4.21 deferral list). Slice 12 ships the persistence; the site's history view is a follow-on.

✅ Pass criteria: site still builds and renders; history is *in the data* even if not yet *in the rendered view*.

### 11.11 Backfill dry-run from this repo's CHANGELOG

The thesis-completion test: this repo (hacky-hours-docs) has 30+ CHANGELOG entries spanning v0.x → v4. Forward-capture caught none of them. Backfill should populate per-agent history retroactively.

```
cd /path/to/hacky-hours-docs
/hacky-hours team backfill --dry-run
```

**Expected:**
- Pre-flight surfaces: source (CHANGELOG.md preferred), entry count (30+), target team (default), agents in scope (12).
- Dry-run skips per-agent interactivity. Prints proposed entries grouped by agent.
- Each agent shows a sensible number of proposed entries:
  - **Maya (Product):** ~12 entries (every milestone version)
  - **Priya (Architect):** ~10 entries (ARCHITECTURE updates, ADRs, structural changes)
  - **Alex (Security):** ~5 entries (SECURITY_PRIVACY updates, audit findings)
  - **Lena (A11y):** ~3 entries (ACCESSIBILITY updates, v1.6.0 audit)
  - **Diego (Licensing):** ~2 entries (LICENSING.md, CLA decision)
  - **Emma (QA):** ~3 entries (TESTING.md, V4_QA.md, pre-release checklist)
  - Others as the classification table allows.
- Each line follows the format `- <date> · hacky-hours-docs · <verb> (backfilled, CHANGELOG#<anchor>) · <summary>`.
- No team-repo writes occur (dry-run).

✅ Pass criteria: classification produces sensible per-agent breakdowns; no agent is wildly miscounted; summaries reference what the CHANGELOG entry actually says (not invented detail); zero commits land.

### 11.12 Backfill real run, per-agent batch review, commits land

```
/hacky-hours team backfill
```

**Expected flow:**
- Same pre-flight + summary as 11.11, but proceeds interactively.
- Per agent (in some sensible order — by entry count desc is reasonable), presents the batch with `a / s / e / r / d` options.
- For agent 1 (Maya): answer `a` (accept all). Verify a commit lands on the team repo: `git -C ~/.hacky-hours/teams/default log --oneline | head` shows `history: backfill @ hacky-hours-docs — product (12 entries from changelog)` or similar.
- For agent 2 (Priya): answer `s`, select a subset (e.g., `1, 3-5, 8`). Verify only those entries land in priya's history.md.
- For agent 3 (Alex): answer `e`, edit one summary. Verify the edited form lands.
- For agent 4 (Felix or Yuki): answer `r` (reject all). Verify no entries land for that agent and no commit is created.
- For agent 5 (Sam): answer `d` (defer). Verify `~/.hacky-hours/sessions/<session-id>/backfill-pending/sam.md` exists.
- After all 12 agents resolved: footer summary prints per-agent disposition + commits added count.

```bash
# Verify per-agent commits exist
git -C ~/.hacky-hours/teams/default log --oneline | grep "history: backfill"
# Should show separate commits per accepting agent

# Verify a specific agent's history.md
cat ~/.hacky-hours/teams/default/agents/product/history.md
# Should have the 12 entries chronologically, all annotated `(backfilled, CHANGELOG#...)`

# Verify backfilled-vs-forward-captured distinguishability
grep "(backfilled," ~/.hacky-hours/teams/default/agents/product/history.md | wc -l
# Should match the accepted count for that agent
```

**Re-invocation safety:** run `/hacky-hours team backfill` a second time on the same repo:

**Expected:** entries already present (with their `(backfilled, ...)` annotations matched against proposed anchors) are skipped. Conductor sees: *"<count> entries already backfilled for <agent>; <count> new entries to consider."* If everything is already there: *"No new backfill candidates — already retroactively populated."*

✅ Pass criteria: per-agent batches behave correctly under each disposition (accept/select/edit/reject/defer); per-agent commits land on team repo; annotations distinguish backfilled from future forward-captured entries; re-invocation is idempotent.

---

## Test 12 — Slice 13 verification (agent representation: metrics + team site + résumé + reflection)

The thesis-visibility test. Slice 12 closed the persistence loop in the data; Slice 13 closes it in the visible layer. Verify the four coordinated pieces work together: metrics refresh, team-site rendering, résumé generation, and reflection. Assumes Slice 12 has been run and at least one team has history (run Test 11 first, or backfill this repo).

### 12.1 Metrics block springs into existence after first multi-role verb

Pre-state: a fresh agent's `profile.md` has no `metrics:` block. (Default team templates ship without one; the block lands on first refresh.)

```bash
# Inspect pre-state
grep -A1 "^metrics:" ~/.hacky-hours/teams/default/agents/security/profile.md
# Should print nothing (no metrics block yet) OR an existing one from prior tests
```

Run a multi-role verb that engages Security:

```
/hacky-hours audit
```

After the audit's Step 5 (Stash), inspect:

```bash
grep -A12 "^metrics:" ~/.hacky-hours/teams/default/agents/security/profile.md
```

**Expected:** the `metrics:` block now exists with at least `level`, `history_entries`, `projects`, `verbs_run`, `last_active`, `metrics_refreshed` populated. Values reflect the audit run (e.g., `history_entries: 1`, `verbs_run: 1`, `projects: [hacky-hours-docs]`, `last_active: <today>`, `level: 1`).

```bash
# Verify the commit bundles history.md + profile.md
git -C ~/.hacky-hours/teams/default log -1 --stat
# Should show both agents/security/history.md AND agents/security/profile.md in the same commit
```

✅ Pass criteria: metrics block is created/refreshed in same commit as history append; level + counts reflect actual activity.

### 12.2 Level derivation handles base table + breadth bumps

Pre-condition: backfill this repo so multiple agents have varying history counts and verb-type variety.

```
/hacky-hours team backfill
# accept all batches
```

Inspect a few agents' levels:

```bash
for agent in product architect security accessibility data; do
  echo "=== $agent ==="
  grep -A2 "^metrics:" ~/.hacky-hours/teams/default/agents/$agent/profile.md | grep -E "level|history_entries"
done
```

**Expected:** levels track the base table:
- agents with 0 entries → level 0
- 1–5 entries → level 1
- 6–15 → level 2
- 16–30 → level 3
- 31–60 → level 4
- 61+ → level 5

Plus breadth bumps:
- +1 if 3+ projects (probably won't fire on this repo; only 1 project)
- +1 if 5+ verb types (likely fires for product and architect)

Maya (product) and Priya (architect) likely hit level 3 from raw count with a +1 bump from verb-type variety → level 4. Verify the math matches the table.

✅ Pass criteria: levels are honest signal — high count alone doesn't max out levels without breadth; agents with no work show level 0.

### 12.3 Team site renders metrics badges on index cards

```
/hacky-hours team site build
open ~/.hacky-hours/teams/default/docs/index.html
```

**Expected:** Index page shows agent cards. Each card with `history_entries > 0` displays a metrics badge below the body: `lvl <N> · <count> contribution(s) · <K> project(s)`. Agents with zero history get no badge (clean card). Level number is highlighted with the accent color.

Inspect HTML directly:

```bash
grep -c "metrics-badge" ~/.hacky-hours/teams/default/docs/index.html
# Should match the count of agents with non-zero history
```

✅ Pass criteria: badges render where appropriate; absent where appropriate; visually distinct from existing card content.

### 12.4 Profile page renders Recent track record + Lessons applied

Open any agent with history:

```bash
open ~/.hacky-hours/teams/default/docs/agents/architect.html
```

**Expected:**
- Header has metadata line ending with "Level <N> · <count> contributions"
- After the existing Bio (Background / How I work / What I produce), a new "Recent track record" section appears with a timeline of up to 10 entries (newest first). Each entry shows date · project · verb · summary.
- After Track record, a "Lessons applied" section shows up to 5 durable feedback notes (omitted if `feedback.md` is empty or only contains the template placeholder).
- Backfilled entries' `(backfilled, ...)` annotation is stripped from the rendered verb name (display-clean; data still has it).

```bash
grep -c "Recent track record" ~/.hacky-hours/teams/default/docs/agents/architect.html
# Should be 1
grep -c "history-entry" ~/.hacky-hours/teams/default/docs/agents/architect.html
# Should match min(history_entries, 10) for that agent
```

✅ Pass criteria: timeline renders chronologically; entries are readable; lessons render only when present; CSS is mobile-responsive (resize to <600px and verify single-column layout).

### 12.5 team resume generates fact-derived synthetic résumé

```
/hacky-hours team resume architect
```

**Expected:** writes `~/.hacky-hours/teams/default/agents/architect/resume.md`. Footer prints line count + level + contribution count.

```bash
cat ~/.hacky-hours/teams/default/agents/architect/resume.md
```

Verify structure:
- Frontmatter: `agent`, `generated`, `generator: team-resume v4.0.0`, `style: standard`, `source.history_entries`, `source.feedback_entries`
- `# <Name> <avatar> <Role>` header
- `> <tagline>` quote
- `**Level <N>** · <count> contributions · <K> projects · joined <date>`
- `## Summary` (2-3 sentences, no padding)
- `## Skills` (aggregated by verb-type, evidence counts cited)
- `## Experience` grouped by project, chronological within project, newest-first
- `## Recent learnings` (paraphrased from feedback; omitted if feedback empty)
- `## Profile` (verbatim bio sections)
- Footer line

✅ Pass criteria: every skill claim has a count traceable to history.md; no invented experience; honest about thin work (if architect has only 3 entries, skills section is 1-2 lines, not padded to 8).

### 12.6 team resume --all + thin-work honesty

```
/hacky-hours team resume --all
```

**Expected:** writes resume.md for every agent. Per-agent status lines print. Agents with zero history get a **minimal** résumé (header + Summary + Profile only — no Skills/Experience/Learnings padding). Agents with history get standard structure.

```bash
# Verify zero-history agent gets minimal output
wc -l ~/.hacky-hours/teams/default/agents/data/resume.md   # likely minimal — data has no FE/BE work in this repo
wc -l ~/.hacky-hours/teams/default/agents/product/resume.md # likely fuller — product touches every milestone
```

The first should be noticeably shorter than the second. Honest output reflects actual work.

✅ Pass criteria: --all completes for all 12 agents; minimal vs. standard structure matches history depth; no résumé claims experience the agent doesn't have.

### 12.7 Team site links to résumés and renders standalone pages

```
/hacky-hours team site build
```

**Expected:** for every agent with a `resume.md`, a `docs/agents/<id>-resume.html` is generated. Profile pages show a "📄 Read full résumé →" link below the specialties list.

```bash
open ~/.hacky-hours/teams/default/docs/agents/architect-resume.html
```

**Expected on the résumé page:**
- "← Profile" back-link in the header (navigates back to the profile page, not the team index)
- Rendered markdown of resume.md as a single-column page
- Distinct styling (blockquote accents, larger h1)

✅ Pass criteria: résumé pages render; back-link goes to profile; cross-link from profile to résumé is present and works.

### 12.8 team reflect — silent Track record refresh + prose proposals + self-observations

Pre-condition: agent has at least 5 history entries (run Test 12.2 backfill first).

```
/hacky-hours team reflect architect
```

**Expected interactive flow:**
- The verb reads `history.md`, `feedback.md`, current `profile.md`
- Phase 1: silently refreshes a `## Track record` section in profile.md Bio (auto-append/replace, no review). One paragraph per project, third-person past-tense.

```bash
# After running reflect — check Track record section is present
grep -A20 "^## Track record" ~/.hacky-hours/teams/default/agents/architect/profile.md
```

- Phase 2: presents proposed prose updates (Background / How I work / What I produce) — only sections where history/feedback justifies revision. For each, writes a `kind: prose_update` pending entry. Verify:

```bash
ls ~/.hacky-hours/sessions/<session-id>/pending/
# Should show one or more architect.md pending entries with kind: prose_update
cat ~/.hacky-hours/sessions/<session-id>/pending/architect.md
# Should have frontmatter: kind: prose_update, target_section: <background|how_i_work|what_i_produce>
```

- Phase 3: prints self-observations (strengths + gaps). Conductor names items to stash as behavior feedback. Verify those land as separate `kind: behavior_feedback` pending entries.

```bash
# Commit log on team repo
git -C ~/.hacky-hours/teams/default log --oneline | head -3
# Should show "reflect: architect @ <date> — track record + metrics refreshed" (1 commit, the silent refresh)
```

Promote a proposed prose update:

```
/hacky-hours team update
# Accept one of the prose_update entries
```

**Expected:** the relevant section in `profile.md` Bio (Background / How I work / What I produce) is replaced with the proposed prose; team repo commits the change.

✅ Pass criteria: Track record refreshes silently (no review interruption); prose updates land in pending review with correct frontmatter; self-observations print and can be opt-in stashed; team-update promotes prose updates cleanly.

### 12.9 Hybrid editing — three review semantics behave distinctly

Verify the three review-semantic paths from the ADR don't blur together:

- **Silent (metrics, Track record):** runs `audit` again; metrics refresh + history append happen in one commit with no conductor prompt. Track record section refreshes only on `team reflect`, also silent.
- **Conductor-reviewed (prose updates):** `team reflect` proposes prose updates; nothing lands until `team update` accepts each section explicitly.
- **Conductor-initiated (self-observations):** printed by `team reflect`; no auto-write; nothing lands unless conductor names items to stash.

Run all three in one session and verify each behaves correctly:

```
/hacky-hours audit                 # silent metrics + history
/hacky-hours team reflect product  # silent track record + reviewed prose + printed self-obs
/hacky-hours team update           # conductor reviews the pending prose updates
```

✅ Pass criteria: each path operates as designed; no accidental conflation (e.g., metrics don't end up in the pending review flow; prose updates don't auto-land).

### 12.10 End-to-end thesis verification — this repo, fresh team site

After running Tests 11 (Slice 12) + 12.1–12.9, open the team site one final time:

```
/hacky-hours team resume --all
/hacky-hours team site build
open ~/.hacky-hours/teams/default/docs/index.html
```

**Expected — the thesis becomes visible:**
- Index cards show level badges for agents who've shaped this codebase. Maya, Priya, Alex, Lena, Diego, Emma, Jordan visibly differ from data, ai-ml, FE, BE (who have less or no history on a docs-only repo).
- Click into any agent's profile → see Recent track record timeline of their actual contributions. Lessons applied if they have durable feedback. Résumé link.
- Click the résumé link → see the full synthetic CV with summary, skills, experience by project, recent learnings, and profile.
- Click "← Profile" from résumé → back to profile page.
- Each agent reads as a *teammate with a track record*, not a static persona.

✅ Pass criteria: the conductor opens the team site and recognizes the agents as having grown with the project. The v4 thesis — *"orchestra of stakeholder-role AI agents that learn and grow with context"* — is no longer a claim but a visible fact.

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
