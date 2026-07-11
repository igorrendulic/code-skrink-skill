# code-shrink

Codex skill for making code easier to read while preserving behavior.

Install this repository directly into a Codex skills directory, or use a local checkout while developing the skill.

## Goal

`code-shrink` helps an agent make code clearer, simpler, and easier to review without changing user-visible behavior. It is meant for cleanup work such as:

- Improving unclear names and tangled control flow.
- Removing proven dead code.
- Deduplicating repeated logic.
- Extracting focused helpers.
- Splitting files by real responsibility boundaries.
- Inlining weak abstractions.
- Narrowing data shapes and dependency reach.
- Adding or choosing validation that proves behavior stayed stable and readability improved.

The skill is intentionally conservative. It prioritizes maintainer comprehension, behavior contracts, public API stability, scoped edits, and targeted verification over aggressive rewrites or line-count wins.

## What The Skill Optimizes For

- Preserve existing behavior first.
- Prefer code a future maintainer can understand faster.
- Accept a few more lines when explicitness, naming, or structure improves comprehension.
- Prefer deletion, inlining, and reuse before new abstractions.
- Keep helpers close to their domain.
- Avoid generic `utils`, `helpers`, or `common` dumping grounds.
- Split files only when ownership, dependency direction, testability, or reviewability improves.
- Keep diffs reviewable and avoid unrelated formatting churn.
- Validate with evidence matched to the risk of the cleanup.

## Repository Layout

- `SKILL.md`: entry point loaded by Codex when the skill triggers.
- `references/readability.md`: naming, explicitness, comments, idioms, DRY tradeoffs, and responsibility checks.
- `references/cleanup-playbook.md`: ordered cleanup strategy and risk controls.
- `references/file-scope.md`: explicit file-scope contract and guard usage.
- `references/helper-extraction.md`: when and how to extract helpers.
- `references/file-splitting.md`: when a file split is worthwhile.
- `references/library-replacement.md`: when maintained libraries may reduce owned complexity.
- `references/validation.md`: how to choose baseline, targeted, and broader checks.
- `references/worktree-isolation.md`: required git worktree isolation, handoff, and explicit merge guidance.
- `scripts/file_scope_guard.py`: verifies that changed files stay inside an approved scope.
- `install.sh`: installs this skill into a local Codex skills directory.

## How To Use

You do not need to tell `code-shrink` exactly which refactor to perform. If you invoke the skill without a specific cleanup instruction, it should inspect the available code, find high-confidence readability cleanup opportunities, make the safe behavior-preserving changes, and validate them.

Every cleanup pass includes a file-splitting assessment. The skill should report whether it performed a split, rejected specific split candidates, or found no credible split boundaries. It should still split files only when current code provides a real responsibility boundary.

Use a broad outcome-based prompt when you want the skill to decide what is worth doing:

```text
Use code-shrink.
Use code-shrink on this repo.
Use code-shrink on this package and make it easier to read.
Use code-shrink on src/foo and decide what cleanup is worth doing.
Use code-shrink only on src/foo.ts.
Use code-shrink on clip.py and improve readability, including any warranted file split.
```

The default behavior is:

- No specific scope: perform the fullest high-confidence readability cleanup across the repository or current working area, including file-splitting assessment.
- File, directory, glob, module, or package named: perform the fullest high-confidence readability cleanup inside that scope, including file-splitting assessment.
- Exact cleanup requested: do that cleanup instead of expanding into unrelated changes, but still assess and report file-splitting fit unless explicitly forbidden.

For broad repo-wide, package-wide, multi-file, or parallelizable cleanup, the skill uses `task-graph` first when that skill is installed or available in the current session. Exact narrow edits skip `task-graph`; if it is unavailable, `code-shrink` continues with its normal workflow.

High-confidence cleanup means the agent can justify the change from local evidence, such as clearer names, easier control flow, proven dead code, obvious duplication, weak one-use abstractions, narrower data flow, reduced dependency reach, or a file split with a clear responsibility boundary. It does not mean speculative rewrites, behavior changes, preference-only renames, or broad architecture redesign.

## Prompt Examples

Requests that should trigger this skill include:

```text
Use code-shrink.
Use code-shrink on src/foo.
Shrink this module without changing behavior.
Make this module easier to read without changing behavior.
Deduplicate the repeated validation logic in src/forms.
Split this large file if it has clear responsibility boundaries.
Clean up only src/foo.ts and its tests.
Remove dead code from this package and prove it is unused.
```

For best results, name the target files, directories, or globs when you want a bounded cleanup. You only need to specify the exact cleanup when you already know what change you want.

## Good Vs Over-Specified Prompts

Prefer prompts that describe the desired outcome:

```text
Use code-shrink on src/forms and make the code easier to read.
```

Use exact instructions only when the implementation choice matters:

```text
Use code-shrink on src/forms and only deduplicate the repeated validation logic.
```

## Scoped Edits

The skill supports an explicit file scope contract: when you ask it to target a file, directory, or glob, it should avoid touching anything else. If another file must change, it should list the proposed path and reason before editing.

The bundled guard can verify scope:

```bash
python3 scripts/file_scope_guard.py snapshot --scope 'src/foo.ts' --state /tmp/code-shrink-scope.json
python3 scripts/file_scope_guard.py check --scope 'src/foo.ts' --state /tmp/code-shrink-scope.json
```

In git repositories, `check` uses git status. Outside git, use `snapshot` before editing.

## Worktree Isolation

In git repositories, the skill works from an isolated worktree before editing unless the user explicitly asks to work in place, the session is already isolated, or worktree creation is unavailable after following the fallback rules. It can use Treehouse when installed to lease a reusable worktree pool entry, or plain `git worktree` otherwise. Plain git worktrees use an existing ignored `.worktrees/` or `.worktree/` directory at the repository root when available; otherwise they fall back outside the repository. Managed filesystem sandboxes may block Treehouse's default `~/.treehouse/` root unless that path is writable.

Before creating a worktree, check for existing uncommitted work and avoid moving or discarding it unless the developer explicitly asks.

The skill should not merge back into `main` or another target branch automatically. It reports the worktree path, branch, verification, and exact handoff commands; merging is only done when explicitly requested.

## Validation

Behavior-preserving cleanup is only complete when verification matches the risk and the result is easier to understand. Typical evidence includes:

- Reference searches before deleting code.
- Existing targeted tests for touched modules.
- Characterization tests for important behavior with weak coverage.
- Type checks or builds when imports, exports, or file boundaries change.
- Before/after CLI output, generated artifacts, API responses, or UI screenshots when automated tests are not enough.
- Final readability review for names, control flow, locality, responsibility boundaries, and reviewability.

The final report should say what changed structurally, what readability improved, what behavior was preserved, which checks passed, and which checks could not be run.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/igorrendulic/code-shrink-skill/main/install.sh | bash
```

By default, the installer copies the skill to `${CODEX_HOME:-$HOME/.codex}/skills/code-shrink`.

For a local checkout, run:

```bash
./install.sh
```

## Development Notes

Keep `SKILL.md` short and procedural. Put detailed guidance in `references/` and link it directly from `SKILL.md` so Codex can load only the relevant context.

When changing the skill:

1. Keep frontmatter limited to `name` and `description`.
2. Make sure every reference file used by the skill is linked from `SKILL.md`.
3. Test scripts with representative commands.
4. Run the skill validator when its dependencies are available.
5. Avoid adding general documentation files that are not needed by the agent at runtime.
