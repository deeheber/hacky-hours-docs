# Glossary

Plain-language definitions for every term used in this framework. When you hit an unfamiliar word in a runbook or template, look it up here.

---

## A

**ARIA (Accessible Rich Internet Applications)**
A set of HTML attributes that help screen readers understand interactive elements on a webpage. For example, `aria-label` describes a button's purpose when the visual label alone isn't clear enough.

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

**Backend**
The part of an app that users don't see — the server, the database, and the logic that processes requests. Runs on a server, not in the browser.

---

## C

**CCPA (California Consumer Privacy Act)**
A California law giving residents the right to know what personal data is collected about them and to request its deletion. Relevant if your product has California users.

**Copyleft**
A licensing approach (used by GPL and AGPL) that requires anyone who modifies and distributes the code to also share their modifications under the same license. The opposite of "permissive" licenses like MIT, which don't have this requirement.

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

**Frontmatter**
Metadata at the top of a Markdown file, enclosed between `---` lines. Used by tools to store structured information (like a title or description) separate from the document's content. Written in YAML format.

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

**GDPR (General Data Protection Regulation)**
A European Union law governing how personal data is collected, stored, and processed. Applies to any product that serves EU users, regardless of where the company is based. Requires explicit consent and gives users the right to access, correct, and delete their data.

**GPL (General Public License)**
An open-source license that requires anyone who distributes modified versions of the code to also release their source code under the same license. See also: copyleft. AGPL (Affero GPL) extends this to software accessed over a network.

---

## H

**HIPAA (Health Insurance Portability and Accountability Act)**
A US law that governs how health information is stored and shared. If your product handles medical records, health data, or patient information, HIPAA compliance is required.

**Hosting**
Putting your app on a server so it's accessible on the internet. Services like Vercel and Netlify handle this for you — you push code to GitHub, and they deploy it automatically.

---

## M

**MCP (Model Context Protocol)**
A standard for connecting AI tools to external data sources and services. Think of it as a universal adapter that lets different AI applications (Claude Code, Cursor, etc.) plug into the same tools.

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

**NVDA (NonVisual Desktop Access)**
A free, open-source screen reader for Windows. Screen readers convert on-screen text to speech or Braille output, allowing visually impaired users to navigate software. Other common screen readers: VoiceOver (macOS/iOS), TalkBack (Android).

---

## O

**OAuth**
A standard that lets users log into your app using an existing account (like Google or GitHub) instead of creating a new username and password. Safer and simpler than building your own login system.

**OWASP Top 10**
A widely-referenced list of the ten most critical web application security risks, published by the Open Web Application Security Project. Includes things like injection attacks, broken authentication, and exposed sensitive data. Used as a baseline for security reviews.

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

**Screen Reader**
Software that reads aloud what's displayed on screen, enabling visually impaired users to navigate and interact with applications. Common screen readers: VoiceOver (macOS/iOS), NVDA (Windows), TalkBack (Android).

**Submodule**
A git feature that lets you include one repository inside another. The inner repo stays independent — it has its own history and can be updated separately. Used when you want to reference shared code or templates without copying them.

**Symlink (Symbolic Link)**
A shortcut file that points to another file or folder. When you open the symlink, you're actually opening the file it points to. Used to avoid duplicating files that need to exist in multiple locations.

---

## S

**Semantic Versioning**
A version numbering system: `MAJOR.MINOR.PATCH` (e.g., `1.2.3`). Patch = bug fix, Minor = new feature, Major = breaking change. The MVP ships as `0.1.0`; V1 ships as `1.0.0`.

**SSH**
A secure way to authenticate with remote servers (including GitHub) from the terminal. An alternative to HTTPS for pushing/pulling code.

**Tag (git)**
A named marker attached to a specific commit, typically used to mark release versions (e.g., `v1.0.0`). Unlike branches, tags don't move — they permanently mark a point in history. GitHub uses tags to create Releases.

---

## T

**Terminal**
A text-based interface for giving your computer instructions. Also called: command line, command prompt, shell, console. See `runbooks/getting-started/00-what-is-a-terminal.md` for a beginner guide.

---

## V

**VoiceOver**
Apple's built-in screen reader for macOS and iOS. Reads aloud on-screen elements so visually impaired users can navigate applications. See also: NVDA (Windows), TalkBack (Android).

**Version Control**
The practice of tracking changes to files over time so you can see what changed, when, and why — and revert if needed. Git is the most common version control system.

**VS Code (Visual Studio Code)**
A free, widely-used code and text editor made by Microsoft. Used in this framework for editing Markdown files and running the terminal.

---

## W

**WCAG (Web Content Accessibility Guidelines)**
International standards for making web content accessible to people with disabilities. The most common target is WCAG 2.1 AA — a practical middle ground that covers most accessibility needs. AAA is stricter but often impractical for all content. Published by the W3C (World Wide Web Consortium).

---

## Y

**YAML (YAML Ain't Markup Language)**
A human-readable data format used for configuration files. Uses indentation instead of brackets. You'll see it in frontmatter (the `---` blocks at the top of Markdown files) and in GitHub Actions workflow files.

---

## Related

- [00-what-is-a-terminal.md](./runbooks/getting-started/00-what-is-a-terminal.md)
- [Getting Started README](./runbooks/getting-started/README.md)
- [FAQ](./runbooks/FAQ.md)
