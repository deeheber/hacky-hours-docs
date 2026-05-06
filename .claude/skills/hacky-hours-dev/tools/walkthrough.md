# Tools: Walkthrough

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `tools walkthrough`.*

**Purpose:** Narrative overview of how all the commands work together. Designed for framework adopters who want to understand the whole picture before diving in.

Walk through the framework as a story:

**The shape of a project:**

1. **Step 1 — Ideate.** You start with `/hacky-hours step 1`. This is where you get your idea out of your head and into structured form. No code yet — just who you're building for, what it does, and why it matters.

2. **Step 2 — Design.** Once you know what you're building, `/hacky-hours step 2` helps you define how it works. Architecture, data model, user journeys, security, accessibility — whichever ones your project needs. As of v3.0.0, each design doc is built as a deep dive first (the actual blueprint, what AI builds from), then a one-screen summary is generated from it as a faithful condensation for quick gut-checks and as an onramp for non-technical readers.

3. **Step 3 — Roadmap.** `/hacky-hours step 3` takes everything from your design docs and helps you decide what to build first. The goal is a small, shippable MVP.

4. **Step 4 — Build.** `/hacky-hours step 4` drives the implementation cycle. Pick a task from BACKLOG.md, build it against your design docs, verify before merging.

5. **Step 5 — Iterate.** After you ship, `/hacky-hours step 5` captures feedback, amends docs, and queues the next round of work. This is the main loop — most of your time will be here.

**The review commands:**

At any point, you can step back and evaluate. They go from tactical to strategic:

- `/hacky-hours review 1` — "Did we follow best practices?" Run before every release.
- `/hacky-hours review 2` — "Did we build it well?" Run when something feels off mid-cycle.
- `/hacky-hours review 3` — "Should we be building something else?" Run when you're questioning direction.

**Onboarding others:**

When someone new joins or you want to check understanding:

- `/hacky-hours learn 1` — walk them through the project (big picture first)
- `/hacky-hours learn 2` — get them hands-on with a real starter task
- `/hacky-hours learn 3` — test what they know

**Shipping:**

- `/hacky-hours review 1` → run this first
- `/hacky-hours update 1` → publish the GitHub Release
- `/hacky-hours update 2` → keep BACKLOG and GitHub Issues in sync

**Framework management:**

- `/hacky-hours tools upgrade` → update your project artifacts when you update the command (also: onboard an existing codebase, or migrate from an old layout)
- `/hacky-hours tools mode` → switch conversation style between builder (plain language) and engineer (technical)

**The bare command `/hacky-hours` with no arguments** surveys your project and figures out where you are. It's always safe to run — it just tells you what it found and asks what you want to do.

Ask the user: "Does this give you a clear enough picture, or would you like me to go deeper on any particular part?"
