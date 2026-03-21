# Level 2: Design

Design documents define how your product works — in detail, and from multiple angles. Together, they give Claude (and future human collaborators) the context needed to make good decisions during implementation.

**Not every project needs every document.** Start by reviewing this list with Claude. Share your `PRODUCT_OVERVIEW.md` and ask: "Which of these documents does my project actually need?"

---

## Documents in This Level

| Document | Use when... |
|----------|-------------|
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Your product has multiple systems, services, or technical layers that interact |
| [`DATA_MODEL.md`](./DATA_MODEL.md) | Your product stores, retrieves, or transforms data of any kind |
| [`USER_JOURNEYS.md`](./USER_JOURNEYS.md) | You need to map out how users move through key flows in your product |
| [`STYLE_GUIDE.md`](./STYLE_GUIDE.md) | Your product has a UI and you want consistent visual design and language |
| [`ACCESSIBILITY.md`](./ACCESSIBILITY.md) | Your product has a UI — build accessibly from day one, not as an afterthought (almost always) ♿ |
| [`MARKET_FIT.md`](./MARKET_FIT.md) | You want to validate who your users are and why they'd choose your product |
| [`BUSINESS_LOGIC.md`](./BUSINESS_LOGIC.md) | Your product has rules, calculations, or domain-specific behavior that needs to be explicit |
| [`SECURITY_PRIVACY.md`](./SECURITY_PRIVACY.md) | Your product handles user data, authentication, payments, or anything sensitive (almost always) |
| [`LICENSING.md`](./LICENSING.md) | Almost always — ask early, before any dependencies are chosen |
| [`decisions/`](./decisions/) | Record significant design changes over time without overwriting original documents |
| [`diagrams/`](./diagrams/) | You want visual representations of any of the above |

---

## How to Work Through This Level

1. Share `PRODUCT_OVERVIEW.md` with Claude and ask which documents apply to your project
2. Work through each relevant document one at a time — don't try to fill everything in at once
3. Generate Mermaid diagrams for complex relationships (see [`diagrams/README.md`](./diagrams/README.md))
4. Cross-reference documents as you go — decisions in one often affect others

---

## Done Enough to Move On?

You're ready for Level 3 when:
- A new collaborator could read these docs and understand how the product is meant to work — they don't need to be complete, they need to be honest
- There are no major open questions about how core features function
- `SECURITY_PRIVACY.md` and `ACCESSIBILITY.md` exist in some form, even if minimal

---

## Claude Guidance for This Level

When helping a user at Level 2:
- Begin every design session by re-reading `PRODUCT_OVERVIEW.md` — especially the **Constraints & Values** section — to stay grounded in the product's licensing intent, privacy stance, and infrastructure preferences
- Help the user select only the documents they actually need — avoid over-engineering
- When a document reveals a gap or contradiction in `PRODUCT_OVERVIEW.md`, surface it clearly
- Generate Mermaid diagrams proactively for data models, user journeys, and architecture — visuals help non-technical stakeholders validate understanding
- `SECURITY_PRIVACY.md` should be created for almost every project that handles user data; prompt the user if they're skipping it
- `ACCESSIBILITY.md` should be created for almost every project with a UI; it's the most commonly skipped document and the most costly to fix later
- `LICENSING.md` should be created early — before architecture decisions lock in dependency choices. License compatibility is much easier to reason about before than after
- **Safety-first throughout:** when recommending tools, services, or approaches, lead with the free/simple/privacy-preserving option. Explain tradeoffs before suggesting complexity. The user can choose a more powerful path — but they should choose it knowingly
- When design decisions change during iteration, write a short Architecture Decision Record (ADR) in `decisions/` rather than rewriting the original document — this preserves the reasoning behind original decisions

---

## Related

- [Level 1: Ideation](../01-ideate/README.md)
- [Level 3: Roadmap](../03-roadmap/README.md)
- [diagrams/](./diagrams/)
