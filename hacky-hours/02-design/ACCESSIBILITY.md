# ACCESSIBILITY.md

**Level 2 — Design** | hacky-hours-docs

---

## Scope

As of v1.8.0, this project now has UI artifacts — the generated Astro sites in `hacky-hours/learn/` (tour and quiz). Accessibility now covers both the documentation layer and the generated web layer.

For the generated web layer, the target standard is **WCAG 2.1 AA**. Astro generates semantic HTML by default; the interactive components (feedback form, quiz UI) need explicit accessibility evaluation before they can be considered done. This has not yet been performed.

For the documentation layer, accessibility means:

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

### v1.7.0 Voice Mode — Accessibility Rationale

The default voice mode is **non-technical** by design. This is an accessibility decision: non-technical users often don't know what signals to send to indicate their background, so they can't self-identify as needing plain-language explanations. Defaulting to accessible language ensures these users are never left behind. Engineers can opt in to technical mode explicitly via `/hacky-hours mode engineer`.

New terms from this feature to add to GLOSSARY.md:
- "voice mode" — the current conversation style setting for the framework assistant

### v1.8.0 New Commands — Accessibility Notes

- **`/hacky-hours learn tour`** — the generated Astro tour site has not yet been evaluated for WCAG 2.1 AA compliance. Known items to verify before launch: heading hierarchy in generated pages, keyboard navigation through tour sections, alt text on any diagrams rendered from Mermaid, and accessible markdown editor in the feedback form (focus management, label associations, error states).
- **`/hacky-hours learn onboard`** — conversation-only; no web UI. The GitHub Issue it creates should use plain-language titles and body text, not jargon. "Onboarding" label should be explained in the issue body for readers unfamiliar with the term.
- **`/hacky-hours learn quiz`** — the generated quiz site needs WCAG 2.1 AA evaluation. Key concerns: quiz answer interactions must be keyboard-accessible, score/feedback must be announced to screen readers (ARIA live regions), and question text must not rely on color alone to convey meaning.
- **`/hacky-hours upgrade`** — conversation-only; no web UI. Output should use plain language. The diff it produces (what's new vs. what you have) should be structured as a readable list, not a technical patch format.

New terms to add to GLOSSARY.md:
- "WCAG 2.1 AA" — already exists, but the entry should now mention it applies to the generated learn suite sites
- "Astro" — the static site generator used for the learn suite
- "onboarding" — in the GitHub context (labeled issues, structured starter tasks)

### Remaining Gaps (not blocking)

- No guidance for screen reader users navigating the framework's own docs
- No internationalization or non-English language support
- Shell-specific instructions (`.bashrc` vs `.zshrc`) could be clearer on macOS
- New terms from v1.5.0 (token, pivot, GitHub Issue, label) need GLOSSARY entries

## Related

- [GLOSSARY.md](../../GLOSSARY.md)
- [Getting Started Guides](../../runbooks/getting-started/)
