# Install /hacky-hours as a Claude Code Skill

## What is this?

When you're in a Claude Code session, you can type `/hacky-hours` to give Claude the full Hacky Hours framework as context, so it can guide you through ideation, design, roadmap, build, and release cycles in any project.

As of v3.0.0, `hacky-hours` ships as a [Claude Code Skill](https://code.claude.com/docs/en/skills) — a directory under `~/.claude/skills/` with a small entrypoint plus per-step / per-review supporting files that load only when you use them. (Prior versions shipped as a single `.md` file under `~/.claude/commands/`. The installer migrates you automatically.)

Installing means you can type `/hacky-hours` in any Claude Code session and it just works — no need to clone this repo or copy files around.

---

One command installs `/hacky-hours` so it works in **any repo you open** in Claude Code — no cloning required.

---

## Install

### macOS / Linux

Open a terminal and run:

```bash
curl -fsSL https://raw.githubusercontent.com/empathetech/hacky-hours-docs/main/install.sh | bash
```

### Windows

Open PowerShell and run:

```powershell
irm https://raw.githubusercontent.com/empathetech/hacky-hours-docs/main/install.ps1 | iex
```

That's it. The script downloads the skill directory from GitHub and places it at `~/.claude/skills/hacky-hours/`. If you have a v2.x install at `~/.claude/commands/hacky-hours.md`, the script removes it automatically. **Restart Claude Code** after install — the new top-level `.claude/skills/` directory needs to be picked up.

---

## Verify It Works

1. Open a terminal in **any project** — something unrelated to hacky-hours-docs
2. Start a Claude Code session: `claude`
3. Type `/hacky-hours` and press Enter

Claude should print the help message listing all available arguments.

---

## Using the Command

| Command | What it does |
|---------|-------------|
| `/hacky-hours` | Survey your project and report where you are |
| `/hacky-hours step 1` | Step 1 — Ideation |
| `/hacky-hours step 2` | Step 2 — Design |
| `/hacky-hours step 3` | Step 3 — Roadmap |
| `/hacky-hours step 4` | Step 4 — Build |
| `/hacky-hours step 5` | Step 5 — Iterate (post-release cycle) |
| `/hacky-hours review 1` | Did we follow best practices? |
| `/hacky-hours review 2` | Did we build it well? |
| `/hacky-hours review 3` | Should we build something else? |
| `/hacky-hours learn 1` | Tour — big-picture walkthrough |
| `/hacky-hours learn 2` | Onboard — hands-on starter task |
| `/hacky-hours learn 3` | Quiz — test your knowledge |
| `/hacky-hours update 1` | Publish a new release |
| `/hacky-hours update 2` | Sync BACKLOG ↔ GitHub Issues |
| `/hacky-hours tools upgrade` | Update framework artifacts (also: adopt or migrate) |
| `/hacky-hours tools mode` | Toggle between plain-language and technical mode |
| `/hacky-hours tools walkthrough` | Narrative overview of how all commands work together |
| `/hacky-hours step 0` | Explore without writing any files (safe to try) |
| `/hacky-hours help` | Full help message |

---

## Updating

Re-run the same install command. It downloads the latest version, replaces the existing skill directory, and removes any stale v2.x command file. Restart Claude Code after the install completes.

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/empathetech/hacky-hours-docs/main/install.sh | bash
```

---

## Uninstalling

```bash
# macOS/Linux
rm -rf ~/.claude/skills/hacky-hours
# If a stale v2.x file is still around, also:
rm -f ~/.claude/commands/hacky-hours.md
```

```powershell
# Windows PowerShell
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\hacky-hours"
# If a stale v2.x file is still around, also:
Remove-Item -Force "$env:USERPROFILE\.claude\commands\hacky-hours.md" -ErrorAction SilentlyContinue
```

---

## Related

- [README.md](../../README.md)
- [import-as-resource.md](./import-as-resource.md) — use this repo as context in another project
- [starter-prompts/](../starter-prompts/) — copy-paste prompts for each step
