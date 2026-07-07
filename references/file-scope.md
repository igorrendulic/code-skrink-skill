# File Scope

Use this when the user asks to target a specific file, directory, glob, test group, module, or "only these files."

## Scope Contract

1. Restate the approved scope before editing.
2. Treat exact paths, directories, and globs as an allowlist.
3. If the scope is inferred from language such as "same module" or "tests for X," state the inferred paths before editing.
4. Use `scripts/file_scope_guard.py` when available:
   - In non-git projects, run `snapshot` before editing.
   - After scoped editing, run `check` before reporting completion.
5. Before editing outside the allowlist, stop and list:
   - Path.
   - Intended change.
   - Why the change is necessary.
   - In-scope alternative, if one exists.
6. Continue only after explicit approval.

## Interpreting Scope

- Exact file: only that path is approved.
- Directory: all files under that directory are approved.
- Glob: paths matched by the glob are approved.
- "Tests for X": approve the relevant test files only, not production code.
- "Same module": approve the smallest directory or package that owns the target behavior, and state that inferred scope before editing.
- Generated files, lockfiles, snapshots, migrations, and fixtures are out of scope unless named or approved.

If the user approves multiple files, directories, or globs, combine them into one allowlist. A file only needs to match one approved scope.

## Workflow

Before editing:

- Confirm the allowlist in plain language.
- If the repository is not a git repository, create a guard snapshot.
- If the working tree already has changes, distinguish known pre-existing changes from changes you make during the task.

After editing:

- Run the guard check when the guard is available.
- If the guard reports only approved paths, continue with normal validation.
- If the guard reports out-of-scope paths that were already dirty before the task, report them as pre-existing.
- If the guard reports out-of-scope paths created by this task, stop and ask for approval before continuing or remediating.

When a formatter or code generator could rewrite unrelated files, do not run it until either the output is constrained to approved paths or the user approves the affected paths. Prefer commands that accept explicit target files. If a broad formatter, generator, migration, or codemod is approved, run the guard immediately afterward and report any out-of-scope changes.

## Guard CLI

From the skill directory, use the bundled guard.

Single-file scope:

```bash
python3 scripts/file_scope_guard.py snapshot --scope 'src/foo.ts' --state /tmp/code-shrink-scope.json
python3 scripts/file_scope_guard.py check --scope 'src/foo.ts' --state /tmp/code-shrink-scope.json
```

Multiple approved scopes:

```bash
python3 scripts/file_scope_guard.py check --scope 'src/foo.ts' --scope 'tests/foo.test.ts' --state /tmp/code-shrink-scope.json
```

Run from outside the project or skill directory with `--root`:

```bash
python3 scripts/file_scope_guard.py check --root /path/to/project --scope 'src/foo.ts' --state /tmp/code-shrink-scope.json
```

In git repositories, `check` uses `git status` and detects staged, unstaged, deleted, renamed, copied, and untracked files. In this mode, `--state` is optional because git is the baseline. Outside git repositories, create a snapshot before editing and compare against it after editing.

## Filesystem Sandboxing

Filesystem sandboxing is coarse containment. It can restrict writes to configured roots such as the workspace and `/tmp`, and it may block global paths such as `~/.treehouse/`.

Sandboxing usually does not express task intent like "only edit `src/foo.ts`." Use sandboxing to prevent writes outside permitted roots, and use the scope contract plus guard CLI to enforce fine-grained file allowlists inside the writable project.
