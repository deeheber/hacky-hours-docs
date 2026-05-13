# /hacky-hours meta — cluster local feedback into framework patches

**Status: stub for v4.0.0-dev (deferred to a later slice on `feat/v4.0.0`).**

When complete, this verb reads `~/.hacky-hours/feedback/` and per-agent history signals, clusters friction by kind (tool / seam / role), and proposes specific diffs to specific files — role definitions, verb workflows, schemas. Output: local patchset the user can apply, plus (opt-in via `/hacky-hours issue`) draft GitHub issues to empathetech.

This is the closer on the dogfood improvement loop — friction → cluster → patch → review → next session is better.

Until this slice lands, tell the user:

> *"The meta-tool that closes the framework improvement loop is deferred to a later slice. It depends on feedback capture (also deferred) landing first."*

See `hacky-hours/02-design/V4_DESIGN.md` §3.4 for the improvement loop design.
