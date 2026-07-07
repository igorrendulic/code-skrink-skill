# Validation

Behavior-preserving cleanup is only complete when verification matches the risk.

## Before Editing

- Find existing tests that cover the target code.
- If coverage is unclear, run or inspect callers to identify observable behavior.
- For risky paths, add characterization tests before refactoring when practical.

## During Editing

- Prefer small commits or local checkpoints when the cleanup spans multiple files.
- Run targeted tests after each meaningful transformation.
- Use type checks, linters, and formatters according to the repository's existing workflow.

## After Editing

- Run targeted tests for changed modules.
- Run broader tests when shared helpers, public APIs, build config, or dependency boundaries changed.
- Manually exercise UI or CLI flows when automated coverage is weak.
- Compare generated outputs, snapshots, API responses, or serialized data when relevant.

## Reporting

Include:

- What changed structurally.
- What behavior was preserved.
- Which commands were run and whether they passed.
- Any verification gaps, skipped tests, or remaining risk.

