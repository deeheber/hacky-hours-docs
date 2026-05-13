---
name: Default Team
tier: full
established: TEMPLATE
philosophy: "Twelve stakeholder voices, one conductor. Every project gets the full team unless you opt for a leaner setup."
---

# Default Team

This is your starting Hacky Hours team — a full 12-role roster covering every stakeholder a great software org would have. Each agent has its own persistent profile, history, and feedback record. As they work on your projects, they learn what you value and adapt.

## Roster

- 📊 **Maya Tanaka** — Product
- 🎨 **Felix Okafor** — Design / UX
- 🏗️ **Priya Chen** — Architect
- 🖥️ **Marcus Rivera** — Frontend Engineer
- ⚙️ **Sam Park** — Backend Engineer
- 🛡️ **Alex Davies** — Security Engineer
- 🚀 **Jordan Kim** — Ops / SRE
- 🔍 **Emma Wright** — QA
- ♿ **Lena Mwangi** — Accessibility
- 📜 **Diego Romano** — Licensing / Legal
- 📈 **Yuki Nakamura** — Data Engineer
- 🤖 **Kai Patel** — AI/ML Engineer

## How this team works

- **You are the conductor.** They are your team; you make the calls. They flag, recommend, and produce; you decide.
- **Voice adapts to you.** Each agent reads your audience profile and adjusts their communication — plain language for non-engineers, precise vocabulary for engineers.
- **They listen to each other.** When one agent produces something the next needs, the handoff is automatic. You don't have to relay between them.
- **They grow over time.** Feedback you give in any session becomes durable. They get better the more you work together.

## Switching teams

This is the default team. You can:
- Create leaner teams (Solo, Lean, Startup tiers) via `/hacky-hours team new`
- Switch the active team per project via the project's `AGENTS.md`
- Fork and customize any agent on this team via `/hacky-hours team` browse + edit

## Files in this folder

- `tier.yml` — team-size tier + roster configuration
- `agents/` — one folder per agent, each with profile/system-prompt/history/feedback
- `VERSION` — framework version this team was built against
- `LICENSE` — your usage license (private by default)
