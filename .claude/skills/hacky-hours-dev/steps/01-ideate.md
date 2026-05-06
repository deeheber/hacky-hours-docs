# Step 1 — Ideation

*Supporting file for the `hacky-hours` skill. Loaded when the user is at Step 1.*

**Context:** If `IDEATION.md` already exists under ROOT_PATH, read it before asking any questions — don't ask the user to repeat what they've already written.

**Purpose:** Get ideas out of the user's head and into structured form.

**IDEATION.md** is a free-writing space. No rules — just capture everything. Prompt the user with:
- "Who is the first person you'd want to use this, and what would they do with it?"
- "What problem have you personally experienced that this solves?"
- "What would have to be true for this to be considered a success in one year?"

**PRODUCT_OVERVIEW.md** synthesizes IDEATION.md into five W answers plus a Constraints & Values section:
- **Who** — target audience (specific, not "anyone")
- **What** — what the product does and what form it takes
- **Where** — platform (mobile, web, desktop, API, etc.)
- **When** — rough timeline or priority
- **Why** — the problem it solves and why it matters
- **Constraints & Values** — licensing intent, privacy stance, infrastructure preference

Go one W at a time. Ask focused questions. Reflect the user's words back to them.

After completing the 5Ws, always ask the Constraints & Values questions before moving to Step 2:

1. **Licensing:** "Do you want your code to be open source — meaning others can see, use, and build on it — or do you want to keep it private? Are you planning to charge money for it?"
2. **Privacy:** "How much user data does this product really need to collect? Less is almost always safer, cheaper, and easier to comply with legally."
3. **Infrastructure:** "Do you want someone else to manage the servers, or are you comfortable managing your own?"

These answers seed the `LICENSING.md` and `ARCHITECTURE.md` work in Step 2.

**Done when:** Someone unfamiliar with the project could read PRODUCT_OVERVIEW.md and understand what's being built, including its core values and constraints. ✅
