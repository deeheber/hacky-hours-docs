# Starter Prompt: Level 3 — Roadmap

Use this when your design documents are complete and you're ready to prioritize what to build.

---

## Prompt

```
I've completed my Level 2 design documents. Here they are:

[paste each completed design document, or summarize the key decisions if they're long]

I'm now building my ROADMAP.md. I need to:
1. List every feature implied by these design documents
2. Decide which features belong in the MVP, V1, and V2+

Please start by reading through everything and listing every distinct feature
you can identify. Then we'll go through them together and decide where each belongs.

Remember: the MVP should be the smallest version that proves the core value
of the product. Push back if I try to add too much to it.
```

---

## Tips

- Let Claude list the features first — it will often surface things you mentioned in design docs but didn't think of as discrete features
- For each feature, the key question is: "Can the product prove its value without this?" If yes, it's not MVP.
- "Nice to have" is not a tier — every feature should have a reason it's in V1 vs V2 vs never
- Milestones should describe outcomes, not tasks: "Residents can post and browse events" not "implement post CRUD"

---

## Scope Check

When you think your MVP list is done, ask Claude:

```
Based on what's in the MVP, how long do you estimate this would realistically
take to build? What are the most complex or risky parts?
```

If the answer is "several months," your MVP is probably too big. Keep cutting until it's something you could ship in weeks, not months.

---

## Related

- [level-2-design.md](./level-2-design.md)
- [level-4-build.md](./level-4-build.md)
- [03-roadmap/ROADMAP.md](../../03-roadmap/ROADMAP.md)
