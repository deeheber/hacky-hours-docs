# TESTING.md

**Level 2 — Design** | [Your Project Name]

---

> **What is this?**
> A testing design document describes how you verify that what you built actually works the way you intended. It covers your testing strategy, what kinds of tests you'll use, and what "good enough" looks like before you ship.
>
> You don't need a PhD in software testing to fill this in. Start with: "How will I know this feature works?" and work backwards.

---

## Testing Strategy

*One paragraph describing your overall approach. Are you writing automated tests? Doing manual testing? Some combination? What's the principle guiding your decisions — e.g. "test at the boundaries, trust the internals" or "every user journey gets a test before it ships."*

---

## Test Types

*Delete the rows that don't apply to your project. Add rows for anything specific to your stack.*

| Type | What it covers | Tool / approach |
|------|----------------|-----------------|
| Unit tests | Individual functions or components in isolation | *e.g. Jest, pytest, Go test* |
| Integration tests | Multiple components working together | *e.g. Supertest, pytest with a real DB* |
| End-to-end tests | Full user journeys through the product | *e.g. Playwright, Cypress* |
| Manual testing | Exploratory testing against real user journeys | Pre-merge checklist |
| Accessibility testing | WCAG 2.1 AA compliance | *e.g. axe, Lighthouse, screen reader* |

---

## What We Test

*List the user journeys or features that must have test coverage before shipping. Pull these from USER_JOURNEYS.md if you have one.*

- *e.g. User can sign up and receive a confirmation email*
- *e.g. Payment fails gracefully and user is informed*
- *e.g. Form validation catches empty required fields*

---

## What We Don't Test (and Why)

*It's OK not to test everything. Name the gaps explicitly so they're a conscious decision, not an oversight.*

- *e.g. We don't test third-party payment processing — Stripe's own test suite covers that*
- *e.g. We don't test browser compatibility below IE11 — our users are on modern browsers*

---

## Definition of Done

*What does "tested enough to ship" look like for this project?*

- [ ] *e.g. All user journeys in the checklist pass manually*
- [ ] *e.g. No new failing tests introduced*
- [ ] *e.g. Accessibility score stays above X in Lighthouse*
- [ ] *e.g. The happy path works on mobile and desktop*

---

## Test Data and Environments

*Where do tests run? What data do they use?*

- **Test environment:** *e.g. Local only / CI on every PR / Staging before release*
- **Test data:** *e.g. Seeded fixtures / real anonymized data / generated on the fly*
- **External services:** *e.g. Stripe test mode / mock email / real GitHub API*

---

> **Claude Guidance**
>
> Before helping the user fill in this document:
> - Read PRODUCT_OVERVIEW.md to understand what's being built
> - Read USER_JOURNEYS.md if it exists — test coverage should trace back to user journeys
> - Read SECURITY_PRIVACY.md — security-sensitive features (auth, payments, data access) need explicit test coverage noted here
>
> Ask before assuming:
> - "Does this project have automated tests already, or are we starting from scratch?"
> - "What's the riskiest part of the product — the thing that breaking would be most painful?"
> - "How much time do you realistically have for writing tests versus building features?"
>
> Don't prescribe a testing framework. Recommend based on the user's stack and experience level. For beginners, start with manual testing checklists before introducing automation.
>
> The pre-merge checklist in `/hacky-hours checklist` already includes "Change has been manually tested against the relevant user journey" — this doc is where they define what that means for their specific product.

---

## Related

- [USER_JOURNEYS.md](./USER_JOURNEYS.md) — the journeys that need test coverage
- [SECURITY_PRIVACY.md](./SECURITY_PRIVACY.md) — security features that need explicit testing
- [BACKLOG.md](../04-build/BACKLOG.md) — testing tasks belong here like any other task
