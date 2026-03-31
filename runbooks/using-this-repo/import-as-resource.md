# Import hacky-hours-docs as a Resource

You can bring the Hacky Hours framework into an existing project so Claude Code can reference it as in-session context. This is useful when you want Claude to follow the four-level system inside a codebase that already has its own structure.

Three approaches are described below, from most to least recommended. **If you're not sure which to pick:** Option 1 is best for ongoing projects, Option 2 is easiest for a quick start, and Option 3 is for when you just need a file or two.

---

## Option 1: Git Submodule (recommended for ongoing projects)

A **submodule** is a way to include one project inside another. Think of it as a folder in your project that stays linked to the Hacky Hours repo — you can update it whenever the framework releases improvements, and your project always knows exactly which version of the framework it's using.

### Setup

Inside your project's terminal:

```bash
# Add the framework as a subfolder called docs/hacky-hours/
git submodule add https://github.com/empathetech/hacky-hours-docs.git docs/hacky-hours

# Save this change to your project
git add .gitmodules docs/hacky-hours
git commit -m "chore: add hacky-hours-docs as submodule"
```

### If you're cloning a project that already has this set up

When you clone the project for the first time, add `--recurse-submodules` so the framework files are downloaded too:

```bash
git clone --recurse-submodules https://github.com/your-username/your-project.git
```

If you already cloned without that flag:

```bash
git submodule update --init --recursive
```

### Updating to the latest framework version

```bash
cd docs/hacky-hours
git pull origin main
cd ../..
git add docs/hacky-hours
git commit -m "chore: update hacky-hours-docs submodule"
```

### Tell Claude where to look

Add this to your project's `CLAUDE.md`:

```markdown
## Hacky Hours Framework

This project uses the Hacky Hours documentation framework.
Framework artifacts live at `hacky-hours/` (default) or wherever you placed them.

Before starting work:
- For new features: read `hacky-hours/04-build/BACKLOG.md`
- For design decisions: read the relevant doc in `hacky-hours/02-design/`
- For security concerns: read `hacky-hours/02-design/SECURITY_PRIVACY.md` before any implementation that touches user data
- For licensing: read `hacky-hours/02-design/LICENSING.md` before adding any dependency or external service
```

---

## Option 2: CLAUDE.md Reference Snippet (quickest setup)

If you don't want to add a submodule, you can simply tell Claude where to find the framework on your computer. This works well if you have the framework checked out somewhere and want multiple projects to reference it.

Add to your project's `CLAUDE.md`:

```markdown
## Hacky Hours Framework

This project follows the Hacky Hours four-level documentation framework.
The framework reference lives at: /path/to/hacky-hours-docs/ (adjust to your local path)

When helping with design decisions, read the relevant template from the framework before making suggestions.
When helping with implementation, read `hacky-hours/02-design/SECURITY_PRIVACY.md` before proceeding.
When adding any dependency, read `hacky-hours/02-design/LICENSING.md` to check compatibility.
```

**Tradeoff:** This only works on machines where the framework is at that exact path. If you work on multiple computers or collaborate with others, they'll need the framework in the same location — or they'll need to update the path.

---

## Option 3: Manual Copy (simplest, but doesn't update)

For the simplest setup — or if you only need a document or two — just copy the files you need into your project:

```bash
cp -r path/to/hacky-hours-docs/02-design/ my-project/docs/design-framework/
```

**Tradeoff:** Your copy won't receive updates when the framework improves. This is fine for a stable reference, but if the framework adds new features or fixes issues, you won't see those changes unless you copy again manually.

---

## Related

- [fork-vs-clone.md](./fork-vs-clone.md)
- [CLAUDE.md](../../CLAUDE.md)
- [03-git-basics.md](../getting-started/03-git-basics.md)
