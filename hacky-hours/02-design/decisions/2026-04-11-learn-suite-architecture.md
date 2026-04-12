# ADR: Learn Suite Architecture

**Date:** 2026-04-11
**Status:** Accepted
**Deciders:** bjamba

---

## Context

Adding three new commands (`learn tour`, `learn onboard`, `learn quiz`) for knowledge transfer and onboarding. Two architectural decisions needed to be settled before implementation:

1. What delivery mechanism (conversation, static site, or both)?
2. What static site stack?

---

## Decision 1: Conversation-First, Site-Optional

**Chosen:** Claude Code conversation is the baseline for all three modes. Static site generation is an optional richer layer on top.

**Alternatives considered:**
- Site-only: requires Node.js, excludes users who don't have it, adds setup friction
- Conversation-only: simpler, but loses the interactive feedback form and shareable artifact value

**Rationale:** Conversation mode works everywhere Claude Code runs with zero setup. The framework's core principle is reducing friction for new builders. A feature that fails silently because Node isn't installed would undermine trust. By making conversation the baseline, we guarantee the feature always works and let the site be an enhancement for users who want it.

**Consequence:** Every `learn` command must produce a complete, useful experience in conversation mode before site generation is considered done.

---

## Decision 2: Astro as the Static Site Stack

**Chosen:** Astro

**Alternatives considered:**
- Plain HTML/CSS/vanilla JS — lightest, no build step, but interactive features (markdown editor in feedback form, quiz UI) become verbose and brittle to maintain as hand-written JS
- 11ty (Eleventy) — Markdown-native, minimal, but weaker component model for interactive pieces; Islands architecture not available
- React/Next.js — over-engineered for this use case; build complexity and bundle size not justified

**Rationale:**
- Content lives in Markdown files — when the codebase changes, regeneration means updating `.md` files, not HTML
- Islands architecture scopes interactive components (feedback form, quiz) without making the whole site a JS app
- Content Collections are purpose-built for "a folder of Markdown files becomes a section of a site"
- Strong community momentum; the framework's own collaborators are likely to know it

**Consequence:** Node.js is now an optional dependency for site generation. The command must check for Node before attempting site generation and degrade gracefully to conversation mode if unavailable. This is the first external runtime dependency the framework has introduced — worth monitoring for friction.

---

## Decision 3: Grouped as `/hacky-hours learn [tour|onboard|quiz]`

**Chosen:** Sub-subcommand grouping under `learn`

**Alternatives considered:**
- Three flat top-level commands (`tour`, `onboard`, `quiz`) — simpler hierarchy, consistent with other top-level commands
- Flag-based (`learn --tour`, `learn --onboard`) — wrong pattern; flags modify operations, they don't select distinct operations

**Rationale:** `tour`, `onboard`, `quiz` are distinct operations that share a conceptual theme (learning). Grouping under `learn` reduces perceived top-level complexity and signals the relationship. Follows the same pattern as `mode [engineer|default]`. The v2.0.0 command audit milestone will evaluate whether to flatten these to top-level once the full command surface is reviewed holistically.

---

## Related

- [ARCHITECTURE.md — Learn Suite section](../ARCHITECTURE.md)
- [ARCHITECTURE.md — Static Site Generation section](../ARCHITECTURE.md)
- [SECURITY_PRIVACY.md — Node.js Dependency section](../SECURITY_PRIVACY.md)
