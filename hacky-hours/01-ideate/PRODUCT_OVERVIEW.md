# PRODUCT_OVERVIEW.md

**Level 1 — Ideation** | hacky-hours-docs

---

## Who — Target Audience

Anyone who has an idea and wants to build it with LLMs — from first-time builders writing their first line of code to seasoned engineers who've shipped many products. The common thread: they lack a structured process for going from idea to shipped product when working with an LLM as their primary collaborator.

Secondary audience: community organizers and educators who want a repeatable framework they can hand to participants (e.g., hackathons, workshops, coding meetups).

## What — Product Description

A documentation framework for LLM-assisted app development. It has two forms:

1. **A set of Markdown templates** organized into four levels (Ideation → Design → Roadmap → Build) that guide a user through figuring out what to build before writing code
2. **A Claude Code slash command (`/hacky-hours`)** that acts as a guided assistant, walking users through each level, scaffolding files, and managing the iterate/audit/sync lifecycle

On day one, a user either installs the slash command and runs `/hacky-hours` in any repo, or forks this repo and starts filling in templates directly.

## Where — Platform and Delivery

- **Primary**: GitHub repository (fork-able template)
- **Secondary**: Claude Code CLI slash command (installed via `curl | bash` or `irm | iex`)
- **Tertiary**: Git submodule import into existing projects

No server, no backend, no database. The "runtime" is Claude Code reading Markdown files as session context.

## When — Timeline and Priority

Active and shipping. Currently at v1.5.0 (2026-03-30). Iterating continuously based on community use and dogfooding. The lifecycle is non-linear — iterate for refinement, pivot for direction changes, optimize for efficiency review.

## Why — Value and Motivation

People vibe-code with LLMs and end up with products that don't match their intent — or worse, products with security holes, inaccessible UIs, and license conflicts they didn't know about. This framework gives structure without bureaucracy: figure out what you're building, design it honestly, prioritize ruthlessly, then build incrementally with review at each step.

The design philosophy — safety-first defaults, free before paid, accessible by default — matters because the audience includes people who don't yet understand the full consequences of what they're building. The framework protects them by making the safest choice the default, not the exception.

---

## Non-Goals

- This is not a code generator — it produces documentation, not application code
- This is not a project management tool — it complements GitHub Issues (via `sync --issues`) but doesn't replace Linear or Jira
- This is not a CI/CD system — `/hacky-hours sync` publishes releases but doesn't run tests or deployments
- This is not opinionated about tech stack — it helps you choose, but doesn't prescribe

---

## Constraints & Values

### Licensing Intent

MIT license. Open source. Maximum freedom for users to fork, modify, and use in any context — including commercial products.

No current revenue model. One could exist in the future (e.g., hosted version, premium templates, workshops), but it's immaterial for current design decisions.

### Privacy Stance

The framework itself collects zero user data. No analytics, no telemetry, no tracking. The slash command runs entirely within the user's Claude Code session — Anthropic's security boundary, not ours.

### Infrastructure Preference

No infrastructure. Pure Markdown files distributed via GitHub. The install scripts download a single file to the user's local `.claude/commands/` directory. No servers to manage, no accounts to create, no dependencies to install.

### Accessibility Commitment

All documentation should be clear, jargon-free, and accessible to people with no prior technical experience. The GLOSSARY.md exists for this reason. The getting-started runbooks cover zero-install paths (GitHub Codespaces) alongside full terminal setups.

WCAG 2.1 AA is the recommendation this framework makes to its users for their own products.
