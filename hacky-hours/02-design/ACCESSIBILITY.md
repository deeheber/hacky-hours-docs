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

## Current State

Audited 2026-03-21. Key findings and actions taken:

- **21 technical terms were used without glossary definitions** — all critical terms now added to GLOSSARY.md (ARIA, WCAG, OWASP, GDPR, CCPA, HIPAA, OAuth, MCP, copyleft, GPL, screen readers, symlink, submodule, tag, frontmatter, YAML, and more)
- **Linux setup assumes users know which package manager to use** (apt vs dnf vs pacman) — a known gap, acceptable since the guide names which distros use which
- **Git submodule advanced steps assume upstream/fetch/merge knowledge** — acceptable for the "Advanced" section, which targets experienced users
- **Command-line flags are not explained** — acceptable tradeoff; explaining every flag would overwhelm beginners who are copy-pasting

**Remaining gaps (not blocking):**
- No guidance for screen reader users navigating the framework's own docs
- No internationalization or non-English language support
- Shell-specific instructions (`.bashrc` vs `.zshrc`) could be clearer on macOS

## Related

- [GLOSSARY.md](../../GLOSSARY.md)
- [Getting Started Guides](../../runbooks/getting-started/)
