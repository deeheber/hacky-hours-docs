# Starter Prompt: Level 2 — Design

Use this at the start of a Level 2 design session to decide which documents your project needs and begin filling them in.

---

## Session Opener: Which Documents Do I Need?

Use this first to figure out your scope before diving into any single document.

```
I've completed my PRODUCT_OVERVIEW.md. Here it is:

[paste your PRODUCT_OVERVIEW.md contents here]

I'm now at Level 2 — Design. The available design documents are:
- ARCHITECTURE.md (how the technical pieces fit together)
- DATA_MODEL.md (what data the product stores and how it's structured)
- USER_JOURNEYS.md (how users move through the product)
- STYLE_GUIDE.md (visual design, brand, and tone)
- MARKET_FIT.md (who the users are and why they'd choose this)
- BUSINESS_LOGIC.md (rules and calculations the product enforces)
- SECURITY_PRIVACY.md (how user data is handled and protected)

Based on my product overview, which of these documents does my project actually need for the MVP? Which are optional? Please explain your reasoning for each.
```

---

## Starting a Specific Design Document

Once you know which documents to create, use this for each one:

```
I'm working on [DOCUMENT NAME] for my project. Here's my PRODUCT_OVERVIEW.md for context:

[paste PRODUCT_OVERVIEW.md]

Here's the blank template for this document:

[paste the relevant blank template, e.g., DATA_MODEL.md]

Please help me fill this in by asking me questions section by section.
Start with the first section and ask me what you need to know.
Don't fill in sections yourself until I've answered your questions — I want
to make the decisions, with your help.
```

---

## Generating a Diagram

After filling in a design document, use this to get a visual:

```
Based on the [DOCUMENT NAME] we just completed, please generate a Mermaid diagram
that visualizes [what you want to show — e.g., "the relationships between data entities"
or "the sign-up user journey" or "the system architecture"].

Use the appropriate Mermaid diagram type for this content.
```

Paste the resulting Mermaid code block into your document under the diagram section.

---

## Tips

- Do one document per session — don't try to fill in everything at once
- After each document, ask Claude: "Does anything in this document conflict with or require us to update another document we've already completed?"
- SECURITY_PRIVACY.md should be created for almost every project that has user accounts or stores any personal data — don't skip it

---

## Related

- [level-1-product-overview.md](./level-1-product-overview.md)
- [level-3-roadmap.md](./level-3-roadmap.md)
- [02-design/](../../02-design/)
- [example/02-design/](../../example/02-design/)
