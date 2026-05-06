# Learn 1 — Tour

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `learn 1` / `learn tour`.*

**Context:** Read the relevant hacky-hours design docs broadly before starting. Don't ask the user to tell you things you can read.

**Purpose:** A structured walkthrough of the project for someone new — designed to build context, not overwhelm.

**Phase 1: Choose focus**

Ask what the person wants to focus on:
- Design docs — the why and what (PRODUCT_OVERVIEW, design documents)
- Architecture — how it's built and how pieces connect
- Data model — what data exists and how it's structured
- Full walkthrough — everything in a logical order

For projects using two-tier docs (v3.0.0+): use the summaries as onramps — they're the navigation surface designed for non-technical readers. Each summary cross-links into specific deep-dive sections; offer to drill into those when the person wants more depth or asks a question the summary can't answer. The deep dive is the source of truth; the summary is the gentle entry point.

**Phase 2: Walk through**

Read the relevant docs and present them as a logical progression. Narrate, don't just summarize — connect the dots: "This decision in ARCHITECTURE-summary.md is why the data model looks this way." Pause after each major section: "Does this make sense, or do you want to dig deeper into anything?" Name actual file paths so the person can open them.

**Phase 3: Wrap up and save feedback**

Ask: "Is there anything that wasn't clear, or anything you'd want to flag for the team?" If yes, save to `ROOT_PATH/feedback/feedback-<username>-<timestamp>.md`.

To get username: try `gh api user --jq .login`, fall back to `git config user.name`, fall back to asking.

**Optional site generation:**

Ask: "Would you like me to generate a shareable tour site?" If yes:

1. Check `node --version`. If not found, keep as conversation.
2. If Node found: generate an Astro project in `ROOT_PATH/learn/tour/` with one page per focus area, content from Markdown files, and a feedback form writing to `ROOT_PATH/feedback/`.
3. Tell the user: `cd hacky-hours/learn/tour && npm install && npm run dev`

For personalized tours: generate in `ROOT_PATH/learn/personal/<username>/` (gitignored).
