# Worktree Isolation

Use this when isolated cleanup work is requested or useful. Isolation is optional for single-agent work, but it protects the current checkout and can preserve dependency caches.

## Order Of Preference

1. If already in an isolated worktree, use it.
2. If `treehouse` is installed and usable, lease a Treehouse worktree.
3. If Treehouse is unavailable, use a plain git worktree.
4. If git is unavailable, work in place and rely on file-scope checks.

## Detect Current State

```bash
git rev-parse --is-inside-work-tree
git rev-parse --git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
```

If `git-dir` differs from `git-common-dir` and the repo is not a submodule, the session is already in a linked worktree.

## Treehouse

Treehouse manages a reusable pool of git worktrees. Prefer its non-interactive lease flow for agent sessions:

```bash
path=$(treehouse get --lease)
cd "$path"
```

Release the lease when finished:

```bash
treehouse return "$path"
```

Treehouse is useful when repeated sessions should reuse dependency installs and build caches. Do not require it for one-off single-agent work. Its default root is `~/.treehouse/`, so managed sandboxes may block it unless that path is writable or the user approves escalation.

## Plain Git Worktree Fallback

Use this when Treehouse is not available or not appropriate:

```bash
git check-ignore -q .worktrees
git worktree add ".worktrees/<branch-name>" -b "<branch-name>"
```

Before creating a project-local worktree, ensure `.worktrees/` is ignored. If it is not ignored, ask before adding `.worktrees/` to `.gitignore`.

## In-Place Fallback

When git or filesystem permissions prevent worktree creation, work in the current directory. State that isolation was unavailable and run the file-scope guard before and after editing.
