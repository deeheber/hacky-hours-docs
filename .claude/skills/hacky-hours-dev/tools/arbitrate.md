# /hacky-hours arbitrate <mode> <topic> — resolve role disagreement

**Status: stub for v4.0.0-dev (deferred to a later slice on `feat/v4.0.0`).**

When complete, three named arbitration patterns the conductor (you) can invoke when roles disagree:

- **`/hacky-hours arbitrate decide <topic>`** — framework summarizes positions concisely; conductor decides directly. Cheapest. Default behavior when a conflict surfaces mid-verb.
- **`/hacky-hours arbitrate resolve <topic>`** — conductor states high-level concerns; framework asks each role to propose a resolution against those concerns; conductor picks. Medium cost.
- **`/hacky-hours arbitrate watch <topic>`** — two or more roles converse with each other, transcript visible to conductor, ends on convergence or conductor interrupt. Higher cost.

All three produce an ADR in `hacky-hours/02-design/decisions/` once resolved.

Until the arbitrate slice lands, tell the user:

> *"Arbitration modes are deferred to a later slice in v4.0.0 development. Until then, the conductor (you) makes the call directly — describe the disagreement and I'll summarize positions for you to decide."*

See `hacky-hours/02-design/V4_DESIGN.md` §4.11 for the full arbitration design.
