# Runbook: GitHub Desktop (Git Without the Terminal)

GitHub Desktop is a free app that lets you do all your git operations — cloning, committing, pushing, branching — by clicking buttons instead of typing terminal commands.

If the git commands in `03-git-basics.md` felt intimidating, use this instead. You only need the terminal for installing tools and running Claude Code. Everything else can be done in GitHub Desktop.

---

## What You'll Need

- A GitHub account ([01-github.md](./01-github.md))
- Your OS setup complete ([05](./05-windows-setup.md) / [06](./06-macos-setup.md) / [07](./07-linux-setup.md))

---

## Install GitHub Desktop

Download from [desktop.github.com](https://desktop.github.com) and install it. It's available for macOS and Windows. Linux users: use the terminal git workflow from `03-git-basics.md` instead, or try a third-party client like [GitKraken](https://www.gitkraken.com).

---

## Steps

### 1. Sign in

Open GitHub Desktop and click **Sign in to GitHub.com**. It will open a browser to authenticate — follow the prompts.

> **Screenshot:** GitHub Desktop welcome screen with Sign In button

### 2. Clone your fork

After signing in, GitHub Desktop shows your repositories.

1. Click **Clone a repository from the Internet**
2. Find your forked `hacky-hours-docs` repo in the list (or paste its URL)
3. Choose where to save it on your computer — e.g., `~/Documents/my-project-docs`
4. Click **Clone**

> **Screenshot:** GitHub Desktop clone dialog with repository list

### 3. Open in VS Code

Once cloned, click **Open in Visual Studio Code** in GitHub Desktop.

> **Screenshot:** GitHub Desktop showing "Open in Visual Studio Code" button

---

## The Daily Workflow in GitHub Desktop

Instead of typing git commands, you use the interface:

**To save your work to GitHub:**

1. Edit your files in VS Code
2. Switch to GitHub Desktop — it automatically shows what changed
3. Write a short description in the **Summary** box (e.g., "Update product overview")
4. Click **Commit to main**
5. Click **Push origin** in the top bar

> **Screenshot:** GitHub Desktop showing changed files, summary field, and Commit button

**To get updates from GitHub** (e.g., after editing on another computer):

Click **Fetch origin** → **Pull origin** in the top bar.

**To create a branch** (for a specific task):

Click **Current Branch → New Branch**, type a name, click **Create Branch**.

---

## What GitHub Desktop Does NOT Do

GitHub Desktop handles version control, but you still need the terminal for:
- Installing and running Claude Code (`claude`)
- Installing Node.js, git, etc. (done during OS setup — one time only)

---

## You're Done When...

You can open GitHub Desktop, see your project files listed, make a change in VS Code, commit it in GitHub Desktop, and see the commit appear on your GitHub repo page in the browser.

---

## Related

- [Getting Started README](./README.md)
- [03-git-basics.md](./03-git-basics.md)
- [fork-vs-clone.md](../using-this-repo/fork-vs-clone.md)
