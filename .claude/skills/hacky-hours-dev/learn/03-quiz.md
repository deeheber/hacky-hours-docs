# Learn 3 — Quiz

*Supporting file for the `hacky-hours` skill. Loaded when the user runs `learn 3` / `learn quiz [area]`.*

**Context:** Read the relevant hacky-hours docs and codebase based on scope.

**Purpose:** Test and reinforce knowledge about the project.

**Phase 1: Determine scope**

If an area was specified, quiz on that area. If not: ask "Do you want a broad quiz covering the whole project, or focused on a specific area?"

**Phase 2: Generate questions**

Good question types: "Why was X chosen over Y?", "Where would you look if Z breaks?", "What would happen if you changed X?", "Which design doc governs this decision?"

Not: trivia, version number memorization, acronyms.

**Phase 3: Run conversationally**

One question at a time. After each answer: affirm and add context (correct), build on what they got right (partial), explain in plain language and point to the doc (incorrect).

**Phase 4: Summarize**

"Here's what you showed strong understanding of: [list]. Here are areas worth more time: [list] — check [doc names]."

**Optional site generation:** Same pattern as Tour. Generate in `ROOT_PATH/learn/quiz/` (general) or `ROOT_PATH/learn/personal/<username>/` (personalized, gitignored). Quiz cards with reveal-on-click answers.
