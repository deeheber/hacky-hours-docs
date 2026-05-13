# /hacky-hours feedback — capture session friction (local-only)

**Status: stub for v4.0.0-dev (deferred to a later slice on `feat/v4.0.0`).**

When complete, this verb captures friction during real sessions and writes structured notes to `~/.hacky-hours/feedback/`. Three kinds of friction:

- **Tool friction** — a verb felt clunky
- **Seam friction** — a handoff between roles or verbs was lossy
- **Role friction** — an agent's output was wrong, over-cautious, under-cautious, jargon-y, etc.

All local-only by default. The `/hacky-hours meta` verb later clusters these into framework improvement patches; `/hacky-hours issue` opt-in submits to empathetech GitHub.

Until this slice lands, tell the user:

> *"Feedback capture is deferred to a later slice. For now, if something feels off during a session, just tell me directly and I'll keep it in mind. Once feedback capture lands, friction notes will accumulate into improvement signal."*

See `hacky-hours/02-design/V4_DESIGN.md` §3.4 for the improvement loop design.
