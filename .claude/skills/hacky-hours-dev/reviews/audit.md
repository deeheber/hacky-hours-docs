# /hacky-hours audit — three-lane audit with traffic-light scorecard

**Status: stub for v4.0.0-dev (Slice 5 — in development on `feat/v4.0.0`).**

The v4 audit verb supersedes v3's `review 1`. When complete (Slice 5), it will run three parallel lanes:

- **(a) Role-driven codebase audit** — security, a11y, ops, QA, architect read the actual code and flag issues (P0/P1/P2)
- **(b) Doc audit** — context-free Claude session reads only `hacky-hours/docs/` and answers structured questions about clarity, completeness, would-a-stranger-onboard-from-this
- **(c) Cross-reference integrity** — broken links, stale paths, contradictions between docs

Output: consolidated report at `hacky-hours/audits/<date>.md` with a **scorecard** at the top — points + traffic lights (🟢/🟡/🔴 per dimension), at-a-glance section, then detailed findings.

Until Slice 5 lands, tell the user:

> *"The v4 audit verb is in active development — landing as Slice 5 of the v4.0.0 work.*
>
> *For now, you can run `/hacky-hours review 1` (v3 audit, still supported in v4) which provides a single-lane audit. The v4 audit adds the doc-audit lane (fresh-context Claude evaluates if your docs survive contact with someone unfamiliar) and the traffic-light scorecard."*

See `hacky-hours/02-design/V4_DESIGN.md` §4.1 for the full audit design.
