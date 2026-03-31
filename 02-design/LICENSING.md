# LICENSING.md

**Level 2 — Design** | Contributed by: Product owner, with Claude facilitation

> **What is this?** A license is a set of rules that says what other people can and can't do with your code — and what you can and can't do with code written by others. This document helps you pick a license for your product and make sure the tools and libraries you use are compatible with that choice. It sounds legal (and it is), but the decisions are straightforward once you understand your options.

This document covers two things: (1) the license you choose for **your product**, and (2) the licenses attached to the **code and services you depend on**, and how they interact.

---

> **Claude Guidance:** Ask about licensing early — at the start of Level 2, not the end. The license choice affects architecture (can we use this library?), business model (can we charge for this?), and compliance (do we have to publish our source?). Keep explanations plain — most people building with this framework haven't navigated licensing before. Lead with a simple question: "Do you want others to be able to use, modify, or build on your code freely?" Then walk through the implications. Never assume a license — always surface the choice explicitly.

---

## Your Product's License

*What license governs your product's source code? If you haven't decided yet, use the questions below to think it through.*

### Key Questions

- **Open or closed source?** Do you want your source code to be publicly visible and reusable? Or do you want to keep it private?
- **Commercial or non-commercial?** Do you plan to charge for access, usage, or a hosted version of this product?
- **Do you want to allow others to fork and modify it?** If yes, can they keep their modifications private, or must they also share?

### Common License Choices (plain language)

| License | Who it's for | Key rule |
|---------|-------------|----------|
| **MIT** | Open source projects that want maximum freedom | Anyone can use, copy, modify, and distribute — including in commercial products. Almost no restrictions. |
| **Apache 2.0** | Open source projects that want patent protection included | Like MIT but also grants explicit patent rights. Good for projects where patent risk is a concern. |
| **GPL v3** | Open source projects that want to stay open | Anyone who distributes a modified version must also release their changes under GPL. "Copyleft." |
| **AGPL v3** | Open source projects that also cover hosted/SaaS use | Like GPL but closes the "SaaS loophole" — even running the software as a service requires publishing changes. |
| **BSL (Business Source License)** | Projects that want time-limited protection | Source is visible but not freely usable commercially until a specified date, then converts to open source. |
| **Proprietary / All rights reserved** | Closed source commercial products | You retain all rights. Others cannot use, copy, or distribute without your permission. |

*Chosen license: [fill in — or leave as TBD and note the open questions]*

*Reasoning: [Why this license? What tradeoffs did you weigh?]*

---

## Dependency License Inventory

*The code and services you depend on have their own licenses. Some restrict how you can use them — especially in commercial or closed-source products.*

### Questions to work through

- What open-source libraries does your project use?
- Are any of them GPL or AGPL licensed? (If so, and your product is closed source, you may have a conflict.)
- Are you using any third-party APIs or services with their own terms of service? (These can restrict commercial use, data portability, or resale.)

### Dependency table

| Dependency | License | Commercial use OK? | Copyleft? | Notes |
|------------|---------|-------------------|-----------|-------|
| *[e.g., React]* | *[MIT]* | *[Yes]* | *[No]* | *[No restrictions]* |
| *[e.g., PostgreSQL]* | *[PostgreSQL License]* | *[Yes]* | *[No]* | *[Very permissive]* |

*If you're unsure about a dependency's license, search "[library name] license" or check its GitHub repo's LICENSE file.*

---

## License Compatibility

*Does your chosen product license conflict with any dependencies?*

The main risk: if you use a copyleft library (GPL/AGPL) in a closed-source product, the copyleft terms may require you to open-source your product too. Claude can help you check compatibility — just list your dependencies above.

*Known conflicts or open questions: [fill in, or "none identified"]*

---

## Business Model Implications

*How does your license interact with how you plan to make money?*

- **Selling the software directly** — proprietary or BSL licenses fit best; GPL-licensed software can be sold but buyers can redistribute it freely
- **Hosted/SaaS model** — if you want to prevent competitors from hosting your code, consider AGPL or BSL
- **Open core model** — open-source the base, charge for hosted or premium features — a common and viable strategy
- **Grants, non-profit, or community use** — open source (MIT/Apache) often makes you more eligible for public funding and community contribution

*Planned business model: [fill in]*

*License alignment: [does the license support that model?]*

---

## Pre-Build Checklist

- [ ] Product license chosen and documented
- [ ] All major dependencies reviewed for license compatibility
- [ ] No GPL/AGPL dependencies used in a closed-source context without legal review
- [ ] Third-party API terms of service reviewed for commercial use restrictions
- [ ] LICENSE file added to the repository root

---

## Claude Guidance (extended)

When working through this document with a user:

- If the user is building a personal or community project with no commercial plans, MIT or Apache 2.0 is usually the right answer — explain it in one sentence and move on
- If the user wants to make money, spend more time: walk through the hosted model vs. selling question, and flag AGPL/BSL as options that protect against "cloud giants forking your work"
- If the user is unsure, default to recommending **MIT** as the safest, most permissive starting point with a note that they can always add restrictions later (but not retroactively remove them from what's already been published)
- Always flag GPL/AGPL transitive dependencies if any are identified in the architecture — these are easy to miss and can be expensive to fix later
- For dependencies on commercial SaaS APIs: flag that terms of service can change, which is a form of infrastructure risk

---

## Related

- [Design README](./README.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md) — dependency choices happen here
- [SECURITY_PRIVACY.md](./SECURITY_PRIVACY.md) — open-source dependency security intersects with license hygiene
- [build/BACKLOG.md](../04-build/BACKLOG.md) — add "Add LICENSE file to repo" as a task
