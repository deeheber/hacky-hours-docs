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

Claude should respond by surveying the project and offering options.

---

## Using the Command

| Command | What it does |
|---------|-------------|
| `/hacky-hours` | Auto-detects your project's state and presents options |
| `/hacky-hours ideate` | Jump directly to Level 1 — Ideation |
| `/hacky-hours design` | Jump directly to Level 2 — Design |
| `/hacky-hours roadmap` | Jump directly to Level 3 — Roadmap |
| `/hacky-hours build` | Jump directly to Level 4 — Build |

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
