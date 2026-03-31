# ACCESSIBILITY.md

**Level 2 — Design** | Contributed by: Product owner, with Claude facilitation

> **What is this?** Accessibility means making sure your product works for everyone — including people who use screen readers, navigate by keyboard, have low vision, or experience your product differently than you do. This document helps you plan for that from the start, which is much easier than fixing it later. Good accessibility also makes your product better for *all* users: clearer language, better contrast, simpler navigation.

The earlier you design for it, the easier it is. Review this document before implementation begins and revisit it whenever new UI surfaces are added.

---

## Standards

*Which accessibility standard does this product target? Common choices:*

- **WCAG 2.1 AA** — the most widely adopted baseline for web and mobile products. Required by law in many jurisdictions. This is the recommended default.
- **WCAG 2.1 AAA** — a higher bar, appropriate for products serving users with specific accessibility needs
- **Section 508** — required for US federal products and contractors
- **EN 301 549** — required for products sold in the EU public sector

*Chosen standard: [e.g., WCAG 2.1 AA]*

---

## Perceivable

Users must be able to perceive all content and interface elements.

### Visual

- **Color contrast** — text must meet a minimum contrast ratio of 4.5:1 (AA) against its background. Large text (18pt+) requires 3:1.
  - *Chosen contrast approach: [e.g., all text ≥ 4.5:1; use a tool like WebAIM Contrast Checker to verify]*
- **Color as the only indicator** — color must never be the sole way to convey information (e.g., a red error border must also include an error icon or text label)
- **Text resizing** — the UI must remain usable when text is scaled up to 200%

### Images and media

- **Alt text** — all meaningful images must have descriptive alt text. Decorative images use `alt=""`.
- **Captions** — all video content must include captions. Auto-generated captions must be reviewed for accuracy.
- **Audio descriptions** — video that conveys information visually must include audio descriptions for blind users

*List any known image-heavy or media-heavy areas that will need special attention: [e.g., the product feed, onboarding video]*

---

## Operable

Users must be able to navigate and interact with all functionality.

### Keyboard navigation

- All interactive elements (links, buttons, form fields, modals) must be reachable and operable using only a keyboard
- Focus order must follow a logical reading sequence
- Focus must always be visible — never remove the focus ring without replacing it with an equally visible custom indicator
- Keyboard traps (where focus gets stuck) must not exist

### Touch and pointer

- Touch targets must be at least 44×44px
- Gestures must not be the only way to perform an action (e.g., swipe-to-delete must have a button alternative)

### Time limits

- If the product uses session timeouts, users must be warned before the session ends and given the option to extend it

*List any time-sensitive interactions: [e.g., session timeout, auto-advancing carousels]*

---

## Understandable

Users must be able to understand the content and how to use the interface.

### Language

- The page language must be declared (e.g., `<html lang="en">`)
- Error messages must clearly describe what went wrong and how to fix it — not just "invalid input"
- Instructions must not rely solely on sensory characteristics (e.g., "click the green button" is not accessible)

### Consistency

- Navigation and labeling must be consistent across the product
- Unexpected changes of context (e.g., auto-submitting a form when a checkbox is checked) must not happen without warning

*Note any areas where the product's language or instructions may need review: [e.g., onboarding copy, error states]*

---

## Robust

The product must work with current and future assistive technologies.

### Semantic markup (web/mobile)

- Use native HTML elements where possible (`<button>`, `<nav>`, `<main>`, `<header>`) rather than generic divs styled to look like them
- Custom components must use appropriate ARIA roles, states, and properties when native elements aren't sufficient
- Form inputs must have associated labels (not just placeholder text)

### Screen reader support

*Which screen readers will be tested against?*

- Web: [e.g., NVDA + Chrome (Windows), VoiceOver + Safari (macOS/iOS)]
- Mobile: [e.g., TalkBack (Android), VoiceOver (iOS)]

*Target: all critical user journeys must be completable with a screen reader.*

---

## Testing Plan

| Method | When | Who |
|--------|------|-----|
| Automated scan (e.g., axe, Lighthouse) | Every PR | CI / developer |
| Keyboard-only walkthrough | Before each release | Developer |
| Screen reader walkthrough | Before each milestone release | Developer or QA |
| User testing with people who use assistive tech | [Frequency] | [Owner] |

*Note any known gaps in current testing coverage: [e.g., no screen reader testing in CI yet]*

---

## Known Issues and Exceptions

*Document any known accessibility gaps that have been accepted, with justification and a remediation plan.*

| Issue | Affected users | Justification | Target fix |
|-------|----------------|---------------|------------|
| *[e.g., PDF exports not screen-reader-friendly]* | *[e.g., blind users]* | *[e.g., third-party library limitation]* | *[e.g., V2 milestone]* |

---

## Claude Guidance

When helping the user fill in this document:

- Ask about the product's platform first (web, mobile, desktop, API) — accessibility requirements differ significantly
- If the product has a UI, `WCAG 2.1 AA` is the right default unless there's a specific reason to go higher or lower
- **Start simple, stay semantic:** the most effective accessibility improvements are also the simplest — use native HTML elements (`<button>`, `<nav>`, `<label>`) instead of styled divs, add alt text, ensure keyboard focus is visible. These cost almost nothing and cover the majority of use cases. Only reach for ARIA when native elements aren't sufficient.
- **Accessible-by-default tech choices:** when recommending UI frameworks or component libraries, prefer ones with strong built-in accessibility (e.g., Radix UI, Headless UI, React Aria) over ones that require extensive manual remediation. Flag accessibility track records when comparing options.
- Push gently on the testing plan — automated tools catch ~30% of issues. Keyboard and screen reader testing are essential and often skipped
- If the user isn't sure where to start, suggest beginning with the three most commonly missed items: color contrast, keyboard navigation, and alt text
- Frame accessibility as a quality bar, not a compliance checkbox — and as a values statement. Empathetech builds for everyone. This document is where that commitment becomes concrete.
- **Don't defer:** accessibility is significantly harder to retrofit than to build in. If a user says "we'll add accessibility later," flag that this is one of the most common and costly mistakes in product development.

---

## Related

- [`STYLE_GUIDE.md`](./STYLE_GUIDE.md) — color palette and contrast decisions live here
- [`USER_JOURNEYS.md`](./USER_JOURNEYS.md) — journeys should be verified for keyboard and screen reader completability
- [`SECURITY_PRIVACY.md`](./SECURITY_PRIVACY.md) — accessibility intersects with privacy when assistive tech data is involved
