# /hacky-hours adopt — bring an existing codebase into the framework

**Status: stub for v4.0.0-dev (Slice 4 — in development on `feat/v4.0.0`).**

This is the **only operation on existing code** in v4. There is no separate "productionize" verb — production-grade emerges from continuous ensemble play after adoption, not from a one-shot productionization step.

When complete (Slice 4), this verb will:

1. Detect that this is an existing repo (no `hacky-hours/` folder yet, but code exists).
2. Ask orientation questions: tier, intent, sensitive paths.
3. Bind the project to an active team (from `~/.hacky-hours/teams/`).
4. Fan out every role in the active team to read the codebase in parallel.
5. Each role roleplays its assessed level of involvement based on what it finds.
6. Consolidates into a single `hacky-hours/adoption-assessment-<date>.md` artifact.
7. Conductor reviews top-to-bottom and confirms/adjusts involvement per role.
8. Generates the v4 artifact set: AGENTS.md, CLAUDE.md (v4 schema), NARRATIVE.md, STATE.md, HANDOFFS.yml, VOICE.md, plus role-specific first-impressions design docs.

Until Slice 4 lands, tell the user:

> *"Adoption is in active development — landing as Slice 4 of the v4.0.0 work. It depends on Slice 2 (team scaffold) which is being built first.*
>
> *In the meantime, you can use `/hacky-hours tools upgrade` (v3 verb, still supported in v4) which provides the v3 version of codebase adoption — it infers PRODUCT_OVERVIEW and creates scaffold files. The v4 version will fan out the full role roster in parallel for richer first-impressions."*

See `hacky-hours/02-design/V4_DESIGN.md` §3.2 and §4.10 for the full adopt design.
