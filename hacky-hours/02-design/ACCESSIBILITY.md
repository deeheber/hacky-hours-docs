# ACCESSIBILITY.md

**Level 2 — Design** | hacky-hours-docs

---

## Scope

This project has no UI — it's entirely Markdown documentation read by humans and by Claude Code. Accessibility here means:

1. **Language accessibility** — clear, jargon-free writing that doesn't assume prior technical knowledge
2. **Document structure** — proper heading hierarchy, meaningful link text, logical reading order
3. **Inclusivity of entry points** — multiple getting-started paths for different skill levels and platforms

## Standards

- All documentation should be readable by someone with no programming experience
- Technical terms should be defined in `GLOSSARY.md` on first use
- Runbooks should cover zero-install paths (GitHub Codespaces) alongside full terminal setups
- Starter prompts should work for people who've never used a terminal before
- New commands should be explained in the help message and subcommand help before being referenced elsewhere

## Current State

Last full audit: 2026-03-21 (v1.3.0). Incremental review: 2026-03-30 (v1.5.0).

### Resolved

- **21 technical terms were used without glossary definitions** — all critical terms now added to GLOSSARY.md (ARIA, WCAG, OWASP, GDPR, CCPA, HIPAA, OAuth, MCP, copyleft, GPL, screen readers, symlink, submodule, tag, frontmatter, YAML, and more)
- **Linux setup assumes users know which package manager to use** (apt vs dnf vs pacman) — a known gap, acceptable since the guide names which distros use which
- **Git submodule advanced steps assume upstream/fetch/merge knowledge** — acceptable for the "Advanced" section, which targets experienced users
- **Command-line flags are not explained** — acceptable tradeoff; explaining every flag would overwhelm beginners who are copy-pasting

### v1.5.0 New Commands — Accessibility Notes

- **`/hacky-hours optimize`** — may produce technical output (token counts, staleness metrics, cross-reference maps). Recommendations section should use plain language. Term "token" should be in GLOSSARY.md.
- **`/hacky-hours pivot`** — uses metaphor ("pivot") that may not be obvious to non-business audiences. Help text explains it as "rethink product direction." Term should be in GLOSSARY.md.
- **`/hacky-hours sync --issues`** — introduces concepts (labels, issue linking, `#<number>` annotations) that assume GitHub familiarity. The command explains each step, but a GLOSSARY entry for "GitHub Issue" and "label" would help.

### Remaining Gaps (not blocking)

- No guidance for screen reader users navigating the framework's own docs
- No internationalization or non-English language support
- Shell-specific instructions (`.bashrc` vs `.zshrc`) could be clearer on macOS
- New terms from v1.5.0 (token, pivot, GitHub Issue, label) need GLOSSARY entries

## Related

- [GLOSSARY.md](../../GLOSSARY.md)
- [Getting Started Guides](../../runbooks/getting-started/)
