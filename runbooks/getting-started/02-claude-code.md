# Runbook: Set Up Claude Code

Claude Code is Anthropic's CLI (command-line interface) for working with Claude directly inside your project. It reads your files, understands your context, and helps you build — all within your terminal and editor.

---

## What You'll Need

- An Anthropic account (or access through Claude.ai)
- Node.js installed (version 18 or higher — see your OS setup runbook)
- A terminal (built into macOS and Linux; on Windows, use Windows Terminal or PowerShell)

---

## Steps

### 1. Create an Anthropic account

Go to [claude.ai](https://claude.ai) and sign up. Claude Code requires a **Claude Pro** subscription (check [claude.ai/pricing](https://claude.ai/pricing) for current pricing — it is a paid plan). The free Claude account lets you chat on the website, but Claude Code — which reads your project files and works directly inside your codebase — is a Pro feature. If you're just evaluating, the setup steps below work the same; you'll just need to subscribe before Claude Code will let you run sessions.

### 2. Install Claude Code

In your terminal, run:

```bash
npm install -g @anthropic-ai/claude-code
```

The `-g` flag means "install globally" — it makes the `claude` command available everywhere on your computer, not just in one project folder.

### 3. Authenticate

Run:

```bash
claude
```

On first launch, Claude Code will open a browser window to authenticate with your Anthropic account. Follow the prompts.

### 4. Start a session in your project

Navigate to your project folder in the terminal. Replace the path below with the actual location of your project — for example, if you cloned it to your Documents folder:

```bash
cd ~/Documents/my-project-docs
claude
```

> **Tip:** Not sure of your folder path? In VS Code, right-click any file in the Explorer panel and choose "Copy Path" to get it.

Claude Code will read any `CLAUDE.md` file in the directory and use it as context. This is the mechanism the Hacky Hours framework uses to keep Claude aligned with your project.

### 5. Verify it works

Try asking Claude something about your project:

```
What files are in this directory?
```

If Claude responds with an accurate list, you're set up correctly.

---

## Tips

- **Keep your CLAUDE.md updated** — Claude reads it at the start of every session. The more context it has, the better aligned it will be.
- **Use `/help`** in the Claude Code session to see available commands.
- **Press Ctrl+C** to exit a session.

---

## You're Done When...

You can type `claude` in your terminal inside your project folder and Claude responds to a question. If it asks you to authenticate, follow the browser prompt — that's expected on first run.

---

## Related

- [01-github.md](./01-github.md)
- [04-ide-setup.md](./04-ide-setup.md)
- [import-as-resource.md](../using-this-repo/import-as-resource.md)
