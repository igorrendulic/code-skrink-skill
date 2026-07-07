# code-shrink

Codex skill for reducing code size and complexity while preserving behavior.

Use this repository as the source folder for installing the `code-shrink` skill into a Codex skills directory.

## Goal

`code-shrink` helps an agent make code smaller, clearer, and easier to review without changing user-visible behavior. It is meant for cleanup work such as:

- Removing proven dead code.
- Deduplicating repeated logic.
- Extracting focused helpers.
- Splitting files by real responsibility boundaries.
- Inlining weak abstractions.
- Narrowing data shapes and dependency reach.
- Adding or choosing validation that proves behavior stayed stable.

The skill is intentionally conservative. It prioritizes behavior contracts, public API stability, scoped edits, and targeted verification over aggressive rewrites.

## What The Skill Optimizes For

- Preserve existing behavior first.
- Prefer deletion, inlining, and reuse before new abstractions.
- Keep helpers close to their domain.
- Avoid generic `utils`, `helpers`, or `common` dumping grounds.
- Split files only when ownership, dependency direction, testability, or reviewability improves.
- Keep diffs reviewable and avoid unrelated formatting churn.
- Validate with evidence matched to the risk of the cleanup.

## Repository Layout

- `SKILL.md`: entry point loaded by Codex when the skill triggers.
- `references/cleanup-playbook.md`: ordered cleanup strategy and risk controls.
- `references/file-scope.md`: explicit file-scope contract and guard usage.
- `references/helper-extraction.md`: when and how to extract helpers.
- `references/file-splitting.md`: when a file split is worthwhile.
- `references/validation.md`: how to choose baseline, targeted, and broader checks.
- `references/worktree-isolation.md`: optional isolation guidance with Treehouse or git worktrees.
- `scripts/file_scope_guard.py`: verifies that changed files stay inside an approved scope.
- `install.sh`: installs this skill into a local Codex skills directory.

## Usage Examples

Requests that should trigger this skill include:

```text
Shrink this module without changing behavior.
Deduplicate the repeated validation logic in src/forms.
Split this large file if it has clear responsibility boundaries.
Clean up only src/foo.ts and its tests.
Remove dead code from this package and prove it is unused.
```

For best results, name the target files, directories, or globs, and mention any behavior that must remain stable.

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

Before creating a worktree, check for existing uncommitted work and avoid moving or discarding it unless the developer explicitly asks.

## Validation

Behavior-preserving cleanup is only complete when verification matches the risk. Typical evidence includes:

- Reference searches before deleting code.
- Existing targeted tests for touched modules.
- Characterization tests for important behavior with weak coverage.
- Type checks or builds when imports, exports, or file boundaries change.
- Before/after CLI output, generated artifacts, API responses, or UI screenshots when automated tests are not enough.

The final report should say what changed structurally, what behavior was preserved, which checks passed, and which checks could not be run.

## Install

```bash
./install.sh
```

By default, the installer copies the skill to `${CODEX_HOME:-$HOME/.codex}/skills/code-shrink`.

## Development Notes

Keep `SKILL.md` short and procedural. Put detailed guidance in `references/` and link it directly from `SKILL.md` so Codex can load only the relevant context.

When changing the skill:

1. Keep frontmatter limited to `name` and `description`.
2. Make sure every reference file used by the skill is linked from `SKILL.md`.
3. Test scripts with representative commands.
4. Run the skill validator when its dependencies are available.
5. Avoid adding general documentation files that are not needed by the agent at runtime.
