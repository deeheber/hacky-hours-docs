# Glossary

Plain-language definitions for every term used in this framework. When you hit an unfamiliar word in a runbook or template, look it up here.

---

## A

**API (Application Programming Interface)**
A way for two pieces of software to talk to each other. When your app "calls an API," it's sending a request to another service (like a payment processor or weather data provider) and getting back a response. You don't need to know how the other service works — just what to ask and what you'll get back.

**Authentication**
Proving who you are. When you log in with an email and password, or click a magic link, you're authenticating — confirming your identity to the system.

**Authorization**
Deciding what you're allowed to do once you're logged in. Authentication says "this is Sarah." Authorization says "Sarah is allowed to post events but not delete other people's posts."

---

## B

**Backlog**
A prioritized list of tasks that need to be completed. In this framework, it lives in `BACKLOG.md`. Think of it as your project's to-do list, organized by which version each task belongs to.

**Branch**
A parallel version of your project where you can make changes without affecting the main version. When a task is done, the branch gets merged back into `main`. Named after what you're working on, e.g., `feat/user-signup`.

**Bug**
An error in the code that causes the product to behave in an unintended way.

---

## C

**CLI (Command-Line Interface)**
A text-based way to interact with software — you type commands instead of clicking buttons. Claude Code is a CLI tool. The terminal is where you run CLI tools.

**Clone**
Downloading a copy of a repository from GitHub to your computer. Unlike a fork (which lives on GitHub), a clone lives on your hard drive.

**Codespace**
A cloud-based development environment provided by GitHub. Runs VS Code and a terminal in your browser — no local installation required. See `runbooks/getting-started/08-github-codespaces.md`.

**Commit**
A saved snapshot of your changes, with a message describing what changed. Think of it as a checkpoint in a video game — you can always return to it.

---

## D

**Database**
Where an application permanently stores information. When a user creates an account or posts something, it gets written to the database. Common types: PostgreSQL (relational/table-based), MongoDB (document-based).

**Dependency**
A piece of software that your project relies on. When you run `npm install`, you're installing dependencies.

**Deploy / Deployment**
Making your app available on the internet for real users to access. Hosting platforms like Vercel handle deployment automatically when you push code to GitHub.

---

## E

**Environment Variable**
A configuration value stored outside your code — typically secret credentials like API keys or database passwords. They live in a `.env` file locally and in your hosting provider's settings in production. Never commit them to git.

**ERD (Entity Relationship Diagram)**
A visual diagram showing what data your app stores and how different types of data relate to each other. Used in `DATA_MODEL.md`.

---

## F

**Fork**
Creating a personal copy of someone else's GitHub repository under your own account. Your fork is independent — changes you make don't affect the original. This is how you get your own copy of `hacky-hours-docs`.

**Frontend**
The part of an app that users see and interact with — the screens, buttons, and layout. Runs in the browser.

---

## G

**Git**
The version control system that tracks changes to your project over time. Every commit, branch, and push uses git under the hood.

**GitHub**
A website that hosts git repositories and adds collaboration tools (pull requests, issues, releases). Git is the tool; GitHub is the service.

**GitHub Desktop**
A free app that gives you a visual interface for git operations — no terminal required.

---

## H

**Hosting**
Putting your app on a server so it's accessible on the internet. Services like Vercel and Netlify handle this for you — you push code to GitHub, and they deploy it automatically.

---

## M

**Magic Link**
A login method where the system emails you a one-time link that logs you in when clicked — no password needed. Simpler and often more secure than traditional passwords for low-risk applications.

**Main (branch)**
The primary, production-ready version of your codebase. Changes are merged into `main` after review.

**Markdown**
A simple text formatting syntax used for all documents in this framework. `**bold**` becomes **bold**, `# Heading` becomes a heading. GitHub and VS Code both render it automatically.

**Merge**
Combining changes from one branch into another — typically merging a feature branch into `main` after it's been reviewed.

**Mermaid**
A plain-text diagramming syntax that GitHub renders as visual diagrams. Used in this framework for architecture diagrams, ERDs, and flowcharts.

**MVP (Minimum Viable Product)**
The smallest version of your product that proves your core idea. Deliberately incomplete — just enough to test whether people find value in it.

---

## N

**Node.js**
A JavaScript runtime that lets you run JavaScript code outside a browser. Required to install Claude Code. You don't need to write any Node.js code — you just need it installed.

**npm**
Node Package Manager — a tool for installing JavaScript packages and tools. Comes with Node.js. Used to install Claude Code: `npm install -g @anthropic-ai/claude-code`.

---

## P

**PATH**
A system setting that tells your computer where to look for programs when you type a command in the terminal. If you install a tool and your terminal says "command not found," the tool's location isn't in your PATH.

**PR / Pull Request**
A request to merge changes from one branch into another, with an opportunity for review before the merge happens. Even if you're working solo, opening a PR creates a record of what changed and why.

**Production**
The live, real version of your app that actual users access. Opposite of "local" (your computer) or "staging" (a test environment).

---

## R

**Repository (Repo)**
A folder for your project that git tracks. Contains all your files, plus the full history of every change ever made. Lives on GitHub and optionally as a local clone on your computer.

**RSVP**
In the context of this framework's example project, a user's response to an event. In general use: confirming attendance.

---

## S

**Semantic Versioning**
A version numbering system: `MAJOR.MINOR.PATCH` (e.g., `1.2.3`). Patch = bug fix, Minor = new feature, Major = breaking change. The MVP ships as `0.1.0`; V1 ships as `1.0.0`.

**SSH**
A secure way to authenticate with remote servers (including GitHub) from the terminal. An alternative to HTTPS for pushing/pulling code.

---

## T

**Terminal**
A text-based interface for giving your computer instructions. Also called: command line, command prompt, shell, console. See `runbooks/getting-started/00-what-is-a-terminal.md` for a beginner guide.

---

## V

**Version Control**
The practice of tracking changes to files over time so you can see what changed, when, and why — and revert if needed. Git is the most common version control system.

**VS Code (Visual Studio Code)**
A free, widely-used code and text editor made by Microsoft. Used in this framework for editing Markdown files and running the terminal.

---

## Related

- [00-what-is-a-terminal.md](./runbooks/getting-started/00-what-is-a-terminal.md)
- [Getting Started README](./runbooks/getting-started/README.md)
- [FAQ](./runbooks/FAQ.md)
