# Validation

Behavior-preserving cleanup is only complete when verification matches the risk.

Use this reference to choose evidence, not to run every possible check. The goal is to prove the visible contract stayed stable while the code became smaller, simpler, or easier to review.

## Before Editing

- Find existing tests that cover the target code.
- If coverage is unclear, run or inspect callers to identify observable behavior.
- Capture a baseline for behavior that is easy to compare: targeted test output, CLI output, rendered UI state, generated files, API responses, snapshots, or serialized data.
- For risky paths, add characterization tests before refactoring when practical.
- If characterization tests are impractical, write down the manual checks or sample inputs that will stand in for them before changing code.

## During Editing

- Prefer small commits or local checkpoints when the cleanup spans multiple files.
- Run targeted tests after each meaningful transformation.
- Use type checks, linters, and formatters according to the repository's existing workflow.
- Re-run the baseline check after transformations that move logic, change call order, alter imports, or delete code.
- Stop and reassess if a validation failure cannot be explained by the intended cleanup.

## After Editing

- Run targeted tests for changed modules.
- Run broader tests when shared helpers, public APIs, build config, or dependency boundaries changed.
- Manually exercise UI or CLI flows when automated coverage is weak.
- Compare generated outputs, snapshots, API responses, or serialized data when relevant.
- Confirm the final diff actually shrinks or simplifies the target: less duplication, fewer branches, narrower data flow, smaller dependency reach, clearer file ownership, or lower review burden.

## Match Checks To Cleanup Type

| Cleanup type | Minimum useful evidence |
| --- | --- |
| Dead-code removal | Reference search across code, tests, docs, config, generated entry lists, and dynamic registration points; targeted tests for remaining callers. |
| Helper extraction | Tests or sample inputs covering the extracted branches, errors, side effects, and ordering assumptions; caller tests proving behavior through the original entry point. |
| Conditional simplification | Cases for each preserved branch, including defaults, empty inputs, boundary values, and error paths. |
| File splitting or import movement | Targeted tests plus build/type checks that catch broken exports, cycles, framework discovery issues, and dependency boundary mistakes. |
| Dependency or data-shape narrowing | Tests for public APIs, serialization, config loading, plugin hooks, and external callers that might rely on the old shape. |
| UI cleanup | Before/after screenshots or manual interaction notes for affected states, responsive breakpoints, loading/empty/error states, and accessibility-relevant controls. |
| CLI/API cleanup | Before/after command output or response samples for success, validation failure, missing input, and error cases. |

## Characterization Tests

Add characterization tests when behavior is important but poorly covered and the cleanup changes control flow, parsing, normalization, error mapping, serialization, or public entry points.

- Test through the existing public entry point when possible.
- Preserve current behavior even when it looks odd, unless the user approves a behavior change.
- Prefer a few representative edge cases over broad test scaffolding that makes the cleanup larger than the code being shrunk.
- Keep tests focused on observable behavior, not internal helper boundaries that may disappear during cleanup.

Skip new tests only when the change is trivial, existing coverage is clearly adequate, or the repository has no practical test harness for the target. In that case, compensate with baseline comparison or manual checks and report the gap.

## Reporting

Include:

- What changed structurally.
- What behavior was preserved.
- Which baseline, targeted, and broad checks were run and whether they passed.
- Any verification gaps, skipped tests, or remaining risk.
