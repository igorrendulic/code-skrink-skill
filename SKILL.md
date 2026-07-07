---
name: code-shrink
description: Reduce code size and complexity while preserving behavior. Use when asked to shrink, simplify, deduplicate, split, clean up, or make code more maintainable without changing user-visible functionality; especially useful for large files, repeated logic, helper extraction, dead-code removal, and validation-focused refactors.
---

# Code Shrink

Shrink code deliberately: preserve behavior first, reduce surface area second, and keep changes easy to review, especially useful for large files, repeated logic, helper reuse/extraction, dead-code removal, and validation-focused refactors.

## Workflow

1. Establish the behavior contract before editing.
   - Read relevant tests, callers, public APIs, docs, and runtime entry points.
   - Identify behavior that must not change, including edge cases and error handling.
   - If the user names target files, directories, or globs, treat them as the approved edit scope and read [file-scope.md](references/file-scope.md).
   - If isolation is useful or requested, read [worktree-isolation.md](references/worktree-isolation.md) before editing.
2. Map the code shape.
   - Find duplicate branches, unused paths, overly broad abstractions, large functions, large files, and dependency boundaries.
   - Prefer local simplifications before introducing new abstractions.
3. Choose the smallest cleanup strategy that preserves behavior.
   - For general cleanup order and risk controls, read [cleanup-playbook.md](references/cleanup-playbook.md).
   - For repeated logic or long functions, read [helper-extraction.md](references/helper-extraction.md).
   - For files that are too large or mix responsibilities, read [file-splitting.md](references/file-splitting.md).
   - For verification strategy, read [validation.md](references/validation.md).
4. Edit in narrow, reviewable steps.
   - Keep unrelated formatting churn out of behavior-preserving refactors.
   - Do not combine cleanup with feature changes unless the user explicitly asks.
5. Validate with evidence.
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
