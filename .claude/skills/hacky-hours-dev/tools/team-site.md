# /hacky-hours team site — static site for browsing your team

Three modes:

- **`serve`** — start a local HTTP server in the team repo's `docs/` folder for browsing in a real browser
- **`build`** — generate / regenerate the HTML output at `~/.hacky-hours/teams/<team>/docs/`
- **`publish`** — guide the user through enabling GitHub Pages (or other host) on the team repo
- (no subcommand) — equivalent to `build` then prints next-step options

## Step 0 — Pre-flight

1. **Default team exists:** if `~/.hacky-hours/teams/<active>/` doesn't exist, run `/hacky-hours team init` first.
2. **Site template present:** check `~/.hacky-hours/teams/<active>/site/`. If absent, copy from the framework template:
   ```bash
   cp -R ${CLAUDE_SKILL_DIR}/templates/team-site ~/.hacky-hours/teams/<active>/site
   ```
3. **Python 3 available:** the generator is pure Python 3 stdlib. Check `python3 --version`. If missing: print *"This verb needs Python 3 installed. Install via brew/apt/etc., then re-run."* and exit.

## Step 1 — Build (default behavior, also subcommand)

Run the generator:

```bash
cd ~/.hacky-hours/teams/<active>/site/
python3 generate.py
```

Expected output: `Generated site at ~/.hacky-hours/teams/<active>/docs/`. The script writes index.html, agents/*.html, and style.css.

Print to the conductor:

> *"Team site generated at `~/.hacky-hours/teams/<active>/docs/`.*
> *<count> agents rendered.*
>
> *Browse it now:*
> *  - `/hacky-hours team site serve` — local server at http://localhost:8000*
> *  - Or open `~/.hacky-hours/teams/<active>/docs/index.html` directly in your browser (file:// works fine)*"

## Step 2 — Serve subcommand

```bash
cd ~/.hacky-hours/teams/<active>/docs/
python3 -m http.server 8000
```

Tell the user the URL is `http://localhost:8000`. Note: this command will block until they Ctrl+C. The framework should:
- Surface this expectation: *"Server will run until you press Ctrl+C. Open http://localhost:8000 to browse."*
- Not block the agent loop indefinitely — instead, print the command for the user to run themselves rather than the framework spawning it, OR spawn it in the background (background option is acceptable since the user can kill it later).

For v4.0.0: print the command for the user to run. Background-spawning a long-lived process is risky in the framework context.

## Step 3 — Publish subcommand

The static site is designed to work on GitHub Pages directly from the team repo. Guide the user:

1. Confirm the team repo has a git remote configured:
   ```bash
   cd ~/.hacky-hours/teams/<active>/
   git remote -v
   ```

2. If no remote: prompt to set one up. Suggest creating a private GitHub repo first (since teams are private by default), then `git remote add origin <url>`.

3. **Privacy gate (load-bearing):**

   Print prominently:
   > *"⚠️ Publishing this site means making the team repo's contents accessible.*
   > *Three paths:*
   > *  1. **Public repo + public Pages** — your team profiles become publicly browsable. Anyone who finds the URL can read them.*
   > *  2. **Private repo + private Pages** — requires GitHub Pro/Team paid plan. Only repo collaborators can browse.*
   > *  3. **Don't publish** — keep file:// browsing only. Default.*
   >
   > *Per-field privacy: each profile.md has a `published` frontmatter flag. If `published: false`, the agent is skipped entirely from the generated site (the generator already respects this).*
   >
   > *Which path?"*

4. If user picks 1 or 2: walk them through:
   - `git push origin main`
   - Open `https://github.com/<user>/<repo>/settings/pages`
   - Select "Deploy from a branch" → main → `/docs` → Save
   - Wait 1-2 minutes; site URL will appear at the top of the Pages settings page

5. Add a `.github/workflows/deploy-pages.yml` for automated rebuilds on push:
   ```yaml
   name: Build and deploy team site
   on:
     push:
       branches: [main]
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: '3.11'
         - name: Generate site
           run: cd site && python3 generate.py
         - name: Commit docs
           run: |
             git config user.name "github-actions"
             git config user.email "github-actions@github.com"
             git add docs/
             git commit -m "Auto-rebuild team site" || echo "No changes"
             git push
   ```

   Ask before adding this — it's optional.

## Step 4 — Help

```
/hacky-hours team site

Subcommands:
  (none) | build    Regenerate the site at ~/.hacky-hours/teams/<active>/docs/
  serve             Print the command to start a local server
  publish           Guide through GitHub Pages setup
  help              This message

Output: HTML files at ~/.hacky-hours/teams/<active>/docs/
Source: agents/*/profile.md frontmatter in the team repo
Generator: ~/.hacky-hours/teams/<active>/site/generate.py (Python 3 stdlib only)

Privacy: per-field `published` flag in each profile.md frontmatter respected.
History.md and feedback.md are never published.

See V4_DESIGN.md §4.8 for the full static site design.
```

## Notes for the assistant

- **Don't background-spawn the server** in v4.0.0. Print the command instead so the user has direct control.
- **Generator output is overwritten** on each build. If the user customized HTML directly (vs. editing profiles), they should commit before rebuilding.
- **Generated files are committable** — the `docs/` folder is part of the team repo and used by GitHub Pages. The site/.gitignore should NOT ignore docs/.
- **When the team gets updated** (`/hacky-hours team update` lands new agent feedback / prompt changes), the static site doesn't auto-rebuild. Suggest: *"You promoted changes — want to rebuild the site? `/hacky-hours team site build`"*
