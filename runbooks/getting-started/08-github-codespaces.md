# Runbook: GitHub Codespaces (Zero-Install Option)

**This is the fastest way to get started.** GitHub Codespaces gives you a full development environment — editor, terminal, and all tools — that runs entirely in your web browser. No downloads, no installs, no terminal setup on your own computer.

If the macOS/Windows/Linux setup runbooks felt overwhelming, start here instead.

---

## What You'll Need

- A GitHub account ([01-github.md](./01-github.md))
- A Claude Pro subscription ([claude.ai/pricing](https://claude.ai/pricing))
- A web browser

That's it.

---

## What Is a Codespace?

A Codespace is a computer that runs in the cloud and is accessible from your browser. It comes pre-loaded with a code editor (VS Code), a terminal, and common developer tools. When you close the browser tab, the Codespace pauses — your work is saved and waiting when you come back.

GitHub gives every account a free monthly allowance of Codespace usage. For documentation-only work (Markdown files), you're unlikely to exceed the free tier.

---

## Steps

### 1. Fork this repo

1. Go to the `hacky-hours-docs` repository on GitHub
2. Click **Fork** → **Create fork**

> **Screenshot:** GitHub repository with Fork button highlighted

### 2. Open your fork in a Codespace

1. On your forked repo page, click the green **Code** button
2. Click the **Codespaces** tab
3. Click **Create codespace on main**

> **Screenshot:** Code button dropdown showing Codespaces tab and "Create codespace on main" button

GitHub will spend about 30–60 seconds setting up your environment. When it's ready, VS Code opens in your browser with your repo files in the left panel.

### 3. Open the terminal inside the Codespace

In the VS Code menu bar: **Terminal → New Terminal**

A terminal panel opens at the bottom of the screen. This terminal runs on the cloud computer — not on your laptop.

> **Screenshot:** VS Code in browser with terminal panel open at bottom

### 4. Install Claude Code

In the Codespace terminal, run:

```bash
npm install -g @anthropic-ai/claude-code
```

### 5. Start a Claude Code session

```bash
claude
```

The first time, it will print a URL — something like `https://claude.ai/auth/...`. Since the terminal is running on a cloud computer (not your laptop), it can't open a browser automatically. Copy that URL and paste it into a new browser tab on your computer. Complete the sign-in there, and Claude Code will detect the authentication and continue.

After that first login, your credentials are saved on the Codespace VM. Future sessions just need `claude` — no re-authentication needed, as long as you're resuming the same Codespace.

> **Note:** If you delete your Codespace and create a new one, you'll need to run `npm install -g @anthropic-ai/claude-code` and authenticate again. To avoid this, see the advanced section below.

---

## Saving Your Work

In a Codespace, your files are automatically saved locally to the cloud computer. To save them back to GitHub (so they're permanent and accessible from anywhere):

```bash
git add .
git commit -m "Update my project docs"
git push
```

Or use the **Source Control** panel in VS Code (the branch icon in the left sidebar) to commit and push with buttons instead of commands.

---

## Auto-Installing Claude Code (Advanced)

To avoid re-installing Claude Code every time you create a new Codespace, you can configure your repo to install it automatically. Create a file at `.devcontainer/devcontainer.json` in your project with:

```json
{
  "postCreateCommand": "npm install -g @anthropic-ai/claude-code"
}
```

This runs automatically whenever a new Codespace is created from your repo.

---

## Codespace Limits

GitHub's free tier includes **120 core-hours per month** — roughly 60 hours of active use on a 2-core machine. For documentation work, this is more than enough. If you hit the limit, you can either wait for the monthly reset or upgrade your GitHub plan.

Check your usage at: **github.com → Settings → Billing → Codespaces**

---

## You're Done When...

You can see your project files in the VS Code file explorer inside the browser, open a terminal at the bottom, and type `claude` to start a session. You don't need to install anything else locally.

---

## Related

- [Getting Started README](./README.md)
- [01-github.md](./01-github.md)
- [02-claude-code.md](./02-claude-code.md)
- [fork-vs-clone.md](../using-this-repo/fork-vs-clone.md)
