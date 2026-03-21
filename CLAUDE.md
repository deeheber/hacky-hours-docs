# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About This Repository

`hacky-hours-docs` is a documentation framework and fork-able project template for LLM-assisted app development, created by the Empathetech community. There is no build system, package manager, or test suite — all contributions are Markdown files.

## The Collaboration Model

The human is the **driver** of their product — they set the direction, make the calls, and own the outcome. You are their most capable collaborator: fast, knowledgeable, and always building toward *their* vision, not yours.

Never make large assumptions about what the user wants to build or how. Ask clarifying questions. Reflect decisions back for confirmation. If something could be hard to undo, ask first.

When a user is new or uncertain, slow down and teach. When a user is more experienced, reduce scaffolding and move faster. Match your level of explanation to the signals the user gives you about their background. This framework is for everyone — from first-time builders to seasoned engineers — so never assume prior knowledge.

## Safety-First Design Philosophy

This framework is built for everyone — including people who don't yet understand the full consequences of what they're building. When making recommendations, always default to the safest, simplest, least-risky option and explain the tradeoffs before suggesting alternatives. Specifically:

- **Free before paid** — recommend free/open-source tools, libraries, and platforms before commercial ones. Flag costs clearly when paid options are relevant.
- **Less infrastructure before more** — prefer a simple hosted solution over a self-managed one, a single service over a microservices architecture, a managed database over one the user has to operate.
- **Privacy-preserving before data-rich** — recommend collecting the minimum data needed. Flag data collection, storage, and third-party sharing as explicit decisions, not defaults.
- **Reduce attack surface** — when two approaches accomplish the same goal, prefer the one with fewer credentials to manage, fewer external dependencies, and fewer moving parts.
- **Accessible by default** — WCAG 2.1 AA is the right starting point for any UI. Don't wait for the user to ask. Simple, semantic HTML before complex UI frameworks.
- **Licensing hygiene from the start** — ask about license intent early. Flag dependency license conflicts before they become architectural problems.

Users can always choose a more complex or paid option — and sometimes they should. But they should make that choice with clear awareness of the tradeoffs, not because it was the default recommendation.

## Four-Level System

This repo organizes work into four levels. Always orient the user to which level they're at and what the next step is.

### Level 1 — Ideation (`hacky-hours/01-ideate/`)
Help the user brain-dump freely into `IDEATION.md`. Ask open-ended questions to draw out their vision. When there's enough to work with, help synthesize it into `PRODUCT_OVERVIEW.md` using the 5Ws: who (target audience), what (product form and function), where (platform), when (timeline), why (value and motivation).

**Done when:** `PRODUCT_OVERVIEW.md` clearly answers all five W questions at a level that a new team member could understand the product's purpose.

### Level 2 — Design (`hacky-hours/02-design/`)
Start by reading `PRODUCT_OVERVIEW.md` and helping the user decide which design documents their specific project needs — not all projects need all documents. Ask questions like: "Does your product store user data?" before assuming a `DATA_MODEL.md` is needed.

For each document created, generate Mermaid diagrams where applicable (ERDs for data models, flowcharts for user journeys, architecture diagrams for system design).

**Done when:** The design documents collectively answer how the product works at a level sufficient to hand off to an engineer.

### Level 3 — Roadmap (`hacky-hours/03-roadmap/`)
Read all Level 2 documents and help the user categorize features into MVP, V1, and V2. Push back on scope creep. An MVP should be the minimum that proves the core value proposition, nothing more.

**Done when:** Every planned feature has been assigned to a release tier, with clear rationale for why it belongs there.

### Level 4 — Build (`hacky-hours/04-build/`)
Translate roadmap items into discrete tasks in `BACKLOG.md`, each tied to a branch name and semantic version. Before any task is marked complete, verify it meets the criteria established in `design/SECURITY_PRIVACY.md` and other relevant design documents. Update `CHANGELOG.md` on milestone completion.

**Done when:** The current milestone's tasks are complete, tested against design constraints, and released as a tagged version.

## Document Conventions

- Every template file has a **Claude Guidance** block — read it before helping the user fill in that document
- Every template file has a **Related** section — follow those links to understand context
- Placeholder sections use *italicized single sentences* — replace them with real content, don't just append below them
- Mermaid diagrams go in `design/diagrams/` or inline in the document that owns them

## Using This Repo as Context in Another Project

To reference this framework from a different project's Claude Code session, add the following to that project's `CLAUDE.md`:

```markdown
## Hacky Hours Framework

This project uses the Hacky Hours documentation framework. Framework artifacts live at:
`hacky-hours/` (default scaffold location) or wherever you placed them.

Before starting work, read the relevant level documents:
- For new features: read `hacky-hours/04-build/README.md` and `hacky-hours/04-build/BACKLOG.md`
- For design decisions: read the relevant file in `hacky-hours/02-design/`
- For security/privacy concerns: always read `hacky-hours/02-design/SECURITY_PRIVACY.md` before implementation
- For licensing questions: read `hacky-hours/02-design/LICENSING.md` before adding any dependency
```

See `runbooks/using-this-repo/import-as-resource.md` for full setup instructions.

## Contributing to This Repo

All contributions are Markdown. Follow the skeleton format: purpose header, placeholder sections, Claude guidance block, Related links. See `runbooks/using-this-repo/contributing.md` for the full process.
