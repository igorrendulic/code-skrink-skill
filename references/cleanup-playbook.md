# Cleanup Playbook

Use this order when shrinking code. Earlier steps are usually safer and make later steps clearer.

## 1. Remove Proven Dead Code

- Search for references before deleting exported symbols, CLI commands, route handlers, migrations, or framework-discovered files.
- Check tests, docs, config files, dynamic imports, dependency injection containers, and registration lists.
- Delete code only when absence is established or the user accepts the risk.

## 2. Reuse Existing Code

Before introducing a new helper, abstraction, or utility:

- Search the repository for an equivalent implementation.
- Prefer extending an existing helper over creating a similar one.
- Keep helpers close to their domain unless they already serve multiple modules.
- Avoid creating generic `utils`, `helpers`, or `common` modules.

## 3. Collapse Incidental Duplication

- Merge repeated branches that compute the same value or differ only by constants.
- Prefer parameterizing data over parameterizing control flow.
- Keep duplicated code when two call sites are likely to evolve independently.

## 4. Simplify Conditionals

- Replace nested conditionals with guard clauses when it shortens the happy path.
- Name complex boolean expressions only when the name improves understanding.
- Avoid clever boolean algebra that obscures business rules.

## 5. Inline Weak Abstractions

- Inline helpers that are used once and do not clarify intent.
- Inline wrappers that only rename another function without enforcing a contract.
- Keep wrappers when they isolate dependencies, normalize errors, or encode domain language.

## 6. Split by Responsibility

When a file becomes difficult to navigate:

- Split along natural responsibility boundaries, not arbitrary line counts.
- Separate domain logic, I/O, parsing, API handlers, UI, and data models where appropriate.
- Prefer fewer cohesive files over many tiny files.
- Avoid introducing circular dependencies or excessive indirection.

## 7. Narrow Data Shapes

- Pass only the fields a function needs.
- Replace broad option bags with explicit parameters when call sites remain readable.
- Keep option objects when they improve clarity or extensibility.

## 8. Reduce Dependency Reach

- Keep pure logic independent of frameworks and I/O.
- Reduce unnecessary dependency coupling.
- Move imports only when it solves startup cost, dependency cycles, or architectural clarity—not for cosmetic reasons.