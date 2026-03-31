# GitHub Action: Auto-Sync Docs on Merge

> **This is an advanced feature.** You don't need this to use the Hacky Hours framework — it's for teams or individuals who want to automate their workflow further. If you're just getting started, skip this and come back when you're comfortable with the basics. The `/hacky-hours` command handles backlog and changelog updates for you during normal sessions.

This runbook explains how to set up automatic BACKLOG.md and CHANGELOG.md sync using a GitHub Action and the Claude API. A GitHub Action is a small automated task that GitHub runs for you when something happens in your repo — in this case, when a pull request (PR) is merged. This action removes the completed item from your backlog and records it in your changelog automatically.

This is the "across sessions" piece of the GitHub integration. Within a session, Claude Code handles state through your project CLAUDE.md. This action handles what happens when PRs merge between sessions.

---

## How It Works

```
PR merged to main
       ↓
GitHub Action triggers
       ↓
Claude reads PR title + branch + current BACKLOG.md + CHANGELOG.md
       ↓
Claude removes matching item from BACKLOG.md
Claude adds entry to CHANGELOG.md
       ↓
Action commits updated docs back to main
```

---

## Setup

### 1. Copy the workflow file

Copy [`runbooks/templates/hacky-hours-sync.yml`](./templates/hacky-hours-sync.yml) into your project at:

```
.github/workflows/hacky-hours-sync.yml
```

### 2. Add your Anthropic API key as a secret

In your GitHub repo:
- Go to **Settings → Secrets and variables → Actions**
- Click **New repository secret**
- Name: `ANTHROPIC_API_KEY`
- Value: your key from [console.anthropic.com](https://console.anthropic.com)

### 3. Adjust paths if needed

If your BACKLOG.md or CHANGELOG.md live somewhere other than `04-build/`, update the env vars at the top of the workflow:

```yaml
env:
  BACKLOG_PATH: 04-build/BACKLOG.md
  CHANGELOG_PATH: 04-build/CHANGELOG.md
```

### 4. Push and test

Merge a PR and check the **Actions** tab to see the workflow run. The first time, verify the commit it makes to `main` looks right.

---

## What It Does (and Doesn't Do)

**Does:**
- Remove the matching BACKLOG item when a PR merges
- Add a one-line entry to the current CHANGELOG version section
- Commit the changes back to main automatically
- Skip the file update gracefully if no clear match is found

**Doesn't:**
- Close GitHub Issues — Claude Code handles that in-session via `gh issue close`
- Create new CHANGELOG version sections — run `/hacky-hours sync` to publish a release
- Handle merge conflicts if you've made manual edits to both files simultaneously

---

## Matching Logic

Claude uses the PR title and branch name to find the BACKLOG item. For best results:

- Keep BACKLOG item titles descriptive and close to what the PR will be called
- After running `/hacky-hours sync`, BACKLOG items become GitHub Issue links — Claude can also use the issue number in the branch name (e.g., `feat/42-add-auth`) for more reliable matching

---

## Troubleshooting

**Action ran but files didn't change:**
Check the workflow logs — Claude may not have found a clear match. This is safe; it just skips the update.

**Commit failed with permission error:**
Make sure the workflow has `contents: write` permission (it's in the template). Some repos require this to be explicitly enabled in **Settings → Actions → General → Workflow permissions**.

**API key error:**
Verify `ANTHROPIC_API_KEY` is set correctly in your repo secrets and hasn't expired.

---

## Cost

Each merge triggers one Claude API call — typically a few hundred tokens input + a small output. At current pricing this is fractions of a cent per merge. For most projects, monthly cost from this action is negligible.

See [runbooks/costs.md](./costs.md) for a broader cost breakdown.

---

## Related

- [runbooks/document-hygiene.md](./document-hygiene.md) — BACKLOG and CHANGELOG lifecycle
- [runbooks/install-as-command.md](./install-as-command.md) — the in-session complement to this action
- [runbooks/templates/hacky-hours-sync.yml](./templates/hacky-hours-sync.yml) — the workflow file to copy
