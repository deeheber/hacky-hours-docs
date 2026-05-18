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


# ---- Metrics block extractor (Slice 13) -------------------------------------

def extract_metrics(fm_text: str) -> dict:
    """Pull the metrics: block out of frontmatter text and parse 1 level deep.
    Returns empty dict if no metrics block found."""
    # Find the metrics: line and the contiguous indented block after it
    lines = fm_text.split("\n")
    metrics: dict = {}
    in_metrics = False
    for line in lines:
        if not in_metrics:
            if re.match(r"^metrics:\s*$", line):
                in_metrics = True
            continue
        # Stop on first un-indented line or empty-then-something line
        if line and not line.startswith("  "):
            break
        if not line.strip():
            continue
        # Parse "  key: value" (2-space indent)
        m = re.match(r"^  ([a-zA-Z_][\w-]*):\s*(.*)$", line)
        if not m:
            # 4-space indent = nested sub-dict (by_verb). Skip — we don't render those.
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == "" or value == "[]":
            metrics[key] = [] if value == "[]" else None
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            metrics[key] = [s.strip().strip('"').strip("'") for s in inner.split(",") if s.strip()]
        elif value in ("null", "~"):
            metrics[key] = None
        else:
            stripped = value.strip('"').strip("'")
            try:
                metrics[key] = int(stripped)
            except ValueError:
                metrics[key] = stripped
    return metrics


def read_history(agent_dir: Path, limit: int = 10) -> list[dict]:
    """Read history.md (and history-archive/*.md if present); return last N parsed entries.
    Returns newest-first. Each entry: {date, project, verb, summary, backfilled}."""
    history_file = agent_dir / "history.md"
    if not history_file.exists():
        return []
    text = history_file.read_text()
    # Match structured entry lines: "- YYYY-MM-DD · project · verb · summary"
    entries: list[dict] = []
    line_re = re.compile(r"^-\s+(\d{4}-\d{2}-\d{2})\s+·\s+([^·]+?)\s+·\s+([^·]+?)\s+·\s+(.+)$")
    for line in text.split("\n"):
        m = line_re.match(line.strip())
        if not m:
            continue
        date, project, verb, summary = m.group(1), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()
        backfilled = "(backfilled" in verb or "(backfilled" in summary
        # Clean the "(backfilled, anchor)" annotation from verb display
        verb_display = re.sub(r"\s*\(backfilled[^)]*\)", "", verb).strip()
        entries.append({
            "date": date,
            "project": project,
            "verb": verb_display,
            "summary": summary,
            "backfilled": backfilled,
        })
    # Sort newest-first by date string (ISO dates sort lexicographically)
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries[:limit]


