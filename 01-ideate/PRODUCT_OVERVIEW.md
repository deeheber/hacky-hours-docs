# PRODUCT_OVERVIEW.md

**Level 1 — Ideation** | Contributed by: Product owner, with Claude facilitation

This document answers the five foundational questions about your product. It is synthesized from `IDEATION.md` through a conversation with Claude. Every answer here should come from you — Claude helps draw it out and structure it, but you make the decisions.

This document becomes the source of truth for all Level 2 design work. When in doubt about the product's direction, come back here.

---

> **Claude Guidance:** Help the user fill in each section by asking focused questions drawn from their `IDEATION.md`. If a section is vague, push for specificity — "anyone could use it" is not a useful audience definition. Keep language plain and jargon-free. Once the five Ws are drafted, work through the **Constraints & Values** section before declaring Level 1 done — these answers directly shape Level 2 design choices. Once a complete draft exists, read it back to the user in plain language and ask if it matches their vision.

---

## Who — Target Audience

*Who is this product for? Describe the primary user: their background, what they're trying to accomplish, and what they struggle with today. Be specific — "small business owners who don't have a dedicated IT person" is better than "businesses."*

## What — Product Description

*What does this product do, and in what form does it exist? Describe the core functionality and the user experience at a high level. What can a user do with it on day one?*

## Where — Platform and Delivery

*Where does this product live? Examples: web app, iOS/Android mobile app, desktop app, command-line tool, API, browser extension, hardware device. If multiple platforms, note which is primary.*

## When — Timeline and Priority

*What is the rough timeline? Is there a deadline, a launch target, or a milestone that matters? What needs to exist first? This doesn't need to be precise — "build a working prototype in 2 months" is enough to start.*

## Why — Value and Motivation

*Why does this product need to exist? What problem does it solve, and why is that problem worth solving? Why are you the right person to build it? Why would someone choose this over alternatives?*

---

## Non-Goals

*What is explicitly out of scope? What will this product NOT do, at least for now? Defining boundaries early prevents scope creep and keeps the team aligned.*

---

## Constraints & Values

*These answers shape every design decision that follows. Be honest — there are no wrong answers, but vague answers lead to mismatched recommendations.*

### Licensing Intent

*Will this product's source code be open source (publicly visible and reusable) or closed source (private)?*

*If open source: which license? (MIT, Apache 2.0, GPL, etc.) If you're not sure yet, note that — it's a question to resolve early in Level 2.*

*Is this product intended to generate revenue? If so, how? (e.g., subscription, one-time purchase, free with premium features, grants/donations)*

### Privacy Stance

*How much user data does this product actually need to collect? What is the minimum required for the product to function?*

*Are there categories of data you explicitly want to avoid collecting (e.g., location, behavioral tracking, health information)?*

### Infrastructure Preference

*Do you prefer managed/hosted infrastructure (someone else runs the servers) or self-hosted (you manage your own)? Or no preference yet?*

*Is cost a significant constraint? Are free tiers acceptable, or is there a budget for paid services?*

### Accessibility Commitment

*Who needs to be able to use this product? Are there specific accessibility needs to design for from day one?*

*Default target: WCAG 2.1 AA. Is there a reason to go higher or lower?*

---

> **Claude Guidance:** Work through these questions with the user before moving to Level 2. These constraints directly shape which architecture choices are appropriate, what data to collect, and which third-party services are compatible. If the user hasn't thought about licensing, explain the basics in plain language: open source vs. closed source, and whether they plan to charge for the product. Default recommendation for personal or community projects: MIT license, managed hosting, minimum viable data collection.

---

## Related

- [Level 1 README](./README.md)
- [IDEATION.md](./IDEATION.md) — the source material for this document
- [Level 2: Design](../02-design/README.md) — the next step after this document is complete
- [LICENSING.md](../02-design/LICENSING.md) — seed from the Licensing Intent answers above
