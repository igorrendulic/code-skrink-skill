---
name: code-shrink
description: Reduce code size and complexity while preserving behavior. Use when asked to shrink, simplify, deduplicate, split, clean up, or make code more maintainable without changing user-visible functionality; especially useful for large files, repeated logic, helper extraction, dead-code removal, and validation-focused refactors.
---

# Code Shrink

Shrink code deliberately: preserve behavior first, reduce surface area second, and keep changes easy to review, especially useful for large files, repeated logic, helper reuse/extraction, dead-code removal, and validation-focused refactors.

## Default Behavior

When the user invokes this skill without a specific cleanup instruction, perform the fullest high-confidence behavior-preserving cleanup that the current scope supports.

- If the user gives no narrower scope, inspect the repository or current working area and clean up all high-confidence opportunities found.
- If the user names files, directories, globs, modules, or packages, treat that as the approved scope and perform full high-confidence cleanup inside it.
- If the user specifies an exact cleanup, follow that request instead of expanding into unrelated cleanup.
- Treat cleanup as high-confidence only when local evidence supports it: proven dead code, obvious duplication, weak one-use abstractions, simpler conditionals, narrower data flow, reduced dependency reach, or a file split with a clear responsibility boundary.
- Do not use "full cleanup" as permission for speculative rewrites, behavior changes, broad architecture redesign, or touching files outside an explicit scope.

## Workflow

1. Coordinate broad cleanup when task-graph is available.
   - For repo-wide, package-wide, multi-file, or clearly parallelizable cleanup work, use the `task-graph` skill first if it is installed or available in the current session.
   - Use `task-graph` to create or follow project-local task files, then apply this skill's behavior-preserving cleanup, scope, and validation rules inside each task.
   - Skip `task-graph` for exact narrow edits such as one requested file, one named function, or one specific refactor.
   - If `task-graph` is unavailable, continue with this workflow directly.
2. Establish the behavior contract before editing.
   - Read relevant tests, callers, public APIs, docs, and runtime entry points.
   - Identify behavior that must not change, including edge cases and error handling.
   - If the user names target files, directories, or globs, treat them as the approved edit scope; read [file-scope.md](references/file-scope.md) and use `scripts/file_scope_guard.py` when available.
   - In git repositories, read [worktree-isolation.md](references/worktree-isolation.md) and work from an isolated worktree before editing unless the user explicitly asks to work in place, the session is already in an isolated worktree, or worktree creation is unavailable after following the fallback rules.
3. Map the code shape.
   - Find duplicate branches, unused paths, overly broad abstractions, large functions, large files, and dependency boundaries.
   - If local code implements commodity functionality that a maintained library may replace, read [library-replacement.md](references/library-replacement.md).
   - Prefer local simplifications before introducing new abstractions.
4. Choose the smallest cleanup strategy that preserves behavior.
   - For general cleanup order and risk controls, read [cleanup-playbook.md](references/cleanup-playbook.md).
   - For repeated logic or long functions, read [helper-extraction.md](references/helper-extraction.md).
   - For files that are too large or mix responsibilities, read [file-splitting.md](references/file-splitting.md).
   - For verification strategy, read [validation.md](references/validation.md).
5. Edit in narrow, reviewable steps.
   - Keep unrelated formatting churn out of behavior-preserving refactors.
   - Do not combine cleanup with feature changes unless the user explicitly asks.
   - Recheck the diff after each logical cleanup and stop if the change only moves complexity around.
6. Validate with evidence.
   - Run existing targeted tests first, then broader checks based on blast radius.
   - If tests are missing, add focused characterization tests when feasible.
   - Report any verification that could not be run.

## Operating Rules

- Honor explicit file scope. Edit only approved files or globs; before touching anything else, list the path, intended change, reason, and in-scope alternative, then wait for explicit user approval.
- Preserve public names, module boundaries, serialized formats, CLI flags, config keys, and error semantics unless the user explicitly approves a breaking change.
- Prefer deletion, inlining, reuse of existing helpers, and narrower helpers over framework-level abstractions.
- Search for existing helpers before creating new helpers.
- Do not create generic `utils`, `helpers`, or `common` dumping grounds.
- Do not split a file only because it is long; split when responsibilities, dependency direction, or reviewability improve.
- Stop and reassess if a cleanup requires speculative behavior changes.
- Do not run broad formatters, generators, migrations, or codemods when the output may touch files outside approved scope unless the user approves those paths first.
