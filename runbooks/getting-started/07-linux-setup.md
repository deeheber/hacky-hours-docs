# Runbook: Linux Setup

This runbook installs the minimum tooling needed on Linux to use the Hacky Hours workflow: Node.js, git, VS Code, and Claude Code.

**New to terminals?** Read [`00-what-is-a-terminal.md`](./00-what-is-a-terminal.md) first — it explains what all of this is and why you need it.

Commands below use `apt` (Debian/Ubuntu). For Fedora/RHEL, replace `apt` with `dnf`. For Arch, use `pacman`.

---

## 1. Update your package list

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 2. Install Git

```bash
sudo apt install git -y
```

Verify:

```bash
git --version
```

---

## 3. Install Node.js

Use the NodeSource setup script for a current LTS version. This command downloads a setup script from NodeSource (a trusted provider of Node.js packages) and runs it with administrator privileges (`sudo`). It configures your system to install a modern version of Node.js — the version bundled with most Linux distributions is often outdated.

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install nodejs -y
```

Verify:

```bash
node --version
npm --version
```

**Fedora:**
```bash
sudo dnf install nodejs -y
```

---

## 4. Install VS Code

**Debian/Ubuntu:**
```bash
sudo apt install wget gpg -y
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update
sudo apt install code -y
```

Or download the `.deb` directly from [code.visualstudio.com](https://code.visualstudio.com) and install with `sudo dpkg -i code_*.deb`.

See [04-ide-setup.md](./04-ide-setup.md) for recommended extensions.

---

## 5. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Then follow [02-claude-code.md](./02-claude-code.md) to authenticate.

---

## Troubleshooting

**"Permission denied" on npm install -g** — This happens because npm is trying to install files in a system folder your user doesn't own. The fix is to tell npm to use a folder inside your home directory instead. Run these four commands once, and the problem goes away permanently:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

What these do: (1) create a folder for global packages in your home directory, (2) tell npm to use it, (3) tell your terminal where to find programs installed there, (4) reload your terminal settings. After this, retry the npm install without `sudo`.

**Node version too old** — If your distro's default `apt` provides an outdated Node.js, use the NodeSource script above or [nvm](https://github.com/nvm-sh/nvm).

---

## You're Done When...

Run these three commands and confirm each prints a version number:

```bash
node --version
git --version
code --version
```

If all three respond with a version, your Linux setup is complete. Move on to [`02-claude-code.md`](./02-claude-code.md).

---

## Related

- [00-what-is-a-terminal.md](./00-what-is-a-terminal.md)
- [01-github.md](./01-github.md)
- [02-claude-code.md](./02-claude-code.md)
- [03-git-basics.md](./03-git-basics.md)
- [04-ide-setup.md](./04-ide-setup.md)
