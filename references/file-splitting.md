# File Splitting

Split files only when doing so makes the code easier to understand, navigate, test, or evolve. Line count alone is not a reason to split a file.

Each resulting file should have one clear responsibility, cohesive internals, and a stable reason to exist.

For code-shrink work, a split should reduce practical complexity: smaller review units, narrower dependency reach, clearer tests, or less code in the original hot path. Moving the same complexity into more files is not a successful shrink.

## Architecture Heuristics

Use these checks to decide whether a split creates a better module boundary or only rearranges code:

- Locality: after the split, a reader should understand one concept with less bouncing between files.
- Depth: the new module should hide meaningful complexity behind a smaller, stable contract.
- Deletion test: deleting the new module should concentrate complexity back into the owner; if it only moves lines back, the module is probably shallow.
- Real seam: the boundary should be supported by existing responsibilities, callers, tests, imports, dependency direction, or different reasons to change.
- Shallow-module warning: avoid splits where the new file's public surface is nearly as complex as its implementation.

Treat these as filters, not permission for broad architecture redesign. If a split needs new abstractions, renamed concepts, or changed behavior to look good, stop and keep the cleanup smaller.

## Before Splitting

- Pin the behavior contract: public exports, side effects, error text, serialized data, route behavior, CLI flags, and config keys.
- Identify the shrink target: smaller entry point, isolated pure logic, narrower imports, easier tests, or removed duplication after extraction.
- Check existing callers and tests so the new module boundary follows current use, not imagined reuse.
- Check whether the proposed boundary improves locality and depth; reject shallow modules that only move lines.
- Decide which file owns the public API after the split.
- Stop if the only expected benefit is a lower line count.

## Split When

- The file contains multiple responsibilities or ownership boundaries.
- Different parts of the file have different reasons to change.
- Tests or callers naturally target one subset of the file.
- Imports reveal mixed layers such as UI, persistence, networking, framework glue, and domain logic in one file.
- Pure logic is mixed with framework-bound or I/O-heavy code.
- A smaller module can have a stable public contract.
- The extracted module makes one concept easier to understand locally.
- A split reduces cognitive load without increasing dependency complexity.

## Avoid Splitting When

- The split would create circular imports.
- The split would increase public API surface without reducing complexity.
- The new files would be named after vague buckets such as `utils`, `helpers`, `common`, or `misc`.
- Most functions need most of the same private state.
- The split only moves code without improving dependency direction, testability, navigation, or reviewability.
- The new module is shallow: its interface exposes nearly as much complexity as the implementation hides.
- The result would be many tiny files that are harder to understand than the original file.
- The split depends on imagined future reuse rather than current structure.
- The original file is still the easiest place to understand ordering, transactions, locks, retries, or cleanup behavior.
- Most names would need to become exported only so the split can compile.

## Practical Pattern

1. Identify stable seams from existing callers, tests, imports, and responsibilities.
2. Extract pure domain logic before framework-bound glue.
3. Move private types or helper functions with the logic that owns them.
4. Keep helpers local when they are used by only one module.
5. Keep entry points and public exports stable, even if they delegate internally.
6. Preserve behavior, error semantics, serialized formats, route contracts, CLI flags, and config keys.
7. Avoid adding new abstraction layers only to make the split possible.
8. Add barrel exports only if the project already uses them.
9. Update tests and imports mechanically after the split.
10. Run the smallest relevant validation after each logical split.
11. Recheck the diff for net clarity: fewer responsibilities per file, simpler imports, or easier tests.

## Natural Extraction Targets

- Type definitions, schemas, or contracts shared across modules.
- Pure transformation, parsing, normalization, and validation logic.
- Domain rules that can be tested without framework or I/O dependencies.
- Adapters for external services, storage, queues, APIs, or SDKs.
- API handlers or controllers that mostly coordinate other logic.
- UI subcomponents with independent state, rendering concerns, or test boundaries.
- Test fixtures, builders, and test-only helpers when they obscure the main test intent.

## Dependency Direction

Prefer splits that make dependencies point inward toward stable domain logic.

Good direction:

```text
entrypoint / UI / route
        ↓
application / orchestration
        ↓
domain logic / pure helpers
        ↓
types / contracts
```

Avoid this direction:

```text
domain logic / pure helpers
        ↓
entrypoint / UI / route / framework
```

If a proposed split creates this direction, extract a smaller pure module or keep the code together.

## Public API Control

- Preserve existing imports for external callers when possible.
- Keep newly extracted functions private unless another module already needs them.
- Prefer one owner for re-exporting public names.
- Do not export internal helpers only to test them; test through the behavior when practical.
- When direct tests are useful, extract a cohesive pure module with a meaningful public contract.

## State And Ordering

Be cautious when splitting code that depends on shared mutable state, lifecycle order, transactions, retries, caching, cleanup, subscriptions, or locks.

Before moving that code, write down:

- Which state is read and written.
- Which operations must happen before or after others.
- Which errors are intentionally swallowed, wrapped, retried, or propagated.
- Which cleanup steps must run on success, failure, and cancellation.

If the split makes these rules harder to see, keep the code together or extract a smaller pure calculation instead.
