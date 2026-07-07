# code-shrink

Codex skill for reducing code size while preserving behavior.

Use this repository as a source folder for installing the `code-shrink` skill into a Codex skills directory.

## Scoped Edits

The skill supports an explicit file scope contract: when you ask it to target a file, directory, or glob, it should avoid touching anything else. If another file must change, it should list the proposed path and reason before editing.

The bundled guard can verify scope:

```bash
python3 scripts/file_scope_guard.py snapshot --scope 'src/foo.ts' --state /tmp/code-shrink-scope.json
python3 scripts/file_scope_guard.py check --scope 'src/foo.ts' --state /tmp/code-shrink-scope.json
```

In git repositories, `check` uses git status. Outside git, use `snapshot` before editing.

## Worktree Isolation

For repeated sessions, the skill can use Treehouse when installed to lease a reusable worktree pool entry. For one-off work, plain `git worktree` or in-place work is enough. Managed filesystem sandboxes may block Treehouse's default `~/.treehouse/` root unless that path is writable.

## Install

```bash
./install.sh
```

By default, the installer copies the skill to `${CODEX_HOME:-$HOME/.codex}/skills/code-shrink`.
