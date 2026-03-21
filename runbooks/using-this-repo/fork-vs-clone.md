# Fork vs Clone

When starting a new project with the Hacky Hours framework, you need your own copy of this repo. Here's how to get it.

**Just getting started?** Follow the beginner path below — it's three steps.

---

## The Beginner Path: Fork on GitHub, then Clone Locally

### Step 1: Fork on GitHub

1. Go to the `hacky-hours-docs` repository on GitHub
2. Click the **Fork** button in the top right

> **Screenshot:** GitHub repository page with Fork button highlighted

3. On the next screen, choose your account as the destination and click **Create fork**

This creates your own personal copy of the repo on GitHub. You can now modify it freely without affecting the original.

### Step 2: Clone it to your computer

Cloning downloads your fork to your computer so you can work on it locally.

On your fork's GitHub page, click the green **Code** button and copy the HTTPS URL. Then in your terminal:

```bash
git clone https://github.com/YOUR-USERNAME/hacky-hours-docs.git my-project-docs
```

Replace `YOUR-USERNAME` with your GitHub username (e.g., `git clone https://github.com/jsmith/hacky-hours-docs.git my-project-docs`).

> **Screenshot:** GitHub Code button dropdown showing the HTTPS URL to copy

### Step 3: Open it

```bash
cd my-project-docs
code .
```

You're done. Your project folder is open in VS Code and connected to your GitHub repo.

---

## Renaming Your Fork (optional but recommended)

After forking, rename the repo in GitHub to match your actual project:

1. Go to your forked repo on GitHub → **Settings**
2. Change the **Repository name** to something like `my-app-docs`
3. Update the URL in your local clone to match:

```bash
git remote set-url origin https://github.com/YOUR-USERNAME/my-app-docs.git
```

---

## What's the Difference Between Fork and Clone?

| | Fork | Clone |
|--|------|-------|
| Where it happens | On GitHub (in your browser) | On your computer (in the terminal) |
| What it creates | A copy of the repo on your GitHub account | A local copy on your hard drive |
| When you need it | Once, to get your own GitHub copy | Once, to download it locally |

You always do both: fork first, then clone your fork.

---

## Advanced: Keeping Your Fork Updated

If the Hacky Hours framework releases improvements you want to pull in, you can connect your fork back to the original:

<details>
<summary>Show advanced steps</summary>

```bash
# Add the original repo as a remote called "upstream"
git remote add upstream https://github.com/empathetech/hacky-hours-docs.git

# Pull in updates from the original
git fetch upstream
git merge upstream/main
```

You only need to do the first command once. Run the second two whenever you want to pull in new framework updates.

</details>

---

## You're Done When...

You can open your terminal, `cd` into your project folder, run `git status`, and see "On branch main" with your project files listed. That means your local clone is connected to your GitHub fork and ready to use.

---

## Editing Files Without VS Code: GitHub's Web Editor

If you just want to edit a Markdown file and don't want to open a terminal or VS Code, GitHub has a built-in editor that works entirely in your browser.

1. Go to any file in your forked repo on GitHub
2. Click the **pencil icon** (Edit this file) in the top right of the file view
3. Make your changes in the editor
4. Scroll down and click **Commit changes** with a short description

> **Screenshot:** GitHub file view with pencil/edit icon highlighted

This is useful for quick edits to documents — filling in a section of `IDEATION.md`, updating `PRODUCT_OVERVIEW.md`, etc. For anything involving running Claude Code or building the actual app, you'll still need a terminal (or Codespaces).

---

## Related

- [Getting Started README](../getting-started/README.md)
- [08-github-codespaces.md](../getting-started/08-github-codespaces.md)
- [01-github.md](../getting-started/01-github.md)
- [03-git-basics.md](../getting-started/03-git-basics.md)
- [import-as-resource.md](./import-as-resource.md)
