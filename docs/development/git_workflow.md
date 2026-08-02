# Git Workflow & Commit Conventions

This document specifies the branching strategy, commit message standards, and pull request guidelines for Almora.

---

## Branch Naming Conventions

Branches must use descriptive prefixes followed by a short summary in `kebab-case`:

| Prefix | Use Case | Example |
| :--- | :--- | :--- |
| `feature/` | New features or functionality | `feature/settings-validation` |
| `fix/` | Bug fixes and patches | `fix/string-settings-length-check` |
| `docs/` | Documentation additions or updates | `docs/add-git-workflow` |
| `refactor/` | Code refactoring without behavioral changes | `refactor/core-settings-cleanup` |
| `chore/` | Maintenance, tooling, or dependency updates | `chore/update-pytest-config` |

---

## Conventional Commits Standard

Commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <short summary>

[optional body]
```

### Commit Types:
* **`feat`**: A new feature for the user or system.
* **`fix`**: A bug fix.
* **`docs`**: Documentation changes only.
* **`style`**: Formatting, missing semi-colons, whitespace fixes (no logic change).
* **`refactor`**: Code change that neither fixes a bug nor adds a feature.
* **`test`**: Adding missing tests or correcting existing tests.
* **`chore`**: Changes to the build process, tool configuration, or auxiliary libraries.
* **`draft`**: New draft, unstable version, no tests.
* **`wip`**: Stand for work in progess, usually changes from draft commit but still unstable.

### Examples:
```bash
git commit -m "docs(core): add docstrings to settings2.py"
git commit -m "feat(core): add IntSettings range validation"
git commit -m "fix(cli): correct configuration file loading path"
git commit -m "feat(settings): implement settings branch hierarchy

Introduce the Settings, SettingsBranch, and SettingsItem
structure with runtime validation and dynamic attribute
access."
```