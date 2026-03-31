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

### 5. Audit Secret Scanning Limitations

The `/hacky-hours audit` Phase 1 uses regex patterns to scan for secrets in uncommitted changes. This is a heuristic — it catches common patterns (`API_KEY=`, `password:`, etc.) but cannot detect:
- Secrets in committed history (use `git log -p | grep` or tools like `truffleHog` for that)
- Base64-encoded or otherwise obfuscated secrets
- Secrets in binary files

**Mitigation:** The audit explicitly states it's a heuristic check and recommends manual review of `git diff` before committing.

## Dependency Security

This project has no code dependencies — no `package.json`, no `requirements.txt`, no imports. The only external dependencies are:
- **Claude Code** (Anthropic's product) — the runtime environment
- **`gh` CLI** (optional) — for sync and issues commands
- **`git`** — for version control operations

## License Hygiene

MIT license. No dependency license conflicts possible (no dependencies). Users building products with this framework should manage their own license compatibility via `02-design/LICENSING.md`.
