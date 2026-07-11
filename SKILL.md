---
name: code-shrink
description: Use when code should be made easier to read, simplified, shrunk, deduplicated, split, cleaned up, or made more maintainable without changing user-visible behavior; especially for unclear names, tangled control flow, large files, repeated logic, weak abstractions, dead code, and validation-focused refactors.
---

# Code Shrink

Make code easier to understand while preserving behavior. Smaller code is useful only when it lowers cognitive load; accept a few more lines when clearer names, explicit control flow, or better responsibility boundaries help a future maintainer understand the code faster.

## Default Behavior

When the user invokes this skill without a specific cleanup instruction, perform the fullest high-confidence readability cleanup the approved scope supports.

- If no scope is given, inspect the repository or current working area and clean up high-confidence opportunities, including file-splitting assessment.
- If files, directories, globs, modules, or packages are named, treat them as the approved scope and clean up inside it, including file-splitting assessment.
- If an exact cleanup is requested, do that cleanup instead of expanding into unrelated work, but still assess and report file-splitting fit unless explicitly forbidden.
- Treat a cleanup as high-confidence only when local evidence shows it preserves behavior and improves comprehension: clearer names, simpler control flow, reduced duplication, removed dead code, narrower data flow, better locality, or a file split with a real responsibility boundary.
- Do not use cleanup as permission for speculative rewrites, behavior changes, broad architecture redesign, cosmetic churn, or touching files outside the approved scope.

## Workflow

1. Coordinate broad cleanup when task-graph is available.
   - For repo-wide, package-wide, multi-file, or clearly parallelizable cleanup work, use the `task-graph` skill first if it is installed or available in the current session.
   - Use `task-graph` to create or follow project-local task files, then apply this skill's behavior, readability, scope, and validation rules inside each task.
   - Skip `task-graph` for exact narrow edits such as one requested file, one named function, or one specific refactor.
2. Establish the behavior contract before editing.
   - Read relevant tests, callers, public APIs, docs, and runtime entry points.
   - Identify behavior that must not change, including edge cases, side effects, ordering, and error handling.
   - If the user names target files, directories, or globs, treat them as the approved edit scope; read [file-scope.md](references/file-scope.md) and use `scripts/file_scope_guard.py` when available.
   - In git repositories, read [worktree-isolation.md](references/worktree-isolation.md) and work from an isolated worktree before editing unless the user explicitly asks to work in place, the session is already in an isolated worktree, or worktree creation is unavailable after following the fallback rules.
3. Map the readability problems.
   - Read [readability.md](references/readability.md) for naming, explicitness, comments, idioms, DRY tradeoffs, and responsibility checks.
   - Find unclear names, misleading abstractions, dense expressions, deep nesting, scattered related logic, repeated branches, large functions, large files, mixed responsibilities, and dependency boundaries.
   - Always assess possible file splits across the approved scope; look for responsibility boundaries that improve locality, module depth, testability, dependency direction, or reviewability rather than line count.
   - If local code implements commodity functionality that a maintained library may replace, read [library-replacement.md](references/library-replacement.md).
4. Choose the smallest readability strategy that preserves behavior.
   - For general cleanup order and risk controls, read [cleanup-playbook.md](references/cleanup-playbook.md).
   - For repeated logic or long functions, read [helper-extraction.md](references/helper-extraction.md).
   - For every cleanup pass, consider file splitting and read [file-splitting.md](references/file-splitting.md) before deciding whether to split.
   - For verification strategy, read [validation.md](references/validation.md).
5. Edit in narrow, reviewable steps.
   - Prefer changes that make the caller, public entry point, or next maintainer's path through the code simpler.
   - Keep unrelated formatting churn out of behavior-preserving refactors.
   - Do not combine cleanup with feature changes unless the user explicitly asks.
   - Recheck the diff after each logical cleanup and stop if the change only moves complexity around or makes intent harder to see.
   - Be able to point to concrete before/after readability evidence: clearer names, flatter flow, better locality, less duplication, narrower data, or a smaller review surface.
6. Validate with evidence.
   - Run existing targeted tests first, then broader checks based on blast radius.
   - If tests are missing, add focused characterization tests when feasible.
   - Review the final diff for behavior preservation and readability improvement.
   - Report any verification that could not be run.

## Operating Rules

- Preserve public names, module boundaries, serialized formats, CLI flags, config keys, and error semantics unless the user explicitly approves a breaking change.
- Honor explicit file scope. Edit only approved files or globs; before touching anything else, list the path, intended change, reason, and in-scope alternative, then wait for explicit user approval.
- Prefer clarity over cleverness. A direct loop, guard clause, or named intermediate value is often better than a compact chain that requires a mental pause.
- Prefer deletion, renaming, inlining, reuse of existing helpers, and narrower helpers over framework-level abstractions.
- Search for existing helpers before creating new helpers.
- Do not create generic `utils`, `helpers`, or `common` dumping grounds.
- Do not split a file only because it is long; split when responsibilities, dependency direction, locality, testability, or reviewability improve.
- For every cleanup, report how file splitting was considered: splits performed, split candidates rejected, or no credible split boundaries found.
- Stop and reassess if a cleanup requires speculative behavior changes or makes tests pass only by modifying expected behavior.
- Do not run broad formatters, generators, migrations, or codemods when the output may touch files outside approved scope unless the user approves those paths first.

## Done Means

- The code's observable behavior is unchanged.
- The final code is easier to read by local project standards, not just shorter.
- The diff is narrow enough to review.
- File-splitting fit was assessed and reported.
- Verification evidence matches the risk of the cleanup.
