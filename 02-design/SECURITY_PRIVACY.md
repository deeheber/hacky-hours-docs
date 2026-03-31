# SECURITY_PRIVACY.md

**Level 2 — Design** | Contributed by: Product owner, with Claude facilitation

> **What is this?** This document helps you think through how your product protects the people who use it — what personal information it collects, how it keeps that information safe, and what could go wrong. You don't need to be a security expert. You just need to think honestly about what you're asking users to trust you with.

This document defines how your product handles sensitive data, protects its users, and guards against common threats. It is not optional — if your product touches real users, this document must exist in some form before you write production code.

---

> **Claude Guidance:** This document should be revisited before every implementation task in Level 4. When helping the user fill it out, ask: "What's the most sensitive thing your product stores?" and "What would happen if an attacker got into your database?" Keep the language approachable — no jargon. Flag any gaps (e.g., "you mentioned email addresses but haven't addressed how they're stored") and recommend minimizing data collection where possible. Reference OWASP Top 10 in plain language when relevant. Do not skip this document even for "small" projects — a small project with real users has real responsibilities.
>
> **Data minimization is a security strategy, not just a privacy preference.** Less data stored = smaller breach impact. Push back on collecting data "just in case." Every field in the data model should have a clear reason to exist.
>
> **For authentication:** strongly prefer OAuth providers (Google, GitHub) or magic links over passwords the product manages itself. Custom password auth is one of the most common sources of security failures and is almost never necessary for new projects. Flag this clearly if the user is leaning toward custom auth.
>
> **For dependency review:** check `LICENSING.md` alongside this document — GPL/AGPL license conflicts can become compliance issues, not just licensing ones.

---

## Data Inventory

*What personal or sensitive data does your product collect, store, or transmit? Be exhaustive — include things that feel minor, like email addresses or IP logs.*

| Data Type | Why Collected | Where Stored | Retention Period |
|-----------|--------------|--------------|-----------------|
| | | | |

## Authentication and Access

*How do users prove who they are? How are sessions managed? What happens when a user is locked out or needs to reset credentials?*

## Authorization Rules

*Who is allowed to see or modify what? Cross-reference with `BUSINESS_LOGIC.md` for role definitions.*

## Data in Transit and at Rest

*Is data encrypted when sent over the network? Is it encrypted in storage? What keys or secrets are involved and how are they managed?*

## Third-Party Data Sharing

*What data does your product send to third-party services (analytics, payments, email, etc.)? For each, note what is shared and why.*

## User Rights and Controls

*What can users do with their own data? Can they export it, delete it, or correct it? How do you handle deletion requests?*

## Known Threat Vectors

*The most likely ways your product could be attacked or misused. For each, describe the mitigation.*

| Threat | Mitigation |
|--------|-----------|
| Unauthorized access to user accounts | |
| Injection attacks (SQL, command, etc.) | |
| Cross-site scripting (XSS) | |
| Exposed secrets in code or logs | |

## Dependency Security and License Hygiene

*Third-party code introduces both security and licensing risk. Review both.*

- **Known vulnerabilities:** Are any dependencies flagged in vulnerability databases (e.g., via `npm audit`, `pip-audit`, or GitHub Dependabot)?
- **Maintenance status:** Are key dependencies actively maintained? Unmaintained libraries are a long-term security risk.
- **License compatibility:** Do any dependencies carry GPL or AGPL licenses that conflict with your product's license? Cross-reference with `LICENSING.md`.
- **Third-party API terms:** Do the terms of service for any external APIs restrict commercial use, data portability, or resale?

| Dependency | Known CVEs | Actively maintained? | License | Conflicts? |
|------------|-----------|---------------------|---------|-----------|
| | | | | |

## Compliance Considerations

*Any legal or regulatory requirements that apply — GDPR, CCPA, HIPAA, COPPA, etc. Note what applies and the key obligations.*

## Pre-Launch Security Checklist

*A list of security conditions that must be verified before going live. Claude should check these before marking any implementation task as complete.*

- [ ] No secrets or API keys in version control
- [ ] All user input is validated and sanitized
- [ ] Authentication tokens expire appropriately
- [ ] Error messages do not expose internal state
- [ ] Dependencies are reviewed for known vulnerabilities
- [ ] User data deletion flow is tested

---

## Related

- [Design README](./README.md)
- [DATA_MODEL.md](./DATA_MODEL.md)
- [BUSINESS_LOGIC.md](./BUSINESS_LOGIC.md)
- [LICENSING.md](./LICENSING.md)
- [build/BACKLOG.md](../04-build/BACKLOG.md)
