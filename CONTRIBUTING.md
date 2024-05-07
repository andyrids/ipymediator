> [!NOTE]
> This file is a a work in progress.

## Git Commit Convention

### Summary

The [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/#summary) is a lightweight convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history; which makes it easier to write automated tools on top of

The commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Recommended commit types include: `build:`, `chore:`, `ci:`, `docs:`, `style:`, `refactor:`, `perf:` and `test:`.