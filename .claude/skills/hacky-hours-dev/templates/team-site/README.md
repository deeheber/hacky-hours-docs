# Team site generator

A pure-Python static site generator for browsing your Hacky Hours team. Generates HTML directly from your team's `agents/*/profile.md` files — no npm, no Astro, no build dependencies beyond Python 3.

## Quick start

After your team is set up (`/hacky-hours team init`), this folder gets copied into your team repo at `~/.hacky-hours/teams/<team-name>/site/`. From there:

```bash
cd ~/.hacky-hours/teams/<team-name>/site/
python3 generate.py
```

Output lands in `~/.hacky-hours/teams/<team-name>/docs/`. Open `docs/index.html` in any browser — works from `file://`, no server needed.

For a local server (needed for cross-page navigation in some browsers, optional for basic browsing):

```bash
cd ~/.hacky-hours/teams/<team-name>/docs/
python3 -m http.server 8000
# Then open http://localhost:8000
```

For GitHub Pages: push the team repo, enable Pages in settings → "Deploy from a branch" → main, /docs folder.

## How it works

1. Reads `~/.hacky-hours/teams/<team-name>/README.md` for team-level frontmatter (name, tier, philosophy, established date).
2. Reads each agent's `profile.md` frontmatter (id, name, pronouns, hats, tagline, avatar, joined, specialties).
3. Generates `index.html` (roster grid) and `agents/<id>.html` (per-agent profile pages).
4. Drops a `style.css` with clean, mobile-friendly styling.

Pure Python stdlib — no PyYAML, no Jinja, nothing to install.

## Customizing

The styles live in `style.css` after generation; edit them to match your branding. The HTML templates live in `generate.py` as Python string constants — modify them and re-run.

For more substantial customization (different layouts, search, dynamic filtering), you can replace this generator entirely with Astro / Hugo / 11ty / whatever you prefer. The team repo's `agents/*/profile.md` files are the source data; any SSG that reads markdown+frontmatter can consume them.

## What's intentionally NOT in this generator (v4.0.0)

- Search (file:// browsers block fetch from local; would need a server)
- Dynamic role filtering (same reason)
- Agent history rendering (intentionally — those are private working notes)
- Feedback display (private)
- Image avatars (emoji only for v4.0.0; add image support by extending profile.md frontmatter)

These can be added in follow-on framework releases or by users customizing the generator.

## Per-field privacy

If you publish the site (GitHub Pages or anywhere else), respect each profile.md's `published:` frontmatter field:
- `published: true` (default) — the profile is included in the site
- `published: false` — the agent is skipped entirely

For history.md and feedback.md, the generator never reads them — they're never published. If you want certain history entries surfaced, copy them into the agent's profile.md "How I work" or "Background" section.
