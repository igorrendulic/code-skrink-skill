# Worktree Isolation

Use this before editing in git repositories. Isolation is required unless the user explicitly asks to work in place, the session is already in an isolated worktree, or worktree creation is unavailable after following the fallback rules.

Before creating a new worktree, check the current checkout for uncommitted work. Do not move or discard existing changes unless the user explicitly asks.

## Order Of Preference

1. If already in an isolated worktree, use it.
2. If `treehouse` is installed and usable, lease a Treehouse worktree.
3. If Treehouse is unavailable, use a plain git worktree.
4. If git is unavailable, work in place and rely on file-scope checks.

Use a branch named `code-shrink/<short-target>` unless the user provides a branch name. Use a filesystem-safe worktree path such as `<worktree-root>/code-shrink-<short-target>`.

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

Treehouse is useful when repeated sessions should reuse dependency installs and build caches. Its default root is `~/.treehouse/`, so managed sandboxes may block it unless that path is writable or the user approves escalation.

## Plain Git Worktree Fallback

Use this when Treehouse is not available or not appropriate.

Before creating a worktree, resolve the repository root and choose the worktree root:

```bash
repo_root=$(git rev-parse --show-toplevel)
worktree_root=

for candidate in .worktrees .worktree; do
  if [ -d "$repo_root/$candidate" ] && git -C "$repo_root" check-ignore -q "$candidate/"; then
    worktree_root="$repo_root/$candidate"
    break
  fi
done

if [ -z "$worktree_root" ]; then
  worktree_root=$(mktemp -d "${TMPDIR:-/tmp}/code-shrink-worktree.XXXXXX")
fi

git -C "$repo_root" worktree add "$worktree_root/code-shrink-<short-target>" -b "code-shrink/<short-target>"
```

Check `$repo_root/.worktrees` first, then `$repo_root/.worktree`. Use the first directory that both exists and is ignored by git. If both directories exist and are ignored, prefer `.worktrees/`.

If neither directory exists or the existing directory is not ignored, do not ask to modify `.gitignore`; create the worktree in a writable temp directory.

## In-Place Fallback

When git or filesystem permissions prevent worktree creation, work in the current directory. State that isolation was unavailable and run the file-scope guard before and after editing.

## Finish And Handoff

At completion, verify inside the worktree and report:

- Worktree path.
- Branch name.
- Git status.
- Diff summary.
- Tests or checks run.
- Any verification gaps.

Do not merge into `main` or another target branch unless the user explicitly asks. Provide exact next commands for the user to open a PR or merge locally.

For a local merge handoff, adapt these commands to the target branch and worktree branch:

```bash
git switch main
git pull --ff-only
git merge --no-ff code-shrink/<short-target>
git worktree remove <worktree-root>/code-shrink-<short-target>
git branch -d code-shrink/<short-target>
```

For Treehouse worktrees, return the lease only after the branch or PR is safely handed off, or after the user confirms the worktree is no longer needed:

```bash
treehouse return "$path"
```

## Explicit Merge

Only merge when the user asks. Before merging, confirm the target branch, update it with `git pull --ff-only`, merge the worktree branch, rerun verification, and remove the worktree only after the merge and verification succeed.
