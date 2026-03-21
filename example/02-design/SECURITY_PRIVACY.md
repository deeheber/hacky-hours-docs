# SECURITY_PRIVACY.md — NeighborBoard Example

> This is a filled-in example. See the blank template at [`02-design/SECURITY_PRIVACY.md`](../../02-design/SECURITY_PRIVACY.md).

---

## Data Inventory

| Data Type | Why Collected | Where Stored | Retention Period |
|-----------|--------------|--------------|-----------------|
| Email address | Login and notifications | Supabase Auth | Until account deleted |
| Display name | Shown on posts | Supabase DB | Until account deleted |
| Post content (title, body, date, location) | Core product function | Supabase DB | Until post removed or account deleted |
| RSVP records | Event attendance tracking | Supabase DB | Until event passes + 90 days |
| Magic link tokens | Authentication | Supabase Auth (temporary) | Expire after 1 hour |
| IP address / request logs | Standard server logs | Vercel (automatic) | 30 days, then auto-deleted |

---

## Authentication and Access

- **Magic link auth:** Users receive a one-time login link via email. No passwords are stored. Links expire after 1 hour.
- **Sessions:** Supabase manages session tokens, stored in the browser as HTTP-only cookies (not accessible to JavaScript).
- **Locked out:** If a user loses access to their email, they lose access to their account. There is no manual recovery in the MVP — document this limitation clearly in the UI.

---

## Authorization Rules

| Role | Can | Cannot |
|------|-----|--------|
| Guest (not logged in) | View all posts and RSVP counts | Post, RSVP, or see post authors' emails |
| Resident | Post events/announcements, RSVP, delete their own posts | Delete others' posts, access admin panel |
| Admin | All resident actions + remove any post, see RSVP lists | Edit another resident's post content |

---

## Data in Transit and at Rest

- All traffic between browser and Vercel is over HTTPS — enforced automatically by Vercel.
- Supabase encrypts data at rest by default.
- Environment variables (database URL, API keys) are stored in Vercel's encrypted environment variable store — never in the codebase or committed to git.

---

## Third-Party Data Sharing

| Service | What is shared | Why |
|---------|---------------|-----|
| Supabase | Email, display name, posts, RSVPs | Database and auth provider |
| Vercel | Request metadata, IP addresses | Hosting provider (standard server logs) |
| Resend | Email address, email content | Sending magic links and notifications |

No data is shared with advertisers, analytics platforms, or social networks.

---

## User Rights and Controls

- **View their data:** Users can see all their own posts and RSVPs on their profile page.
- **Delete their posts:** Users can delete any post they created.
- **Delete their account:** A "Delete my account" button removes their profile, display name, and RSVPs. Their posts are anonymized (author shown as "Former Resident") rather than deleted, to preserve neighborhood history.
- **Opt out of notifications:** Users can disable email notifications at any time from their profile settings.

---

## Known Threat Vectors

| Threat | Mitigation |
|--------|-----------|
| Unauthorized posting (spam/harassment) | Only authenticated residents can post; admin can remove posts |
| Email enumeration (testing if an email is registered) | Magic link flow always shows "Check your email" regardless of whether the address exists |
| Exposing home addresses | Location field is optional and free-text — product guidance discourages exact addresses |
| Secrets exposed in code | All API keys in environment variables; `.env` files listed in `.gitignore` |
| XSS via post content | Post body rendered as escaped text, not raw HTML |
| Excessive RSVP spam | One RSVP per user per event enforced at the database level |

---

## Compliance Considerations

- **GDPR / CCPA:** The app collects email addresses and user-generated content. A basic privacy policy is required before public launch. The account deletion flow satisfies the "right to erasure" requirement.
- **COPPA:** The app is not directed at children. A minimum age statement in the terms of service is sufficient for MVP.
- **No payment data:** No financial information is collected. PCI-DSS does not apply.

---

## Pre-Launch Security Checklist

- [ ] No API keys or secrets in the git repository
- [ ] All user input (post titles, bodies, display names) is sanitized before storage
- [ ] Magic link tokens expire and cannot be reused
- [ ] Admin routes check role before executing
- [ ] `.env` files are in `.gitignore`
- [ ] Supabase Row Level Security (RLS) policies are enabled and tested
- [ ] Privacy policy page is live with contact information
- [ ] Account deletion flow is tested end-to-end

---

## Related

- [DATA_MODEL.md](./DATA_MODEL.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [Blank SECURITY_PRIVACY.md template](../../02-design/SECURITY_PRIVACY.md)
