# ADR: Browser companion — local static workspace with Slack-style team chat

**Date:** 2026-05-22
**Status:** Accepted
**Slice:** v4.1.0 Tier 3 (T3.0–T3.9)
**Issue:** empathetech/hacky-hours-docs#8 (with owner addition for §4.29)
**Arbitration mode:** decide

## Context

V4.0.0 is terminal-only. For non-engineers, this is the friction point — not because the conversational interface is wrong, but because:

- Markdown artifacts (ERDs, design docs, roster, audit scorecards) are clunky to read in a scrollback.
- Repetitive structured input (design-doc Q&A) burns turns and is hard to track.
- Visibility into the team and project state requires reading raw files.
- Mermaid diagrams don't render in the terminal.
- The team as a *team* is invisible — agents are sentences in transcripts, not people you can scroll back to.

#8 originally proposed eight surfaces. During this iterate cycle, the owner added a ninth: a **Slack-style team chat surface** (workspaces = projects, channels = sessions, messages = workroom turns + status updates, with per-agent pixel-art avatars). The addition is load-bearing — it elegantly solves several #11 problems (transcript vs. digest, "show your work," status-update artifact, "team feels like consultants not coworkers").

**Hard constraint: zero additional API spend.** Users pay only for their existing Claude Code subscription. The browser companion never talks to an LLM.

## Roles involved

- **🏗️ Priya (Architect)** — single source of truth (Markdown / JSONL on disk) consumed by terminal + browser. No round-trip; browser is a derivative renderer.
- **🎨 Felix (Design)** — Slack-style chat surface is the headline of v4.1.0. Per-agent pixel-art identity is the key trick that makes the team *feel* like a team. Recognition matters.
- **♿ Lena (Accessibility)** — WCAG 2.1 AA baseline. Keyboard nav, color-contrast, semantic landmarks. Pixel-art avatars need text alternatives (alt text = name + role).
- **🛡️ Alex (Security)** — local-only filesystem, no third-party JS, no CDN dependencies, no LLM round-trips. Threat surface is narrow: a compromised browser companion could only display content already on disk.
- **🚀 Jordan (Ops)** — pure Python stdlib generator + vendored static deps means no `npm install` step, no Node.js dependency, no build pipeline. Works offline. Single command produces the artifact tree.
- **📈 Yuki (Data)** — `messages.jsonl` is the canonical conversation store; the chat surface is the canonical render. JSONL lets `jq` / streaming consumers reuse the data.
- **📜 Diego (Licensing)** — vendored deps (Mermaid, optional HTMX, pixel fonts) must be license-compatible with MIT and properly attributed.

## Decision

### 1. Architecture

Pure-Python static-HTML generator (no npm, no Node) extending the existing `tools/team-site.md` pattern. Three modes:

- **`build`** — produce a static site at `~/.hacky-hours/companion/<project-slug>/`. Idempotent; safe to re-run.
- **`serve`** — `build` + start `python3 -m http.server` on a configurable port. For read-only viewing.
- **`serve --writeback`** — `serve` + a thin POST endpoint (~50 lines) for form submissions and backlog reordering. Writes back to `pending-input.json` files that the framework consumes on the next session.

Generated tree:

```
~/.hacky-hours/companion/
├── index.html                  # workspace switcher (lists projects + team)
├── static/                     # vendored CSS, vendored Mermaid, optional HTMX, fonts
└── workspaces/
    └── <project-slug>/
        ├── home.html           # surface 1: dashboard
        ├── team/               # surface 2: team browser (extends existing `team site`)
        ├── project/            # surface 3: project workspace (01-ideate, 02-design, etc.)
        ├── forms/              # surface 4: schema-aware fillable forms
        ├── backlog.html        # surface 5: kanban
        ├── audits/             # surface 6: traffic-light timeline
        ├── diagrams.html       # surface 7: diagram gallery (Mermaid)
        ├── chat/               # surface 8: Slack-style chat (NEW per A3.1)
        └── monitor.html        # surface 9: session monitor (tails pending/ + history)
```

### 2. The nine surfaces

Each is one HTML page (or page-set) generated from on-disk content:

