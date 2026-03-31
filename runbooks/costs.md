# What Will This Cost?

A plain-language breakdown of the costs involved in using the Hacky Hours framework and building a typical app. No surprises.

---

## Tools You Need to Get Started

| Tool | Cost | Notes |
|------|------|-------|
| **GitHub** | Free | The Free plan covers everything in this framework for a solo developer. Private repos are included. |
| **Claude Pro** | ~$20/month | Required for Claude Code. Check [claude.ai/pricing](https://claude.ai/pricing) for current pricing. |
| **VS Code** | Free | Open source, no subscription. |
| **GitHub Desktop** | Free | No subscription. |
| **Git** | Free | Open source. |

**Minimum to get started: ~$20/month** (Claude Pro only).

---

## Hosting Your App (When You Get There)

Most solo projects can start for free on modern hosting platforms. You only start paying when your app grows.

| Service | Free Tier | Paid Starts At | What It's For |
|---------|-----------|----------------|---------------|
| **Vercel** | Generous free tier for personal projects | ~$20/month (Pro) | Hosting web apps and APIs |
| **Netlify** | Similar to Vercel | ~$19/month (Pro) | Hosting web apps |
| **Supabase** | Free tier (pauses after 1 week inactive) | $25/month | Database + authentication |
| **Railway** | $5/month credit free | Usage-based | Backend services, databases |
| **Render** | Free tier available | $7/month | Web services and databases |

> **Important:** Supabase's free tier **pauses your database after 1 week of inactivity**. This is fine for building and testing, but before you share your app with real users, upgrade to the paid plan ($25/month) to avoid outages.

**Realistic cost for a live MVP: $20–$50/month** depending on the services you use.

---

## Domain Name (Optional)

If you want your app to have a custom URL (like `neighborboard.com` instead of `my-app.vercel.app`):

- Domain names typically cost **$10–$20/year**
- Purchased through registrars like [Namecheap](https://www.namecheap.com), [Porkbun](https://porkbun.com), or [Squarespace Domains](https://domains.squarespace.com)
- Most hosting platforms (Vercel, Netlify) let you connect a custom domain for free

---

## What You Don't Need to Pay For

- A server (modern hosting platforms handle this)
- A dedicated database server (Supabase, Railway, Render all manage this)
- A professional designer (the framework helps you define your design; Claude can generate code from it)
- A development agency

---

## Scaling Up

These costs assume a small-scale app (hundreds of users, not millions). If your app takes off:

- Vercel Pro ($20/month) handles significant traffic before you need enterprise plans
- Supabase Pro ($25/month) supports thousands of active users
- The main cost increase as you scale is database compute and bandwidth — but you'll have validated your idea long before that's a concern

---

## Cost-Saving Tips

- Start with Vercel + Supabase free tiers — they're genuinely sufficient for building and testing
- Don't buy a domain until you have something worth sharing
- Claude Pro is month-to-month — you can pause it between active building periods

---

## Related

- [02-claude-code.md](./getting-started/02-claude-code.md)
- [08-github-codespaces.md](./getting-started/08-github-codespaces.md)
- [FAQ](./FAQ.md)
