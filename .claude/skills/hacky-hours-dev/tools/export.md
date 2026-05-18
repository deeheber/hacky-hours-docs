# /hacky-hours export <target> — export project docs for graduation

The graduation property in action: your project's docs are designed to migrate into a real team's knowledge base. This verb produces export-ready bundles.

## Targets

v4.0.0 ships two targets:

- **`markdown-bundle`** — single concatenated `.md` file ready to paste into Notion, Confluence, Obsidian, GitHub Discussions, anywhere that accepts markdown
- **`html-bundle`** — static HTML site (project-level equivalent of `/hacky-hours team site`)

API-based exporters (`notion`, `gdocs`, `confluence`) are designed but not implemented in v4.0.0. Track those in v4.1+.

## Step 0 — Pre-flight

1. **Project is adopted:** read `hacky-hours/NARRATIVE.md`. If absent, run `/hacky-hours adopt` first.
2. **Parse target argument:** `/hacky-hours export <target>`. If missing: list available targets and ask.

## Step 1 — Identify sources

Read in this order:
1. `README.md` at project root (if present)
2. `hacky-hours/01-ideate/PRODUCT_OVERVIEW.md` (and IDEATION.md if it makes sense)
3. All design docs in `hacky-hours/02-design/`:
   - Two-tier docs: prefer the `<DOC>-deep.md` version (source of truth), include `-summary.md` only if a separate summary is wanted
   - Single-tier docs: include as-is
4. `hacky-hours/03-roadmap/ROADMAP.md`
5. `hacky-hours/04-build/BACKLOG.md`, `CHANGELOG.md`
6. `hacky-hours/runbooks/*.md`
7. ADRs in `hacky-hours/02-design/decisions/`
8. Recent audits in `hacky-hours/audits/` (most recent only by default)

**Always exclude:**
- `hacky-hours/01-ideate/IDEATION.md` — raw free-writing, often messy
- `hacky-hours/adoption-assessment-*.md` — internal team-meeting notes, not team-grade output
- `hacky-hours/NARRATIVE.md`, `STATE.md`, `HANDOFFS.yml`, `VOICE.md` — operational state files
- `hacky-hours/.hacky-hours-denylist*`
- AGENTS.md, CLAUDE.md — framework-internal

Surface the inclusion list to the conductor for confirmation:

> *"Bundling these docs:*
> *  - README.md*
> *  - PRODUCT_OVERVIEW.md*
> *  - ARCHITECTURE.md (deep), summary*
> *  - <list each>*
>
> *Exclude or add anything?"*

Wait for confirmation. Allow the conductor to add or remove paths before proceeding.

## Step 2 — Target-specific generation

### Target: `markdown-bundle`

Concatenate all included docs into a single file at `hacky-hours/exports/<YYYY-MM-DD>-bundle.md`:

```markdown
# <Project name> — Documentation Bundle

Generated <date> by Hacky Hours v4.0.0.

This bundle contains the team-grade documentation for <project>. Paste into any
markdown-aware tool (Notion, Confluence, Obsidian, GitHub Discussions) — it's
designed to render cleanly without modification.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Security & Privacy](#security--privacy)
- ... <generate TOC from included docs' h1 headings>

---

<For each included doc, in source order:>

# <Doc title from h1 or frontmatter>

*Owner: <frontmatter owner>* · *Last reviewed: <date>* · *<status>*

<doc content with h1 demoted to h2 to preserve TOC structure>

---

```

Smart concatenation:
- **Demote heading levels by 1.** The bundle's TOC uses h2/h3 to break up sections; each included doc's existing headings become h2 or deeper.
- **Resolve relative-path image references.** If any doc references `./images/diagram.png`, copy the image into `hacky-hours/exports/<date>-bundle-assets/` and rewrite the path. (For v4.0.0: surface a warning if images can't be resolved; don't crash.)
- **Resolve cross-doc links.** A link like `[Security model](./SECURITY_PRIVACY.md)` becomes `[Security model](#security--privacy)` since they're now in the same document.
- **Strip private frontmatter fields** like `owner: <internal id>` from each section's metadata footer — but keep useful ones (last_reviewed, status).

After generation: print

> *"Bundle written to `hacky-hours/exports/<date>-bundle.md` (<size>, <line count>, <doc count> docs).*
> *Open it, copy-paste into your knowledge base. Drop into Notion/Confluence/GDocs as a single page or split into multiple by section.*
> *If you'd prefer HTML, run `/hacky-hours export html-bundle`."*

### Target: `html-bundle`

Project-level static site. Uses the same generator pattern as `/hacky-hours team site` but for project docs.

For v4.0.0: tell the conductor:

> *"`html-bundle` is in development. The recommended path right now: run `/hacky-hours export markdown-bundle` to get a single .md file, then push it through any static site generator you prefer (MkDocs, Hugo, Astro, 11ty). Or use `/hacky-hours team site` for the team-browser equivalent.*
>
> *Want to do that, or wait for native html-bundle?"*

If user wants to proceed manually: print the recommended setup for MkDocs (simplest):
```bash
pip install mkdocs mkdocs-material
mkdocs new my-project
# Copy hacky-hours/exports/<date>-bundle.md content into docs/index.md, OR
# Copy individual hacky-hours docs into docs/ folder structure
mkdocs serve   # localhost preview
mkdocs build   # generates static site to site/
```

If user wants to wait: just exit politely.

### Target: `notion` / `gdocs` / `confluence`

Print honestly:

> *"<Target> API integration is designed but not yet implemented in v4.0.0. Use `markdown-bundle` and paste manually for now — Notion and Confluence both accept clean markdown paste. Native integrations are tracked for v4.1+."*

## Step 3 — Update state

After successful export:
- Add a note to `hacky-hours/NARRATIVE.md`: *"Exported to <target> on <date>; bundle at <path>."*
- Update `STATE.md` `last_action`.

## Step 4 — Print confirmation

Brief, action-oriented:

> *"Export complete. Bundle at `<path>`.*
> *Suggested next step: paste into your team's knowledge base, OR commit `hacky-hours/exports/` to the repo so the artifact is preserved."*

## Notes for the assistant

- **Quality over completeness.** A 5-doc bundle that renders perfectly in Notion is better than a 15-doc bundle that includes operational state files Notion users don't need.
- **Surface conflicts honestly.** If a doc references a file that doesn't exist, flag it: *"<doc> references `images/foo.png` but that file doesn't exist. Skip the reference, leave broken, or fix the source doc?"*
- **The TOC matters.** A bundle without a clean TOC is hard to navigate in Notion. Generate it carefully from included doc headings.
- **Two-tier docs:** by default include only the `-deep.md` version (source of truth). Ask the conductor if they want both: *"Your ARCHITECTURE.md has a deep + summary pair — include both, or just the deep version?"*
