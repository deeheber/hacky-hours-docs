# Install /hacky-hours as a Global Claude Code Command

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

That's it. The script downloads the command file directly from GitHub and places it in `~/.claude/commands/`.

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
| `/hacky-hours` | Show this help message |
| `/hacky-hours ideate` | Jump to Level 1 — Ideation |
| `/hacky-hours design` | Jump to Level 2 — Design |
| `/hacky-hours roadmap` | Jump to Level 3 — Roadmap |
| `/hacky-hours build` | Jump to Level 4 — Build |
| `/hacky-hours iterate` | Start an iteration cycle after a release |
| `/hacky-hours sync` | Push backlog to GitHub Issues, publish a release |
| `/hacky-hours dry-run` | Run the full workflow without writing any files |
| `/hacky-hours status` | Report which framework level this project is at |
| `/hacky-hours checklist` | Show the pre-merge checklist |
| `/hacky-hours version` | Print the installed version |
| `/hacky-hours help` | Same as running with no argument |

---

## Updating

Re-run the same install command. It overwrites the existing file with the latest version.

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/empathetech/hacky-hours-docs/main/install.sh | bash
```

---

## Uninstalling

```bash
# macOS/Linux
rm ~/.claude/commands/hacky-hours.md
```

```powershell
# Windows PowerShell
Remove-Item "$env:USERPROFILE\.claude\commands\hacky-hours.md"
```

---

## Related

- [README.md](../../README.md)
- [import-as-resource.md](./import-as-resource.md) — use this repo as context in another project
- [starter-prompts/](../starter-prompts/) — copy-paste prompts for each level
