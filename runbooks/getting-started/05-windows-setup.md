# Runbook: Windows Setup

This runbook installs the minimum tooling needed on Windows to use the Hacky Hours workflow: a terminal, Node.js, git, and Claude Code.

**New to terminals?** Read [`00-what-is-a-terminal.md`](./00-what-is-a-terminal.md) first — it explains what all of this is and why you need it.

---

## 1. Install Windows Terminal (recommended)

Windows Terminal is a modern terminal app that supports multiple shells. Download it from the [Microsoft Store](https://aka.ms/terminal) or [GitHub](https://github.com/microsoft/terminal/releases).

Alternatively, use **PowerShell** (already installed on Windows 10/11) or **Git Bash** (installed with Git in step 3).

---

## 2. Install Node.js

Node.js is required to install Claude Code.

1. Go to [nodejs.org](https://nodejs.org) and download the **LTS** version
2. Run the installer — accept the defaults
3. Verify the install by opening a terminal and running:

```powershell
node --version
npm --version
```

Both should print a version number.

---

## 3. Install Git

1. Download [Git for Windows](https://git-scm.com/download/win)
2. Run the installer. On the "Choosing the default editor" step, select **Visual Studio Code** if you have it installed, or keep the default
3. On the "Adjusting your PATH environment" step, select **Git from the command line and also from 3rd-party software**
4. Accept the remaining defaults
5. Verify:

```powershell
git --version
```

---

## 4. Install VS Code

Download and install from [code.visualstudio.com](https://code.visualstudio.com). See [04-ide-setup.md](./04-ide-setup.md) for recommended extensions.

---

## 5. Install Claude Code

In your terminal:

```powershell
npm install -g @anthropic-ai/claude-code
```

Then follow [02-claude-code.md](./02-claude-code.md) to authenticate.

---

## Troubleshooting

**"npm is not recognized as a command"** — Your terminal can't find Node.js. This usually means it isn't in your [PATH](../../GLOSSARY.md) (the list of places your computer looks for programs). Try closing and reopening your terminal first — that often fixes it. If not, reinstall Node.js.

**Permission errors during npm install** — Open your terminal as Administrator (right-click → Run as administrator) and retry.

**Git Bash vs PowerShell** — Either works. Git Bash behaves more like a Unix shell (recommended if commands in other runbooks use `ls`, `cat`, etc.).

---

## You're Done When...

Run these three commands and confirm each prints a version number:

```powershell
node --version
git --version
code --version
```

If all three respond with a version, your Windows setup is complete. Move on to [`02-claude-code.md`](./02-claude-code.md).

---

## Related

- [00-what-is-a-terminal.md](./00-what-is-a-terminal.md)
- [01-github.md](./01-github.md)
- [02-claude-code.md](./02-claude-code.md)
- [03-git-basics.md](./03-git-basics.md)
- [04-ide-setup.md](./04-ide-setup.md)
