# File Splitting

Split files only when doing so makes the code easier to understand, navigate, test, or evolve. Line count alone is not a reason to split a file.

Each resulting file should have one clear responsibility, cohesive internals, and a stable reason to exist.

## Split When

- The file contains multiple responsibilities or ownership boundaries.
- Different parts of the file have different reasons to change.
- Tests or callers naturally target one subset of the file.
- Imports reveal mixed layers such as UI, persistence, networking, framework glue, and domain logic in one file.
- Pure logic is mixed with framework-bound or I/O-heavy code.
- A smaller module can have a stable public contract.
- A split reduces cognitive load without increasing dependency complexity.

## Avoid Splitting When

- The split would create circular imports.
- The split would increase public API surface without reducing complexity.
- The new files would be named after vague buckets such as `utils`, `helpers`, `common`, or `misc`.
- Most functions need most of the same private state.
- The split only moves code without improving dependency direction, testability, navigation, or reviewability.
- The result would be many tiny files that are harder to understand than the original file.
- The split depends on imagined future reuse rather than current structure.

## Practical Pattern

1. Identify stable seams from existing callers, tests, imports, and responsibilities.
2. Extract pure domain logic before framework-bound glue.
3. Keep helpers local when they are used by only one module.
4. Keep entry points and public exports stable.
5. Preserve behavior, error semantics, serialized formats, route contracts, CLI flags, and config keys.
6. Avoid adding new abstraction layers only to make the split possible.
7. Add barrel exports only if the project already uses them.
8. Update tests and imports mechanically after the split.
9. Run the smallest relevant validation after each logical split.

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