1. **Home (`home.html`)** — active project + team, recent activity from `git log` + `CHANGELOG`, "what's next" from BACKLOG top item.
2. **Team browser (`team/`)** — extends existing static site. Roster, per-agent profile + history + resume + system prompt, cross-team compare.
3. **Project workspace (`project/`)** — left rail nav through `01-ideate/` → `05-iterate/`, main panel renders Markdown with inline Mermaid, "edit in your editor" deep-links via `file://` or `vscode://`.
4. **Forms (`forms/`)** — schema-aware fillable forms for PRODUCT_OVERVIEW 5Ws, Constraints & Values, ARCHITECTURE quickstart. Submission writes to `pending-input.json`. Feature-flagged via `features.forms_writeback`.
5. **Backlog (`backlog.html`)** — kanban view (Next milestone / Backlog / Done-from-CHANGELOG). Drag-to-reorder writes back to `BACKLOG.md`. Feature-flagged via `features.backlog_writeback`.
6. **Audit timeline (`audits/`)** — traffic-light scorecards rendered visually, trend over time, drill-down to findings.
7. **Diagram gallery (`diagrams.html`)** — every ERD, architecture diagram, user-journey flowchart in one Mermaid render. Click-to-expand.
8. **Slack-style chat (`chat/`)** — see §3 below. Headline of v4.1.0.
9. **Session monitor (`monitor.html`)** — tails the current session's `pending/` directory and recent `history.md` appends. Feature-flagged via `features.session_monitor`. Auto-refresh via `<meta refresh>` or HTMX poll.

### 3. The Slack-style chat surface (NEW)

**Workspace = project.** Per workspace, the chrome shows a sidebar of available workspaces (multi-project switcher per `~/.hacky-hours/projects.yml`).

**Channels = sessions.** Each `~/.hacky-hours/sessions/<session-id>/` becomes a channel. Channel name derived from session metadata: `#<verb>-<project-slug>-<date>` (e.g., `#design-reciprocator-may19`). Channel description: one-sentence summary from the session's first turn or `ITERATION.md` lead.

**Messages = `messages.jsonl` rows.** Rendered chronologically. Per-message:

- **Avatar:** 24×24 pixel-art PNG from `agents/<id>/avatar.png` (bootstrap-generated; see §5 below).
- **Header:** `<emoji> <Name> · <Role>` (e.g., `🏗️ Priya Chen · Architect`).
- **Body:** Markdown rendered.
- **Timestamp:** relative + absolute on hover.
- **Per-agent accent color:** subtle left border or message-bubble tint, sourced from `agents/<id>/profile.md` frontmatter (or derived deterministically from agent ID if unset).

**Threads emerge from `in_reply_to`.** When a turn references a prior turn, the chat surface renders it as a threaded reply (Slack-style indent).

