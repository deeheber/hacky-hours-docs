# SECURITY_PRIVACY.md

**Level 2 — Design** | hacky-hours-docs

---

## Data Inventory

| Data Type | Why Collected | Where Stored | Retention Period |
|-----------|--------------|--------------|-----------------|
| None | N/A | N/A | N/A |

This framework collects zero user data. No analytics, no telemetry, no tracking, no accounts.

## Authentication and Access

Not applicable. There is no backend, no API, no user accounts. The GitHub repository is public. The slash command runs locally within the user's Claude Code session.

## Risk Surface

Despite being a documentation-only project, there are two meaningful risk areas:

### 1. Install Scripts (`curl | bash` / `irm | iex`)

The install scripts download a file from GitHub and write it to the user's `~/.claude/commands/` directory. This is a common pattern but carries inherent risk:
- Users should inspect the script before running it
- The script should be pinned to a known version/commit when possible
- A compromised GitHub account could serve a malicious script

**Mitigation:** The install scripts are minimal (< 20 lines each), easy to audit, and only write a single `.md` file. No elevated permissions are requested.

### 2. Slash Command Prompt Injection Surface

The slash command prompt is read by Claude Code as context. If a user's project contains adversarial content in files that Claude reads (e.g., a crafted `README.md` or `IDEATION.md`), it could attempt to influence Claude's behavior during a `/hacky-hours` session.

**Mitigation:** This is a general Claude Code risk, not specific to this framework. Users should be aware that Claude reads files they point it at.

## Dependency Security

This project has no code dependencies — no `package.json`, no `requirements.txt`, no imports. The only external dependency is Claude Code itself (Anthropic's product) and `gh` CLI (optional, for `/hacky-hours sync`).

## License Hygiene

MIT license. No dependency license conflicts possible (no dependencies). Users building products with this framework should manage their own license compatibility via `02-design/LICENSING.md`.
