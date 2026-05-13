# /hacky-hours team — manage your persistent team

This verb manages the user's persistent team of stakeholder-role AI agents. The team lives at `~/.hacky-hours/teams/<team-name>/` as its own git repo — separate from any project, portable across machines, applied to projects by binding.

## Subcommand dispatch

Parse the rest of `$ARGUMENTS` after `team`:

- (no subcommand)             → run **Survey & Browse** below (list teams; show active team summary)
- "list"                      → list all teams in `~/.hacky-hours/teams/`, show which is active
- "show <agent-id>"           → show a specific agent's profile + system prompt + recent history
- "switch <team-name>"        → change the active team for the current project (writes to project's AGENTS.md)
- "new [--tier <tier>]"       → create a new team (interactive; defaults to "full" tier)
- "init"                      → if `~/.hacky-hours/teams/default/` doesn't exist, create it from the template; otherwise no-op
- "update"                    → Read `${CLAUDE_SKILL_DIR}/tools/team-update.md` and follow it (promote session customizations into the team repo)
- "site" or "site <subcommand>" → Read `${CLAUDE_SKILL_DIR}/tools/team-site.md` and follow it (static site for browsing — serve / build / publish)
- "help"                      → print the help message below, then stop

## Step 0 — Ensure global skeleton exists

If `~/.hacky-hours/` does not exist, return control to `tools/v4-first-run.md` first (it'll handle setup, then return here).

## Step 1 — Ensure the default team exists

Check whether `~/.hacky-hours/teams/default/` exists. If it doesn't, this is the user's first time invoking `team` after first-run. Run **Default Team Bootstrap** below before proceeding.

### Default Team Bootstrap

Print:

> *"You don't have any teams yet — let me set up your default team. This is a full 12-agent roster (product, design, architect, FE, BE, security, ops, QA, a11y, licensing, data, AI/ML) — your starting orchestra. You can create leaner teams later via `/hacky-hours team new`.*
>
> *Setting up at `~/.hacky-hours/teams/default/`..."*

Then:

1. Copy the template tree from `${CLAUDE_SKILL_DIR}/templates/team/default/` to `~/.hacky-hours/teams/default/`. Use `cp -R` or equivalent.

2. **Stamp the date and conductor identifier** in the template files. Replace literal `TEMPLATE` with today's date (YYYY-MM-DD) in:
   - `~/.hacky-hours/teams/default/README.md` (the `established:` frontmatter field)
   - Each agent's `profile.md` (the `joined:` frontmatter field)

3. **Initialize the git repo** for the team:
   ```
   cd ~/.hacky-hours/teams/default/
   git init
   git add .
   git commit -m "Initial team — created by Hacky Hours v4.0.0-dev"
   ```

   Do not push to a remote. The team is local-only by default. The user can `git remote add` later if they want cross-device sync.

4. Print:

   > *"Done. Your team is at `~/.hacky-hours/teams/default/`. Twelve agents ready:*
   >
   > *📊 Maya Tanaka (Product) · 🎨 Felix Okafor (Design) · 🏗️ Priya Chen (Architect)*
   > *🖥️ Marcus Rivera (Frontend) · ⚙️ Sam Park (Backend) · 🛡️ Alex Davies (Security)*
   > *🚀 Jordan Kim (Ops) · 🔍 Emma Wright (QA) · ♿ Lena Mwangi (A11y)*
   > *📜 Diego Romano (Licensing) · 📈 Yuki Nakamura (Data) · 🤖 Kai Patel (AI/ML)*
   >
   > *Try:*
   > *  - `/hacky-hours team show alex` — meet the security engineer*
   > *  - `/hacky-hours team list` — see your teams*
   > *  - `/hacky-hours adopt` — bring an existing codebase into the framework*
   > *  - `/hacky-hours ideate` — start a new project*"

Then return — don't continue into Browse unless the user invoked it without a subcommand.

## Step 2 — Survey & Browse (default behavior with no subcommand)

After ensuring the default team exists, print a one-screen summary of the active team:

1. Determine active team:
   - If invoked inside a project repo, read `AGENTS.md` for `team:` field
   - Otherwise, treat `default` as active

2. Read `~/.hacky-hours/teams/<active>/README.md` and `tier.yml` for context.

3. Print:

   ```
   Active team: <team-name> (<tier>)
   <one-line philosophy from README frontmatter>

   Roster (<count> agents):
     <emoji> <Name> — <Role> · <tagline>
     ...

   Commands:
     /hacky-hours team show <agent-id>   Read a specific agent's profile + system prompt
     /hacky-hours team list              List all your teams
     /hacky-hours team new               Create a new team (different tier or specialization)
     /hacky-hours team switch <name>     Bind this project to a different team
     /hacky-hours team help              Full help
   ```

   Read each agent's profile.md frontmatter to populate the roster lines (emoji, name, hat, tagline).

## Step 3 — Subcommand handlers

### `list`

List all teams in `~/.hacky-hours/teams/`:
```
Teams (3):
  * default     full tier · 12 agents · created 2026-05-13 · active for this project
    lean-solo   solo tier ·  3 agents · created 2026-05-14
    healthcare  full tier · 13 agents (+1 SME) · created 2026-06-01
```

Mark the active team for the current project (if invoked in a project repo).

### `show <agent-id>`

Read `~/.hacky-hours/teams/<active>/agents/<agent-id>/`:
- Print frontmatter as a profile header (name, pronouns, hats, tagline, specialties)
- Print "Background" + "How I work" + "What I produce" sections from profile.md
- Offer: *"Want to see <name>'s full system prompt? (`/hacky-hours team show <agent-id> --prompt`)"*
- If `--prompt` flag: print system-prompt.md

### `switch <team-name>`

- Validate that `~/.hacky-hours/teams/<team-name>/` exists
- If invoked inside a project repo:
  - Update or create `AGENTS.md` in the project with `team: <team-name>`
  - Confirm: *"This project now binds to team `<team-name>`."*
- If not in a project repo: print *"`team switch` updates the team binding for the current project. You're not in a project repo right now — run this command from inside one."*

### `new [--tier <tier>]`

Interactive flow to create a new team:
1. Ask for team name (kebab-case)
2. Ask for tier (default: ask, options: solo / lean / startup / full)
3. Ask for intended use (free-text → becomes part of README.md philosophy)
4. Create the directory at `~/.hacky-hours/teams/<name>/` by copying the default template
5. Adjust `tier.yml` based on chosen tier (for solo/lean/startup, remove or merge agent folders accordingly — see `references/team-tiers.md`, deferred)
6. For v4.0.0-dev, only "full" tier is fully implemented. For solo/lean/startup: print *"<tier> tier is in development. Defaulting to full tier for now — you can manually remove agents from `~/.hacky-hours/teams/<name>/agents/` and update `tier.yml`."*
7. `git init` + initial commit in the new team repo

### `init`

Same as Default Team Bootstrap. Useful for users who want to re-create the default team after deletion.

### `update`

Routed to `${CLAUDE_SKILL_DIR}/tools/team-update.md`. See that file for the full flow — captures pending session changes, presents per-change accept/edit/reject/defer review, commits accepted changes to the team repo.

### `site` (and subcommands `serve`, `build`, `publish`)

Routed to `${CLAUDE_SKILL_DIR}/tools/team-site.md`. See that file for the full flow — generates static HTML site from agent profiles using a Python 3 stdlib-only generator (no npm), supports `serve`, `build`, `publish` (GitHub Pages).

### `help`

Print this:

```
/hacky-hours team — manage your persistent team

Subcommands:
  (none)                   Show active team roster
  list                     List all teams
  show <agent-id>          View agent profile + bio
  show <agent-id> --prompt View agent's full system prompt
  switch <name>            Bind current project to a different team
  new [--tier <tier>]      Create a new team
  init                     Create the default team (idempotent)

Coming in later slices:
  update                   Promote pending session changes to team repo
  site [serve|build|publish]  Static site for browsing
  help                     Show this message

Teams live at ~/.hacky-hours/teams/<name>/ — each is its own git repo.
See V4_DESIGN.md §4.5–4.9 for the team architecture.
```

---

## Notes for the assistant running this

- All file operations on the team repo (`~/.hacky-hours/teams/<name>/`) should respect the framework principle that **the team is the user's source of truth**. Don't write to it silently — for any non-trivial change, confirm with the conductor first.
- The default team's `README.md` and each agent's `profile.md` ship with the literal token `TEMPLATE` in date fields. The Bootstrap step replaces these with today's date. Use `sed` or equivalent for portability across macOS and Linux:
  ```bash
  TODAY=$(date +%Y-%m-%d)
  find ~/.hacky-hours/teams/default -name "*.md" -exec sed -i.bak "s/TEMPLATE/$TODAY/g" {} \;
  find ~/.hacky-hours/teams/default -name "*.bak" -delete
  ```
- The template files in `${CLAUDE_SKILL_DIR}/templates/team/default/` are MIT-licensed (part of the framework). When copied to `~/.hacky-hours/teams/default/`, they become user-owned (private by default per the LICENSE file in the template).