**Read-only.** No write-back. The companion never injects messages into a conversation — it only renders what the framework already produced. (Owner notes via `/hacky-hours redirect` are written by the framework on the owner's behalf; the chat surface just renders the resulting message.)

**Search.** Browser-native Cmd-F is sufficient at MVP. V1+: a pre-built JSON index for cross-channel search; rendered client-side without a search server.

**Persistence.** Conversations don't expire. Old channels stay browsable. The session folder is the source of truth.

### 4. Multi-workspace switcher

`~/.hacky-hours/projects.yml` is the workspace index:

```yaml
projects:
  - slug: reciprocator
    path: /Users/bjamba/code/github/bjamba/reciprocator
    team: default
    last_active: 2026-05-19T...
  - slug: hacky-hours-docs
    path: /Users/bjamba/code/github/empathetech/hacky-hours-docs/hacky-hours
    team: default
    last_active: 2026-05-22T...
```

Populated automatically when `/hacky-hours adopt` or `/hacky-hours ideate` runs in a new project directory. The companion's left chrome lists workspaces; clicking one switches the active workspace.

### 5. Pixel-art avatar bootstrap

Per-agent 24×24 (or 32×32) pixel-art PNG, generated **once** at team-init time:

- **When:** during default team bootstrap (per `tools/team.md` Step 1) or `team avatars` opt-in verb.
- **How:** one-shot LLM pass per agent — generates SVG that's rasterized to PNG, or directly generates PNG-encodable pixel grid. Stored at `~/.hacky-hours/teams/<name>/agents/<id>/avatar.png`. Counts as install cost, not per-use cost.
- **Style:** palette informed by role (e.g., security in muted slate, design in warm pastel, ops in toolbox-industrial). Consistent style across the roster — same generator pass for all 12 agents.
- **Fallback:** if generation fails (no network, no API), the chat surface uses an emoji + name initials as a placeholder. Avatar can be regenerated later via `/hacky-hours team avatars`.

Pixel-art generator spec lives in `tools/team-avatars.md` (to be authored as part of T3.4).

### 6. Handoff patterns back to Claude

Three patterns for write-back from the browser to the conversation:

1. **Clipboard handoff** (MVP) — "Send to Claude" button copies a slash command to clipboard; user pastes in terminal. Zero coordination, dead simple. Works for forms.
2. **Pending-input file** — form submissions write to `~/.hacky-hours/sessions/<id>/pending-input.json`; next Claude turn checks at preamble time, like behavior feedback already does. Same pattern, well-tested.
3. **Marker-file polling** (stretch / V1+) — Claude's session loop watches a marker file, picks up structured commands. More magic, more failure modes — only if (1) and (2) prove insufficient.

### 7. Vendored deps + license posture

All static deps vendored locally; no CDN:

- **Mermaid.js** (MIT) — for diagram rendering
- **HTMX** (BSD-2) — optional, for progressive forms
- **System fonts only at MVP** — no custom font dependency (faster load, broader compat). Custom pixel font deferred to V1+ if needed.
- **No JS frameworks.** Vanilla DOM + minimal vanilla JS.

License notice file at `~/.hacky-hours/companion/static/THIRD-PARTY.md` lists all vendored deps with their license.

### 8. Build performance / polish constraints

Per the original #8 RFC:

- **Initial load < 200ms** for any static page. Mermaid renders deferred / on-visibility.
- **Bundle target < 100KB** CSS + JS combined for the whole companion.
- **Works offline.** No external CDN dependencies.
- **Keyboard nav + deep-linkable URLs** everywhere.
- **Per-team accent color** drawn from team `README.md` frontmatter so users with multiple teams see at a glance which one they're in.
- **WCAG 2.1 AA baseline** (Lena's contribution).

### 9. Phased delivery

Phase 1 (T3.0–T3.3): scaffold + read-only project workspace + diagram gallery + audit timeline. Shipping alone provides immediate value.

Phase 2 (T3.4–T3.5): pixel-art bootstrap + Slack-style chat surface. The headline.

Phase 3 (T3.6): multi-workspace switcher + `projects.yml`. Enables cross-project navigation.

Phase 4 (T3.7–T3.8): forms + backlog write-back. Cost-saving moves (forms move structured input out of LLM turns).

Phase 5 (T3.9): session monitor. Real-time team activity view.

Each phase is one PR-sized chunk landing on `main` behind its respective flag (forms/backlog/session-monitor) or as opt-in via flag-less verb args (chat surface).

## Consequences

**Positive:**

- Non-engineers get a workspace that matches their expectations of "tools they use."
- The team becomes visible. Per-agent pixel art + chat surface elevates the orchestra metaphor from abstraction to lived experience.
- Cost-saving: forms move structured Q&A out of LLM turns (compounds with #10).
- Single source of truth (Markdown + JSONL) consumed by both terminal and browser — no data duplication, no sync problem.
- Zero per-use API spend. The browser never talks to an LLM.

**Negative / accepted:**

- One-time API spend during pixel-art bootstrap (~12 agents × small image generation = modest one-time cost). Mitigated by: opt-out fallback (emoji + initials) + regeneration only on explicit `team avatars` invocation.
- The Slack-style chat surface depends on `messages.jsonl` being populated, which depends on workroom mode being used. Without workroom adoption, chat channels are sparse. Acceptable: chat surface degrades gracefully, showing whatever's there.
- Companion is local-only at v4.1.0. Multi-user collaboration / hosted version is deferred to v4.2+ (was in original #8 RFC's deferral list too).
- Browser companion is a meaningful new attack surface even if local. Mitigated by: no third-party CDN, no LLM calls, no remote endpoints, content limited to what's already on disk.

## Alternatives considered

- **Web-app instead of static site.** Rejected: violates zero-API-spend constraint if backed by an LLM; otherwise no real advantage over static. Static = simpler ops, simpler security, simpler license.
- **Native desktop app** (Electron, Tauri). Rejected: dependency footprint, build pipeline, install friction. Browser is universal and free.
- **Integrate with existing tools** (VS Code extension, JetBrains plugin). Rejected: locks users into specific tooling. Browser is universal.
- **Real-time messaging server** for the chat surface. Rejected: violates the static-only / local-only constraints. JSONL polling (every 2s when `serve` is active) is sufficient for "real-time" at the scale of one user's local session.
- **Avatars generated client-side** (CSS gradients keyed on agent ID). Rejected: doesn't deliver the recognition payoff. Pixel art is the right aesthetic for the orchestra metaphor and reads as crafted.

## Related

- V4_DESIGN.md §4.28 — Browser companion (architecture overview)
- V4_DESIGN.md §4.29 — Slack-style team chat surface (sub-decision)
- ADR: 2026-05-22-workroom-mechanic.md (`messages.jsonl` is the chat surface's data source)
- ADR: 2026-05-22-three-artifact-model.md (presentations + status updates render here)
- ADR: 2026-05-22-feature-flag-layer.md (feature flags for write-back surfaces)
- `tools/team-site.md` — existing pattern this extends
- `tools/team-avatars.md` — new spec for pixel-art bootstrap (to author in T3.4)
- #8 RFC + ITERATION.md §A3, §A3.1, §B1, §B3