def read_feedback(agent_dir: Path, limit: int = 5) -> list[str]:
    """Read feedback.md and return up to N durable notes as raw strings.
    Skips the boilerplate intro that ships with the template."""
    feedback_file = agent_dir / "feedback.md"
    if not feedback_file.exists():
        return []
    text = feedback_file.read_text()
    # Skip everything before the first "- " bullet or numbered list item
    # If file only contains the template placeholder, return empty
    if "No feedback yet" in text:
        return []
    notes: list[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- ") or re.match(r"^\d+\.\s+", stripped):
            content = re.sub(r"^(-\s+|\d+\.\s+)", "", stripped)
            if content:
                notes.append(content)
    return notes[:limit]


def read_resume(agent_dir: Path) -> str | None:
    """Read resume.md if it exists. Returns the markdown body (frontmatter stripped) or None."""
    resume_file = agent_dir / "resume.md"
    if not resume_file.exists():
        return None
    text = resume_file.read_text()
    _, body = parse_frontmatter(text)
    return body if body.strip() else None


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
  <a href="{home}" class="home-link">← {home_label}</a>
  <span class="team-badge">{team_name}</span>
</header>
<main>
{content}
</main>
<footer>
  <p>Generated by Hacky Hours v4.0.0 · {framework_link}</p>
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
    {metrics_badge}
  </div>
</a>
"""

# Slice 13 — metrics badge for cards. Hidden when level=0 (no history yet — keeps grid clean for fresh teams).
METRICS_BADGE_TEMPLATE = """
    <p class="metrics-badge">
      <span class="level">lvl {level}</span>
      <span class="contributions">{history_entries} contribution{plural}</span>{projects_clause}
    </p>
"""

PROFILE_HEADER = """
<section class="profile-header">
  <div class="avatar large">{avatar}</div>
  <div>
    <h1>{name}</h1>
    <p class="pronouns">{pronouns}</p>
    <p class="role">{role}</p>
    <p class="tagline">{tagline}</p>
    <p class="meta">Hats: {hats} · Joined: {joined}{metrics_clause}</p>
    {specialties_section}
    {resume_link}
  </div>
</section>
"""

# Slice 13 — Recent track record section on profile pages
TRACK_RECORD_SECTION = """
<section class="track-record">
  <h2>Recent track record</h2>
  <p class="section-meta">Latest {count} of {total} contribution{plural} · last active {last_active}</p>
  <ul class="history-list">
{entries}
  </ul>
</section>
"""

HISTORY_ENTRY_TEMPLATE = """    <li class="history-entry">
      <span class="date">{date}</span>
      <span class="project-verb"><code>{project}</code> · <code>{verb}</code></span>
      <span class="summary">{summary}</span>
    </li>"""

# Slice 13 — Lessons applied (from feedback.md) on profile pages
LESSONS_SECTION = """
<section class="lessons">
  <h2>Lessons applied</h2>
  <p class="section-meta">Durable corrections this agent has internalized from conductor feedback.</p>
  <ul class="lessons-list">
{items}
  </ul>
</section>
"""

# Slice 13 — Resume link section
RESUME_LINK_TEMPLATE = """    <p class="resume-link"><a href="{id}-resume.html">📄 Read full résumé →</a></p>"""


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
    """Read all agent profile.md files; return list of frontmatter dicts (+ body + Slice 13 history/feedback/resume)."""
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
        # Slice 13: parse the metrics block and gather history/feedback/resume
        # extract_metrics reads the raw frontmatter text directly (parse_frontmatter
        # is flat-only by design — keeping it that way for backwards compatibility)
        end_match = re.search(r"\n---\n", text[4:]) if text.startswith("---\n") else None
        if end_match:
            fm_text = text[4:4 + end_match.start()]
            fm["_metrics"] = extract_metrics(fm_text)
        else:
            fm["_metrics"] = {}
        fm["_history"] = read_history(agent_dir, limit=10)
        fm["_history_total"] = fm["_metrics"].get("history_entries", len(fm["_history"]))
        fm["_feedback"] = read_feedback(agent_dir, limit=5)
        fm["_resume_body"] = read_resume(agent_dir)
        agents.append(fm)
    return agents


def role_label(agent: dict) -> str:
    hats = agent.get("hats") or []
    if isinstance(hats, str):
        hats = [hats]
    if not hats:
        return agent.get("id", "agent").replace("-", " ").title()
    return ", ".join(h.replace("-", " ").title() for h in hats)


def render_metrics_badge(metrics: dict) -> str:
    """Slice 13 — small badge on cards showing level + contributions + projects.
    Returns empty string for level-0/no-history agents (keeps fresh team grids clean)."""
    level = metrics.get("level", 0) or 0
    history_entries = metrics.get("history_entries", 0) or 0
    if level == 0 and history_entries == 0:
        return ""
    projects = metrics.get("projects", []) or []
    projects_clause = ""
    if isinstance(projects, list) and len(projects) > 0:
        projects_clause = f' · <span class="projects">{len(projects)} project{"s" if len(projects) != 1 else ""}</span>'
    return METRICS_BADGE_TEMPLATE.format(
        level=level,
        history_entries=history_entries,
        plural="s" if history_entries != 1 else "",
        projects_clause=projects_clause,
    )


def render_metrics_clause(metrics: dict) -> str:
    """Slice 13 — inline metrics line on profile header."""
    level = metrics.get("level", 0) or 0
    history_entries = metrics.get("history_entries", 0) or 0
    if history_entries == 0:
        return ""
    return f" · Level {level} · {history_entries} contribution{'s' if history_entries != 1 else ''}"


def render_track_record(agent: dict) -> str:
    """Slice 13 — Recent track record section (from history.md)."""
    history = agent.get("_history") or []
    if not history:
        return ""
    total = agent.get("_history_total", len(history))
    metrics = agent.get("_metrics", {}) or {}
    last_active = metrics.get("last_active") or history[0]["date"]
    entry_html = "\n".join(
        HISTORY_ENTRY_TEMPLATE.format(
            date=html.escape(e["date"]),
            project=html.escape(e["project"]),
            verb=html.escape(e["verb"]),
            summary=html.escape(e["summary"]),
        )
        for e in history
    )
    return TRACK_RECORD_SECTION.format(
        count=len(history),
        total=total,
        plural="s" if total != 1 else "",
        last_active=html.escape(str(last_active)),
        entries=entry_html,
    )


def render_lessons(agent: dict) -> str:
    """Slice 13 — Lessons applied section (from feedback.md)."""
    notes = agent.get("_feedback") or []
    if not notes:
        return ""
    items = "\n".join(f"    <li>{html.escape(n)}</li>" for n in notes)
    return LESSONS_SECTION.format(items=items)


def render_card(agent: dict) -> str:
    return CARD_TEMPLATE.format(
        id=html.escape(agent.get("id", "agent")),
        avatar=html.escape(agent.get("avatar", "🧑")),
        name=html.escape(agent.get("name", agent.get("id", "Agent"))),
        role=html.escape(role_label(agent)),
        tagline=html.escape(agent.get("tagline", "")),
        hats=html.escape(", ".join(agent.get("hats", []) if isinstance(agent.get("hats"), list) else [])),
        metrics_badge=render_metrics_badge(agent.get("_metrics", {}) or {}),
    )


def render_profile_page(agent: dict, team_meta: dict) -> str:
    specialties = agent.get("specialties", [])
    if isinstance(specialties, str):
        specialties = [specialties]
    specialties_section = ""
    if specialties:
        items = "".join(f"<li>{html.escape(s)}</li>" for s in specialties)
        specialties_section = f"<p class=\"specialties\"><strong>Specialties:</strong></p><ul>{items}</ul>"

    resume_link = ""
    if agent.get("_resume_body"):
        resume_link = RESUME_LINK_TEMPLATE.format(id=html.escape(agent.get("id", "agent")))

    header = PROFILE_HEADER.format(
        avatar=html.escape(agent.get("avatar", "🧑")),
        name=html.escape(agent.get("name", agent.get("id", "Agent"))),
        pronouns=html.escape(agent.get("pronouns", "")),
        role=html.escape(role_label(agent)),
        tagline=html.escape(agent.get("tagline", "")),
        hats=html.escape(", ".join(agent.get("hats", []) if isinstance(agent.get("hats"), list) else [])),
        joined=html.escape(agent.get("joined", "unknown")),
        metrics_clause=render_metrics_clause(agent.get("_metrics", {}) or {}),
        specialties_section=specialties_section,
        resume_link=resume_link,
    )

    body = agent.get("_body_html", "")
    # Slice 13: append track record + lessons after the bio body
    track_record = render_track_record(agent)
    lessons = render_lessons(agent)
    content = header + body + track_record + lessons

    return PAGE_SHELL.format(
        title=f"{agent.get('name', 'Agent')} — {team_meta.get('name', 'Team')}",
        stylesheet="../style.css",
        home="../index.html",
        home_label="Team",
        team_name=html.escape(team_meta.get("name", "Team")),
        content=content,
        framework_link='<a href="https://github.com/empathetech/hacky-hours-docs">empathetech/hacky-hours-docs</a>',
    )


def render_resume_page(agent: dict, team_meta: dict) -> str:
    """Slice 13 — render agents/<id>-resume.html if resume.md exists for the agent."""
    body_md = agent.get("_resume_body") or ""
    body_html = md_to_html(body_md)
    content = f'<section class="resume-page">{body_html}</section>'
    return PAGE_SHELL.format(
        title=f"{agent.get('name', 'Agent')} — Résumé — {team_meta.get('name', 'Team')}",
        stylesheet="../style.css",
        home=f"{agent.get('id', 'agent')}.html",
        home_label="Profile",
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
        home_label="Team",
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

/* Slice 13 — metrics badge, track record, lessons, resume link */
.metrics-badge {
  font-size: 0.72rem;
  color: var(--muted);
  margin: 0.35rem 0 0 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  letter-spacing: 0.02em;
}
.metrics-badge .level {
  background: var(--accent);
  color: white;
  padding: 0.08rem 0.42rem;
  border-radius: 4px;
  margin-right: 0.4rem;
  font-weight: 600;
}
.metrics-badge .contributions,
.metrics-badge .projects { color: var(--muted); }

.profile-header .meta { font-variant-numeric: tabular-nums; }
.resume-link {
  margin: 0.85rem 0 0 0;
  font-size: 0.95rem;
}
.resume-link a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}
.resume-link a:hover { text-decoration: underline; }

.section-meta {
  color: var(--muted);
  font-size: 0.85rem;
  margin: 0.2rem 0 0.85rem 0;
  font-style: italic;
}

.track-record { margin-top: 2.5rem; }
.history-list {
  list-style: none;
  padding-left: 0;
  margin: 0.5rem 0;
  border-left: 2px solid var(--card-border);
}
.history-entry {
  display: grid;
  grid-template-columns: 6.5rem 1fr;
  gap: 0.5rem 1rem;
  padding: 0.7rem 0 0.7rem 1rem;
  border-bottom: 1px solid var(--card-border);
}
.history-entry:last-child { border-bottom: none; }
.history-entry .date {
  color: var(--muted);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.82rem;
  font-variant-numeric: tabular-nums;
}
.history-entry .project-verb {
  grid-column: 2;
  font-size: 0.78rem;
  color: var(--muted);
  margin-bottom: 0.2rem;
}
.history-entry .project-verb code {
  font-size: 0.72rem;
  padding: 0.05rem 0.3rem;
}
.history-entry .summary {
  grid-column: 2;
  font-size: 0.95rem;
}

.lessons { margin-top: 2.5rem; }
.lessons-list {
  list-style: none;
  padding-left: 0;
  margin: 0.5rem 0;
}
.lessons-list li {
  padding: 0.6rem 0.9rem;
  background: var(--card-bg);
  border-left: 3px solid var(--accent);
  margin: 0.5rem 0;
  border-radius: 0 6px 6px 0;
  font-size: 0.92rem;
}

.resume-page { padding: 0.5rem 0 2rem; }
.resume-page h1 { margin-top: 0; }
.resume-page h2 {
  margin-top: 2rem;
  padding-bottom: 0.35rem;
  border-bottom: 1px solid var(--card-border);
}
.resume-page blockquote {
  font-style: italic;
  color: var(--muted);
  border-left: 3px solid var(--accent);
  padding-left: 0.9rem;
  margin: 1rem 0;
}

@media (max-width: 600px) {
  .profile-header { flex-direction: column; gap: 0.75rem; }
  .avatar.large { font-size: 3rem; }
  .history-entry { grid-template-columns: 1fr; }
  .history-entry .project-verb,
  .history-entry .summary { grid-column: 1; }
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
    resumes_written = 0
    for agent in agents:
        (out_dir / "agents" / f"{agent['id']}.html").write_text(render_profile_page(agent, team_meta))
        # Slice 13: also render a resume page if resume.md exists
        if agent.get("_resume_body"):
            (out_dir / "agents" / f"{agent['id']}-resume.html").write_text(render_resume_page(agent, team_meta))
            resumes_written += 1

    print(f"Generated site at {out_dir}/")
    print(f"  index.html — team roster ({len(agents)} agents)")
    print(f"  agents/    — per-agent profile pages")
    if resumes_written:
        print(f"  agents/    — plus {resumes_written} résumé page(s) (from agents/<id>/resume.md)")
    print(f"  style.css")
    print()
    print(f"Browse:")
    print(f"  Local file:  open {out_dir}/index.html")
    print(f"  Local serve: cd {out_dir} && python3 -m http.server 8000")
    print(f"  GitHub Pages: enable in repo settings → Deploy from branch / docs folder")


if __name__ == "__main__":
    main()
