# SECURITY_PRIVACY.md

**Level 2 — Design** | hacky-hours-docs

---

## Data Inventory

| Data Type | Why Collected | Where Stored | Retention Period |
|-----------|--------------|--------------|-----------------|
| None | N/A | N/A | N/A |

This framework collects zero user data. No analytics, no telemetry, no tracking, no accounts.

## Authentication and Access

Not applicable for the framework itself. However, two commands interact with authenticated external systems:

- **`/hacky-hours sync`** and **`/hacky-hours sync --issues`** — require `gh` CLI authenticated with a GitHub token. The token must have `repo` scope to create releases and issues. This token is managed by `gh auth` on the user's machine — the framework never reads or stores it directly.
- **`/hacky-hours link`** — writes `RELATED_REPOS.md` to another repo on the user's local filesystem. No authentication required, but the user must have write access to both directories.
- **`/hacky-hours onboard`** — optionally creates a GitHub Issue (requires `gh` CLI, same `repo` scope as `sync`). Also performs a `git add`, `git commit`, and `git push` to persist the feedback file — the only command in the framework that pushes to origin on the user's behalf.

## Risk Surface

### 1. Install Scripts (`curl | bash` / `irm | iex`)

The install scripts download a file from GitHub and write it to the user's `~/.claude/commands/` directory. This is a common pattern but carries inherent risk:
- Users should inspect the script before running it
- The script should be pinned to a known version/commit when possible
- A compromised GitHub account could serve a malicious script

**Mitigation:** The install scripts are minimal (< 20 lines each), easy to audit, and only write a single `.md` file. No elevated permissions are requested.

### 2. Slash Command Prompt Injection Surface

The slash command prompt is read by Claude Code as context. If a user's project contains adversarial content in files that Claude reads (e.g., a crafted `README.md` or `IDEATION.md`), it could attempt to influence Claude's behavior during a `/hacky-hours` session.

**Mitigation:** This is a general Claude Code risk, not specific to this framework. Users should be aware that Claude reads files they point it at.

### 3. GitHub API Surface (`sync` and `sync --issues`)

`/hacky-hours sync` creates git tags, pushes them, and creates GitHub Releases. `/hacky-hours sync --issues` creates/updates/closes GitHub Issues and creates labels. Both commands:
- Always confirm before taking any action
- Require the `gh` CLI to be pre-authenticated (the framework never handles credentials directly)
- Could create unintended public artifacts if the user confirms without reviewing

**Mitigation:** Every sync action shows a preview and requires explicit confirmation. The audit command is designed to run first as a safety check.

### 4. Cross-Repo File Writes (`link`)

`/hacky-hours link` writes `RELATED_REPOS.md` to both the current repo and another repo specified by the user. It could overwrite existing content in the other repo's `RELATED_REPOS.md`.

**Mitigation:** The command shows exactly what it will write to both repos and requires confirmation before writing. It appends sections rather than overwriting the file.

### 5. Automated Git Push (`onboard`)

`/hacky-hours onboard` is the first command that writes to the repo and pushes to origin on the user's behalf, without the user explicitly running git commands. This is a higher-trust operation than any prior command.

Risks:
- The feedback file (`feedback-<username>-<timestamp>.md`) contains user-written content. If the user includes sensitive information (API keys, passwords, private details) in their feedback, it will be committed and pushed to the repo — including any public repos.
- The push happens at wrap-up after the user has confirmed the session is complete. If the user's working tree has uncommitted changes, the command should stage only the feedback file — never `git add -A`.

**Mitigation:** The command must: (1) show the exact content of the feedback file before committing, (2) stage only `hacky-hours/feedback/<filename>` explicitly, (3) confirm before pushing, (4) warn if the repo is public that the feedback will be visible.

### 6. User-Generated Content in Feedback Files

Feedback files committed to the repo become part of git history permanently. Unlike other hacky-hours artifacts (which are written by Claude based on user input), feedback files may contain freeform user text entered directly into a markdown editor.

**Mitigation:** The audit command's secret scanning (Phase 1) should also scan `hacky-hours/feedback/` for common secret patterns before any sync or release operation.

### 7. Astro Site Generation and Node.js Dependency

As of v1.8.0, static site generation introduces Node.js as an optional runtime dependency. The generated Astro projects in `hacky-hours/learn/` include a `package.json` and `node_modules/` (after install).

Risks:
- `node_modules/` must not be committed — add to `.gitignore` at the Astro project level
- Astro and its dependencies introduce a supply chain surface that did not previously exist
- The interactive features (feedback form, quiz UI) use client-side JavaScript

**Mitigation:** Generated Astro projects include a `.gitignore` that excludes `node_modules/` and build output. The `hacky-hours/learn/` folder itself is in `.claudeignore` to prevent generated assets from loading into Claude context. Node.js is checked before site generation; the command degrades gracefully to conversation mode if unavailable.

### 8. Audit Secret Scanning Limitations

The `/hacky-hours audit` Phase 1 uses regex patterns to scan for secrets in uncommitted changes. This is a heuristic — it catches common patterns (`API_KEY=`, `password:`, etc.) but cannot detect:
- Secrets in committed history (use `git log -p | grep` or tools like `truffleHog` for that)
- Base64-encoded or otherwise obfuscated secrets
- Secrets in binary files

**Mitigation:** The audit explicitly states it's a heuristic check and recommends manual review of `git diff` before committing.

## Dependency Security

The framework itself has no code dependencies. External dependencies:
- **Claude Code** (Anthropic's product) — the runtime environment
- **`gh` CLI** (optional) — for sync, issues, and onboard commands
- **`git`** — for version control operations
- **Node.js + Astro** (optional, v1.8.0+) — for static site generation in the learn suite. Only required if the user opts into site generation; conversation mode has no Node.js dependency.

## License Hygiene

MIT license. No dependency license conflicts possible (no dependencies). Users building products with this framework should manage their own license compatibility via `02-design/LICENSING.md`.
