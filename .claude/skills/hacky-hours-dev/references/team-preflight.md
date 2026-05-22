# Team pre-flight — required by every multi-role verb

Every verb that fans out to roles, reads from `~/.hacky-hours/teams/<active>/agents/`, or runs Phase N — Stash must run these two checks before doing anything else. Without them, a first-time v4 user hits a missing-directory crash partway through their first verb (see empathetech/hacky-hours-docs#7).

## Step 1 — Global skeleton

If `~/.hacky-hours/` doesn't exist, Read `${CLAUDE_SKILL_DIR}/tools/v4-first-run.md` first and follow it, then return here.

## Step 2 — Default team

If `~/.hacky-hours/teams/default/` doesn't exist, Read `${CLAUDE_SKILL_DIR}/tools/team.md` and run the **Default Team Bootstrap** section there, then return here.

---

After both checks pass, continue with the verb's normal flow.

## Why this file exists

`tools/adopt.md` and `tools/team.md` historically held these checks inline. Step verbs, `reviews/audit.md`, and `tools/arbitrate.md` did not, so they crashed for first-time users (empathetech/hacky-hours-docs#7). Centralizing the checks here means there's one source of truth and one place to update if the bootstrap requirements change.

## Verbs that include this preflight

- `steps/01-ideate.md` through `steps/05-iterate.md`
- `reviews/audit.md`
- `tools/arbitrate.md`
- `tools/adopt.md`

`tools/team.md` and `tools/v4-first-run.md` are exempt — they *are* the bootstrap. Other `tools/team-*.md` files (team-backfill, team-resume, team-reflect, team-update, team-site) are also exempt because `tools/team.md` routes through its Step 1 (Ensure the default team exists) before dispatching to them.
