# File Scope

Use this when the user asks to target a specific file, directory, glob, test group, module, or "only these files."

## Scope Contract

1. Restate the approved scope before editing.
2. Treat exact paths and globs as an allowlist.
3. Use `scripts/file_scope_guard.py` when available to snapshot or check changed files.
4. Before editing outside the allowlist, stop and list:
   - Path.
   - Intended change.
   - Why the change is necessary.
   - In-scope alternative, if one exists.
5. Continue only after explicit approval.

## Interpreting Scope

- Exact file: only that path is approved.
- Directory: all files under that directory are approved.
- Glob: paths matched by the glob are approved.
- "Tests for X": approve the relevant test files only, not production code.
- "Same module": approve the smallest directory or package that owns the target behavior.
- Generated files, lockfiles, snapshots, migrations, and fixtures are out of scope unless named or approved.

When a formatter or code generator could rewrite unrelated files, do not run it until either the output is constrained to approved paths or the user approves the affected paths.

## Guard CLI

From the skill directory, use the bundled guard:

```bash
python3 scripts/file_scope_guard.py snapshot --scope 'src/foo.ts' --state /tmp/code-shrink-scope.json
python3 scripts/file_scope_guard.py check --scope 'src/foo.ts' --state /tmp/code-shrink-scope.json
```

In git repositories, `check` detects staged, unstaged, deleted, renamed, and untracked files. Outside git repositories, create a snapshot before editing and compare against it after editing.

## Filesystem Sandboxing

Filesystem sandboxing is coarse containment. It can restrict writes to configured roots such as the workspace and `/tmp`, and it may block global paths such as `~/.treehouse/`.

Sandboxing usually does not express task intent like "only edit `src/foo.ts`." Use sandboxing to prevent writes outside permitted roots, and use the scope contract plus guard CLI to enforce fine-grained file allowlists inside the writable project.
