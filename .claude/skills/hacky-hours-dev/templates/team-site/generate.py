#!/usr/bin/env python3
"""
Hacky Hours team site generator.

Reads agent profile.md files from a team repo and generates a static HTML site.
Pure Python stdlib — no external dependencies. Output works via file:// or any static host.

Usage:
    python3 generate.py [--team-root <path>] [--out <path>]

Defaults:
    --team-root  the directory containing this script's parent (so when copied into
                 ~/.hacky-hours/teams/<team>/site/, it auto-resolves to the team root)
    --out        <team-root>/docs/

Run from the team repo's site/ folder:
    cd ~/.hacky-hours/teams/default/site/
    python3 generate.py

Then open docs/index.html in a browser, or:
    cd ../docs && python3 -m http.server 8000
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
from pathlib import Path

# ---- Minimal YAML frontmatter parser (no external deps) ---------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse simple YAML frontmatter. Returns (frontmatter_dict, body)."""
    if not text.startswith("---\n"):
        return {}, text

    end_match = re.search(r"\n---\n", text[4:])
    if not end_match:
        return {}, text

    fm_text = text[4:4 + end_match.start()]
    body = text[4 + end_match.end():]

    fm: dict = {}
    current_list_key: str | None = None
    current_list: list = []

    for raw_line in fm_text.split("\n"):
        if not raw_line.strip():
            continue
        # Top-level key: value
        m_kv = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", raw_line)
        if m_kv and not raw_line.startswith("  "):
            if current_list_key is not None:
                fm[current_list_key] = current_list
                current_list_key = None
                current_list = []
            key, value = m_kv.group(1), m_kv.group(2).strip()
            if value == "" or value == "[]":
                if value == "[]":
                    fm[key] = []
                else:
                    # value will come from following list items
                    current_list_key = key
                    current_list = []
            elif value.startswith("[") and value.endswith("]"):
                # Inline list: [a, b, c]
                inner = value[1:-1].strip()
                items = [s.strip().strip('"').strip("'") for s in inner.split(",") if s.strip()]
                fm[key] = items
            else:
                fm[key] = value.strip('"').strip("'")
        # List item (- value)
        elif raw_line.lstrip().startswith("- ") and current_list_key is not None:
            current_list.append(raw_line.lstrip()[2:].strip().strip('"').strip("'"))

    if current_list_key is not None:
        fm[current_list_key] = current_list

    return fm, body


# ---- Minimal markdown → HTML (just enough for profile bodies) ---------------

def md_to_html(text: str) -> str:
    """Bare-bones markdown converter. Handles headings, paragraphs, lists, bold, italic, code spans, links."""
    lines = text.split("\n")
    html_parts: list[str] = []
    in_list = False
    in_para_buf: list[str] = []

    def flush_para():
        nonlocal in_para_buf
        if in_para_buf:
            joined = " ".join(in_para_buf).strip()
            if joined:
                html_parts.append(f"<p>{inline(joined)}</p>")
            in_para_buf = []

    def inline(s: str) -> str:
        # Don't re-escape; assume input is already safe for code spans we need to escape.
        # Bold **x**
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        # Italic *x* (avoid lists)
        s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
        # Code spans
        s = re.sub(r"`([^`]+)`", lambda m: f"<code>{html.escape(m.group(1))}</code>", s)
        # Links [text](url)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    for line in lines:
        stripped = line.strip()
        h_match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if h_match:
            flush_para()
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            level = len(h_match.group(1))
            text_content = inline(h_match.group(2))
            html_parts.append(f"<h{level}>{text_content}</h{level}>")
        elif re.match(r"^[-*]\s+", line):
            flush_para()
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            item = re.sub(r"^[-*]\s+", "", line)
            html_parts.append(f"<li>{inline(item)}</li>")
        elif stripped == "":
            flush_para()
            if in_list:
                html_parts.append("</ul>")
                in_list = False
        elif stripped.startswith("---"):
            flush_para()
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append("<hr>")
        else:
            in_para_buf.append(line)

    flush_para()
    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)


# ---- HTML templates ---------------------------------------------------------

PAGE_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{stylesheet}">
</head>
<body>
<header>
  <a href="{home}" class="home-link">← Team</a>
  <span class="team-badge">{team_name}</span>
</header>
<main>
{content}
</main>
<footer>
  <p>Generated by Hacky Hours v4.0.0-dev · {framework_link}</p>
</footer>
</body>
</html>
"""

INDEX_INTRO = """
<section class="intro">
  <h1>{team_name}</h1>
  <p class="tagline">{philosophy}</p>
  <p class="meta">Tier: <strong>{tier}</strong> · {agent_count} agents · established {established}</p>
</section>
"""

CARD_TEMPLATE = """
<a href="agents/{id}.html" class="card">
  <div class="avatar">{avatar}</div>
  <div class="card-body">
    <h2>{name}</h2>
    <p class="role">{role}</p>
    <p class="tagline">{tagline}</p>
    <p class="hats">{hats}</p>
  </div>
