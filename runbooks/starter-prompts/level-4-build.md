# Starter Prompt: Level 4 — Build

Use this at the start of each implementation task. One session = one task from BACKLOG.md.

---

## Session Opener: Start a Task

```
I'm starting work on a task from my BACKLOG.md. Here's the task:

[paste the task description from BACKLOG.md]

For context, here are the relevant design documents:

[paste ARCHITECTURE.md — or the relevant section]
[paste the relevant section of DATA_MODEL.md if the task touches data]
[paste SECURITY_PRIVACY.md — or the relevant section]

Before we write any code, please:
1. Confirm you understand what this task requires
2. Ask me any clarifying questions you have
3. Outline the approach you'd take before starting

I want to review your plan before you begin writing code.
```

---

## Before Merging: Pre-Merge Review

When the task feels done, use this before pushing:

```
We've finished implementing [task name]. Before I push this, please review
the changes and check them against:

1. The requirements in the task description
2. The security checklist in my SECURITY_PRIVACY.md:
[paste the pre-launch checklist section]
3. The relevant user journey in USER_JOURNEYS.md to make sure the
   behavior matches what was designed

Flag anything that needs attention before I open a pull request.
```

---

## Writing the Commit Message

```
Help me write a clear git commit message for this task.
The change: [one sentence describing what changed]
The why: [one sentence on why it was needed]

Keep it under 72 characters for the subject line. Add a brief body if needed.
```

---

## Updating the Changelog

```
We just completed [milestone name] and are cutting a release.
Here are the tasks that were completed:
[paste completed tasks from BACKLOG.md]

Please draft a CHANGELOG.md entry for this release in plain language.
Write it for a non-technical audience — the people using the app,
not the people building it.
```

---

## Tips

- Always share the relevant design documents at the start of a session — Claude doesn't remember previous sessions
- If Claude suggests something that contradicts a design decision, say: "That conflicts with what we decided in ARCHITECTURE.md — let's stick with the original approach"
- Small tasks = better results. If a task feels too big to complete in one session, break it into smaller pieces and add them to BACKLOG.md

---

## Related

- [level-3-roadmap.md](./level-3-roadmap.md)
- [04-build/BACKLOG.md](../../04-build/BACKLOG.md)
- [04-build/README.md](../../04-build/README.md)
- [02-design/SECURITY_PRIVACY.md](../../02-design/SECURITY_PRIVACY.md)
