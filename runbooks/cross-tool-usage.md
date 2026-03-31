# Using Hacky Hours Without Claude Code

The `/hacky-hours` slash command is a convenience built for Claude Code. But the framework itself is just Markdown files — it works in **any tool that lets an LLM read project context**.

This includes:
- **Cursor** — a code editor (based on VS Code) with built-in AI features
- **Windsurf** — another AI-powered code editor
- **Claude.ai Projects** — Claude's web interface, where you can upload files and set project-level instructions
- **Any MCP-compatible client** — MCP (Model Context Protocol) is a standard for connecting AI tools to external data; if your tool supports it, it can read these docs
- **Any LLM chat where you can paste context** — even a plain ChatGPT or Claude conversation works if you copy-paste the relevant docs

---

## How It Works

The framework runs on two things:

1. **The artifact files** in your `hacky-hours/` folder (or wherever you scaffolded them)
2. **The `CLAUDE.md` project instructions** at your repo root

When you scaffold a project with `/hacky-hours` (or manually create the structure), the generated `CLAUDE.md` contains a **project state machine** — instructions that tell Claude to check your backlog, track completed work, and follow your design constraints. Any tool that reads `CLAUDE.md` picks this up automatically.

---

## Setup for Cursor

Cursor reads project-level instructions from `.cursorrules` or `.cursor/rules/` files. You have two options:

### Option A: Use CLAUDE.md directly (recommended)

Cursor's Claude integration reads `CLAUDE.md` files. If your project already has one (from scaffolding or adopt), Cursor will follow the project state machine automatically.

Just open your project in Cursor and start talking to Claude:
- "What's in my backlog?"
- "Help me with ideation for this project"
- "I want to start designing the data model"
- "Run through the pre-merge checklist"

### Option B: Copy to .cursorrules

If Cursor doesn't read your `CLAUDE.md`, copy the Project State Machine section into a `.cursorrules` file:

```bash
# Extract the state machine from CLAUDE.md
grep -A 50 "## Project State Machine" CLAUDE.md > .cursorrules
```

---

## Setup for Claude.ai Projects

1. Create a new Project at [claude.ai](https://claude.ai)
2. In the Project Instructions, paste the contents of your `CLAUDE.md`
3. Upload your `hacky-hours/` folder contents as project knowledge
4. Start a conversation — Claude will follow the framework

---

## What You Lose Without the Slash Command

The slash command provides:
- **Argument routing** (`/hacky-hours ideate`, `/hacky-hours audit`, etc.)
- **Automatic file scaffolding** (creates the folder structure)
- **Guided workflows** (step-by-step facilitation for each level)

Without it, you get the same framework behavior through natural language. Instead of `/hacky-hours ideate`, you say "help me with ideation." Instead of `/hacky-hours audit`, you say "check if this project is ready to release."

The artifacts, design constraints, and project state machine all work identically — the difference is in how you invoke them, not what they do.

---

## What You Keep

- The four-level structure (Ideation, Design, Roadmap, Build)
- Design document templates
- Safety-first defaults
- The iterate cycle (capture, synthesize, prioritize, build)
- BACKLOG.md as a queue, CHANGELOG.md as the record
- The project state machine (auto-orient, track work, suggest next steps)

---

## Related

- [Install as a Claude Code command](./install-as-command.md) — for full slash command support
- [Import as a resource](./using-this-repo/import-as-resource.md) — git submodule, CLAUDE.md snippet, or manual copy