</a>
"""

PROFILE_HEADER = """
<section class="profile-header">
  <div class="avatar large">{avatar}</div>
  <div>
    <h1>{name}</h1>
    <p class="pronouns">{pronouns}</p>
    <p class="role">{role}</p>
    <p class="tagline">{tagline}</p>
    <p class="meta">Hats: {hats} · Joined: {joined}</p>
    {specialties_section}
  </div>
</section>
"""


# ---- Generators -------------------------------------------------------------

def read_team_metadata(team_root: Path) -> dict:
    """Read team-level README.md frontmatter + tier.yml."""
    meta = {"name": "Untitled Team", "tier": "unknown", "philosophy": "", "established": "unknown"}
    readme = team_root / "README.md"
    if readme.exists():
        fm, _ = parse_frontmatter(readme.read_text())
        meta.update({k: v for k, v in fm.items() if v})
    return meta


def list_agents(team_root: Path) -> list[dict]:
    """Read all agent profile.md files; return list of frontmatter dicts (+ body)."""
    agents = []
    agents_dir = team_root / "agents"
    if not agents_dir.is_dir():
        return agents
    for agent_dir in sorted(agents_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        profile = agent_dir / "profile.md"
        if not profile.exists():
            continue
        text = profile.read_text()
        fm, body = parse_frontmatter(text)
        if fm.get("published", True) in (False, "false", "False"):
            continue
        fm["_body_html"] = md_to_html(body)
        fm["_dir_id"] = agent_dir.name
        # Fallback ID if frontmatter doesn't have one
        fm.setdefault("id", agent_dir.name)
        agents.append(fm)
    return agents


def role_label(agent: dict) -> str:
    hats = agent.get("hats") or []
    if isinstance(hats, str):
        hats = [hats]
    if not hats:
        return agent.get("id", "agent").replace("-", " ").title()
    return ", ".join(h.replace("-", " ").title() for h in hats)


def render_card(agent: dict) -> str:
    return CARD_TEMPLATE.format(
        id=html.escape(agent.get("id", "agent")),
        avatar=html.escape(agent.get("avatar", "🧑")),
        name=html.escape(agent.get("name", agent.get("id", "Agent"))),
        role=html.escape(role_label(agent)),
        tagline=html.escape(agent.get("tagline", "")),
        hats=html.escape(", ".join(agent.get("hats", []) if isinstance(agent.get("hats"), list) else [])),
    )


def render_profile_page(agent: dict, team_meta: dict) -> str:
    specialties = agent.get("specialties", [])
    if isinstance(specialties, str):
        specialties = [specialties]
    specialties_section = ""
    if specialties:
        items = "".join(f"<li>{html.escape(s)}</li>" for s in specialties)
        specialties_section = f"<p class=\"specialties\"><strong>Specialties:</strong></p><ul>{items}</ul>"

    header = PROFILE_HEADER.format(
        avatar=html.escape(agent.get("avatar", "🧑")),
        name=html.escape(agent.get("name", agent.get("id", "Agent"))),
        pronouns=html.escape(agent.get("pronouns", "")),
        role=html.escape(role_label(agent)),
        tagline=html.escape(agent.get("tagline", "")),
        hats=html.escape(", ".join(agent.get("hats", []) if isinstance(agent.get("hats"), list) else [])),
        joined=html.escape(agent.get("joined", "unknown")),
        specialties_section=specialties_section,
    )

    body = agent.get("_body_html", "")
    content = header + body

    return PAGE_SHELL.format(
        title=f"{agent.get('name', 'Agent')} — {team_meta.get('name', 'Team')}",
        stylesheet="../style.css",
        home="../index.html",
        team_name=html.escape(team_meta.get("name", "Team")),
        content=content,
        framework_link='<a href="https://github.com/empathetech/hacky-hours-docs">empathetech/hacky-hours-docs</a>',
    )


def render_index(team_meta: dict, agents: list[dict]) -> str:
    intro = INDEX_INTRO.format(
        team_name=html.escape(team_meta.get("name", "Team")),
        philosophy=html.escape(team_meta.get("philosophy", "")),
        tier=html.escape(team_meta.get("tier", "unknown")),
        agent_count=len(agents),
        established=html.escape(team_meta.get("established", "unknown")),
    )
    cards = "".join(render_card(a) for a in agents)
    grid = f'<section class="grid">{cards}</section>'
    content = intro + grid

    return PAGE_SHELL.format(
        title=team_meta.get("name", "Team"),
        stylesheet="style.css",
        home="index.html",
        team_name=html.escape(team_meta.get("name", "Team")),
        content=content,
        framework_link='<a href="https://github.com/empathetech/hacky-hours-docs">empathetech/hacky-hours-docs</a>',
    )


# ---- CSS --------------------------------------------------------------------

STYLE_CSS = """
:root {
  --bg: #faf9f5;
  --fg: #1a1a1a;
  --muted: #6b6b6b;
  --accent: #5b4dff;
  --card-bg: #ffffff;
  --card-border: #e6e3da;
  --shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.04);
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  background: var(--bg);
  color: var(--fg);
  line-height: 1.55;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--card-border);
  background: var(--card-bg);
}
.home-link { color: var(--accent); text-decoration: none; font-weight: 500; }
.home-link:hover { text-decoration: underline; }
.team-badge {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.85rem;
  color: var(--muted);
}
main {
  max-width: 980px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}
