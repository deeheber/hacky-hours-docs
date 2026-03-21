# Frequently Asked Questions

Answers to the questions people ask most often about this framework.

---

## Getting Started

**Do I need to know how to code?**
No. The framework is designed for people who want to build something but don't have a technical background. Claude handles the code. Your job is to understand what you're building well enough to direct it — which is what all the documents in this framework help you do.

**Can I use ChatGPT instead of Claude?**
The framework is designed around Claude Code specifically, which integrates directly with your files and project structure. You could use ChatGPT for filling in document templates by copying and pasting, but you'd lose the tight project-context integration that makes the Level 4 build process work well. The starter prompts in `runbooks/starter-prompts/` work with any LLM for the documentation phases.

**How much does this cost?**
See [costs.md](./costs.md) for a full breakdown. The short answer: ~$20/month for Claude Pro to get started. Hosting when you're ready to go live is $0–$50/month depending on the platform and your usage.

**How long will setup take?**
- Zero-install path (Codespaces): ~15 minutes
- Local install path: ~45–60 minutes

See the [Getting Started README](./getting-started/README.md) for your specific path.

---

## Using the Framework

**Where do I start?**
Start at [`runbooks/getting-started/README.md`](./getting-started/README.md) to get set up, then go to [`01-ideate/`](../01-ideate/) to start your first project.

**Do I have to complete every document before moving to the next level?**
No — but the documents you do create should be complete enough to inform the next level. The level READMEs each include a "Done enough to move on?" checklist. The most important thing is that `PRODUCT_OVERVIEW.md` is solid before starting Level 2, and your design documents are consistent before starting Level 3.

**What if I make a mistake and want to undo it?**
That's what git is for. Every commit is a saved state you can return to. If you make changes you want to undo, run `git log` to see your recent commits, then ask Claude: "I want to revert to the state my project was in at [commit message]. How do I do that safely?"

**Can I skip levels?**
You can, but it usually creates problems later. Skipping ideation means you start building before you know what you're building. Skipping design means Claude makes up architectural decisions rather than following yours. The levels exist because the order matters.

**What if the templates don't fit my project?**
The templates are starting points, not rules. Delete sections that don't apply, add sections you need. They're Markdown files — edit them freely.

---

## Working with Claude

**Claude gave me something I don't want. What do I do?**
Tell it directly: "That's not what I was looking for. What I actually want is..." Claude doesn't get offended and doesn't remember past sessions, so you won't hurt its feelings by pushing back. Pushback is how you maintain ownership over your product.

**Claude keeps forgetting what we discussed.**
Claude doesn't have memory between sessions. That's why the documents exist — they're your persistent memory. At the start of each session, give Claude the relevant documents as context. The starter prompts in `runbooks/starter-prompts/` are designed to do this automatically.

**Is it safe to share my project details with Claude?**
Review Anthropic's privacy policy at [anthropic.com/privacy](https://www.anthropic.com/privacy). As a general rule: don't share secrets (passwords, API keys, personal user data) in your Claude Code sessions. Project documents describing what you're building are fine.

**Claude wrote code I don't understand. Should I use it?**
Ask Claude to explain it before you commit it: "Walk me through what this code does, line by line, in plain language." If you don't understand it, you can't maintain it, debug it, or make informed decisions about it. Understanding what's being built is a core principle of this framework.

---

## Git and GitHub

**What if I accidentally delete something?**
If it was committed, it's not gone — git keeps the full history. Run `git log` to see recent commits, then ask Claude to help you recover it.

**What's the difference between git and GitHub?**
Git is the version control software that runs on your computer and tracks changes. GitHub is the website that hosts your repository online, adds collaboration features, and backs up your work. See the [Glossary](../GLOSSARY.md) for more.

**Do I need to commit after every change?**
No — commit when you've finished a meaningful chunk of work (completing a document, finishing a task). A good rule of thumb: if you'd be annoyed to lose everything since your last commit, it's time to commit.

---

## Building and Deploying

**When am I ready to actually build the app (write code)?**
When you have: a completed `PRODUCT_OVERVIEW.md`, the Level 2 design documents your project needs, and a `ROADMAP.md` with a defined MVP scope. See the [Level 4 README](../04-build/README.md) for the full checklist.

**Do I need to know how to deploy an app?**
Not in detail — that's what Claude and platforms like Vercel are for. By the time you get to deployment, Claude will have helped you set up the hosting configuration as part of the build process. The runbooks in this repo will be expanded with deployment guides as the community builds them out.

**What if I want to build something that's not a web app?**
The four-level framework applies to any software project — mobile apps, desktop tools, APIs, browser extensions. The specific design documents you need and the tools for building will differ, but the ideation → design → roadmap → build structure is universal.

---

## Community and Contributing

**How do I contribute a pattern I found useful?**
See [contributing.md](./using-this-repo/contributing.md).

**I found something outdated or wrong. How do I report it?**
Open an issue on the GitHub repository, or fix it yourself and submit a pull request.

---

## Related

- [GLOSSARY.md](../GLOSSARY.md)
- [costs.md](./costs.md)
- [Getting Started README](./getting-started/README.md)
- [Contributing](./using-this-repo/contributing.md)
