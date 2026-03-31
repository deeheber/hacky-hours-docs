# Runbook: Git Basics

Git is the version control system that tracks changes to your project over time. Think of it as a detailed save history — you can always go back to a previous state, see exactly what changed, and collaborate without overwriting each other's work.

This runbook covers the commands you'll use in the Hacky Hours workflow.

---

## Install Git

**macOS:** Git may already be installed. Run `git --version` in your terminal. If not, install it via [Homebrew](https://brew.sh): `brew install git`

**Windows:** Download and install [Git for Windows](https://git-scm.com/download/win). Use "Git Bash" as your terminal for the commands in this guide.

**Linux:** `sudo apt install git` (Debian/Ubuntu) or `sudo dnf install git` (Fedora)

---

## One-Time Setup

Configure your identity — this appears in your commit history:

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## The Core Workflow

### Clone a repository (get a copy of an existing repo)

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### Check what's changed

```bash
git status
```

### Stage changes (prepare them to be saved)

```bash
git add .          # stage all changes
git add file.md    # stage a specific file
```

### Commit (save a snapshot with a message)

```bash
git commit -m "Add initial product overview"
```

Write commit messages in present tense, describing what the change does: "Add user journey for sign-up", not "Added some stuff".

### Push (send your commits to GitHub)

```bash
git push
```

### Pull (get changes from GitHub)

```bash
git pull
```

---

## Working with Branches

A **branch** is a separate copy of your project that lives alongside the main version. You make changes on the branch without affecting anything else. When you're happy with the changes, you merge them back into the main version.

Why bother? Because it lets you experiment freely. If your changes don't work out, you can throw the branch away without having touched anything important.

### Create a new branch and switch to it

The `-b` flag means "create a new branch." The name after it is whatever you want to call your branch.

```bash
git checkout -b feat/user-signup
```

You're now working on the `feat/user-signup` branch. Any changes you make here won't affect `main`.

### Switch back to the main branch

```bash
git checkout main
```

### Push your branch to GitHub

The first time you push a new branch, use `-u origin` to tell GitHub about it. After that, plain `git push` works.

```bash
git push -u origin feat/user-signup  # first time
git push                             # every time after
```

### Merge your changes

When your work is ready, open a **Pull Request** (PR) on GitHub — it's a request to merge your branch into `main`. Even working solo, PRs create a record of what changed and why. On your repo's GitHub page, click **Pull requests → New pull request**, select your branch, and follow the prompts.

---

## The Hacky Hours Branch Pattern

Each task in `BACKLOG.md` gets its own branch, named consistently:

| Type | Pattern | Example |
|------|---------|---------|
| New feature | `feat/description` | `feat/user-signup` |
| Bug fix | `fix/description` | `fix/login-error` |
| Documentation | `docs/description` | `docs/update-readme` |
| Chore / setup | `chore/description` | `chore/add-linting` |

---

## You're Done When...

You can run `git status` inside your project folder and see a response (even if it says "nothing to commit" — that means it's working). You've also set your name and email with `git config`.

---

## Related

- [01-github.md](./01-github.md)
- [04-build/README.md](../../04-build/README.md)
- [fork-vs-clone.md](../using-this-repo/fork-vs-clone.md)