.intro h1 { font-size: 2.25rem; margin: 0 0 0.5rem 0; letter-spacing: -0.02em; }
.intro .tagline { color: var(--muted); font-size: 1.1rem; margin: 0.25rem 0 0.5rem; font-style: italic; }
.intro .meta { color: var(--muted); font-size: 0.95rem; margin-top: 0.5rem; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}
.card {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
  padding: 1rem 1.1rem;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  text-decoration: none;
  color: var(--fg);
  transition: transform 0.12s, box-shadow 0.12s, border-color 0.12s;
}
.card:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow);
  border-color: var(--accent);
}
.avatar {
  font-size: 2.25rem;
  line-height: 1;
  flex-shrink: 0;
}
.avatar.large { font-size: 4rem; }
.card-body { min-width: 0; }
.card h2 { margin: 0 0 0.15rem 0; font-size: 1.05rem; }
.card .role { color: var(--muted); font-size: 0.85rem; margin: 0 0 0.4rem 0; }
.card .tagline { font-size: 0.9rem; margin: 0; }
.card .hats { font-size: 0.75rem; color: var(--muted); margin: 0.35rem 0 0 0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.profile-header {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--card-border);
}
.profile-header h1 { margin: 0 0 0.25rem 0; font-size: 2rem; }
.profile-header .pronouns { color: var(--muted); font-size: 0.9rem; margin: 0; }
.profile-header .role { color: var(--accent); font-weight: 500; margin: 0.5rem 0 0.5rem 0; }
.profile-header .tagline { font-style: italic; margin: 0.5rem 0; color: var(--fg); }
.profile-header .meta { font-size: 0.85rem; color: var(--muted); margin: 0.75rem 0 0.5rem; }
.profile-header .specialties { margin: 0.75rem 0 0.25rem; font-size: 0.9rem; }
.profile-header ul { margin-top: 0.25rem; padding-left: 1.25rem; }
.profile-header li { font-size: 0.9rem; margin: 0.15rem 0; }
main h2 { font-size: 1.25rem; margin-top: 2rem; margin-bottom: 0.75rem; }
main h3 { font-size: 1.05rem; margin-top: 1.5rem; }
main p { margin: 0.75rem 0; }
main code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.9em;
  background: #f0eee5;
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
}
main ul { padding-left: 1.5rem; }
main li { margin: 0.25rem 0; }
main a { color: var(--accent); }
hr { border: none; border-top: 1px solid var(--card-border); margin: 1.5rem 0; }
footer {
  text-align: center;
  padding: 2rem 1rem;
  color: var(--muted);
  font-size: 0.85rem;
}
footer a { color: var(--muted); }
@media (max-width: 600px) {
  .profile-header { flex-direction: column; gap: 0.75rem; }
  .avatar.large { font-size: 3rem; }
}
"""


# ---- Main -------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Generate static team site from Hacky Hours team repo")
    p.add_argument("--team-root", type=Path, default=None, help="Team repo root (default: parent of this script's folder)")
    p.add_argument("--out", type=Path, default=None, help="Output directory (default: <team-root>/docs/)")
    args = p.parse_args()

    script_dir = Path(__file__).resolve().parent
    team_root = args.team_root.resolve() if args.team_root else script_dir.parent
    out_dir = args.out.resolve() if args.out else (team_root / "docs")

    if not (team_root / "agents").is_dir():
        print(f"Error: no agents/ folder at {team_root}. Is this a team repo?", file=sys.stderr)
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "agents").mkdir(parents=True, exist_ok=True)

    team_meta = read_team_metadata(team_root)
    agents = list_agents(team_root)

    # Write stylesheet
    (out_dir / "style.css").write_text(STYLE_CSS)

    # Write index
    (out_dir / "index.html").write_text(render_index(team_meta, agents))

    # Write per-agent pages
    for agent in agents:
        (out_dir / "agents" / f"{agent['id']}.html").write_text(render_profile_page(agent, team_meta))

    print(f"Generated site at {out_dir}/")
    print(f"  index.html — team roster ({len(agents)} agents)")
    print(f"  agents/    — per-agent profile pages")
    print(f"  style.css")
    print()
    print(f"Browse:")
    print(f"  Local file:  open {out_dir}/index.html")
    print(f"  Local serve: cd {out_dir} && python3 -m http.server 8000")
    print(f"  GitHub Pages: enable in repo settings → Deploy from branch / docs folder")


if __name__ == "__main__":
    main()
