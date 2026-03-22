# RELATED_REPOS.md

**Level 2 — Design** | Contributed by: Product owner, with Claude facilitation

Some products are built across multiple repositories — a backend and a frontend, a service and its CLI, a shared library and the apps that use it. When that's the case, design decisions in one repo constrain what's possible in the others. This document captures those relationships: which repos exist, who owns what, and where to look before making decisions that cross repo boundaries.

---

> **Claude Guidance:** Only create this document when the product genuinely spans multiple repos — don't manufacture cross-repo complexity that doesn't exist. If the user is at Level 2 and their ARCHITECTURE.md describes a multi-repo split, ask whether a related repo exists or is planned and suggest creating this document. The most valuable section is the Decision Routing Table — it prevents the dependent repo from making decisions that contradict already-settled design in the authoritative repo. Use the local path if both repos are cloned side by side; fall back to the GitHub URL if not.

---

## Repo: *[related repo name, e.g., my-app-ui]*

*One sentence describing what this repo is and how it relates to this one.*

**GitHub:** *https://github.com/org/repo-name*
**Local path:** *../repo-name* ← relative to this repo's root; update if cloned elsewhere

### Relationship

*Which repo is the source of truth and which is the dependent? What does each repo own?*

| | This repo | Related repo |
|---|---|---|
| **Role** | *[e.g., authoritative backend]* | *[e.g., UI consumer]* |
| **Owns** | *[e.g., data model, business logic, API contracts]* | *[e.g., presentation, UX, routing]* |
| **Source of truth for** | *[e.g., all data structures and enums]* | *[e.g., component system and visual design]* |

*When there is a conflict between the two repos' design docs, which one wins?*
*Answer: [e.g., "This repo wins — the related repo raises an ADR here before changing anything upstream."]*

### Decision Routing Table

*Before making a decision in the related repo, read the relevant doc here. This table is the bridge — it prevents the dependent repo from re-litigating settled design questions.*

| When the related repo needs to know... | Read in this repo |
|----------------------------------------|-------------------|
| *[e.g., What data does this component need?]* | *[e.g., `02-design/DATA_MODEL.md`]* |
| *[e.g., What does this status value mean?]* | *[e.g., `02-design/BUSINESS_LOGIC.md` — Enums section]* |
| *[e.g., What API endpoints exist?]* | *[e.g., `02-design/ARCHITECTURE.md` — API section]* |
| *[e.g., What accessibility rules apply?]* | *[e.g., `02-design/ACCESSIBILITY.md`]* |
| *[e.g., Can I add this dependency?]* | *[e.g., `02-design/LICENSING.md` — Compatibility Matrix]* |

### Cross-Repo Coordination Protocol

*When a decision in the related repo requires a change in this repo:*

1. Check whether this repo's design docs already address it
2. If not, write an ADR in this repo's `02-design/decisions/` — don't change the related repo first
3. Update the affected design doc in this repo
4. Then implement in both repos — authoritative repo first

*Add additional repos below using the same structure if there are more than two.*

---

## Claude Guidance (extended)

When working through this document with a user:

- Read ARCHITECTURE.md first — the system overview and component boundaries tell you what the related repo is responsible for
- The Decision Routing Table is the most important output: walk through the related repo's likely design questions one by one and map each to the section in this repo that answers it
- If the local path isn't known yet (e.g., the related repo hasn't been created), leave it as a placeholder and note that `/hacky-hours link` can populate this document once both repos exist
- When generating this document for the **dependent** repo (the one that conforms to the authoritative repo), reverse the table direction: "when this repo needs to know X, read Y in the other repo"
- If both repos are already cloned locally, Claude can read the other repo's design docs directly using the local path — this is always preferred over summarizing from memory

---

## Related

- [Design README](./README.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md) — the multi-repo split is defined here
- [SECURITY_PRIVACY.md](./SECURITY_PRIVACY.md) — cross-repo data flow has security implications
- [LICENSING.md](./LICENSING.md) — dependent repos must meet the same license compatibility bar
