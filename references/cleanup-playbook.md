# Cleanup Playbook

Use this order when shrinking code. Earlier steps are usually safer and make later steps clearer.

## 1. Pin The Behavior Boundary

- Identify the observable behavior that must remain stable before editing.
- Treat public APIs, exported names, CLI flags, config keys, route paths, database shapes, serialized formats, and error text as contracts.
- Note the shrink target: fewer branches, less duplication, smaller file, narrower data flow, fewer dependencies, or simpler review surface.
- Stop if the cleanup goal requires changing behavior or compatibility.

## 2. Remove Proven Dead Code

- Search for references before deleting exported symbols, CLI commands, route handlers, migrations, or framework-discovered files.
- Check tests, docs, config files, dynamic imports, dependency injection containers, reflection hooks, code generation inputs, and registration lists.
- Remove obsolete tests, fixtures, docs, config, and dependency entries only when they served the deleted path.
- Delete code only when absence is established or the user accepts the risk.

## 3. Reuse Existing Code

Before introducing a new helper, abstraction, or utility:

- Search the repository for an equivalent implementation.
- Prefer extending an existing helper over creating a similar one.
- Keep helpers close to their domain unless they already serve multiple modules.
- Avoid creating generic `utils`, `helpers`, or `common` modules.

## 4. Replace Commodity Code Deliberately

- Prefer existing repo helpers first.
- For generic, high-maintenance functionality, research maintained libraries before preserving local code or hand-rolling another abstraction.
- Add or swap a dependency only when it reduces owned complexity, maintenance cost, line count, or readability burden enough to justify supply-chain, compatibility, and runtime risk.
- Read [library-replacement.md](library-replacement.md) before replacing local functionality with a third-party library.

## 5. Collapse Incidental Duplication

- Merge repeated branches that compute the same value or differ only by constants.
- Prefer parameterizing data over parameterizing control flow.
- Keep duplicated code when two call sites are likely to evolve independently.

## 6. Simplify Conditionals

- Replace nested conditionals with guard clauses when it shortens the happy path.
- Name complex boolean expressions only when the name improves understanding.
- Avoid clever boolean algebra that obscures business rules.

## 7. Inline Weak Abstractions

- Inline helpers that are used once and do not clarify intent.
- Inline wrappers that only rename another function without enforcing a contract.
- Remove pass-through layers, aliases, and compatibility shims only after checking external callers and release expectations.
- Keep wrappers when they isolate dependencies, normalize errors, or encode domain language.

## 8. Narrow Data Shapes

- Pass only the fields a function needs.
- Replace broad option bags with explicit parameters when call sites remain readable.
- Keep option objects when they improve clarity or extensibility.
- Remove intermediate data structures that only mirror another shape without validation, normalization, or naming value.

## 9. Reduce Dependency Reach

- Keep pure logic independent of frameworks and I/O.
- Reduce unnecessary dependency coupling.
- Move imports only when it solves startup cost, dependency cycles, or architectural clarity, not for cosmetic reasons.
- Delete dependencies only after checking build config, plugins, generated code, tests, and runtime entry points.

## 10. Split by Responsibility

When a file becomes difficult to navigate:

- Split along natural responsibility boundaries, not arbitrary line counts.
- Separate domain logic, I/O, parsing, API handlers, UI, and data models where appropriate.
- Prefer fewer cohesive files over many tiny files.
- Avoid introducing circular dependencies or excessive indirection.

## 11. Recheck The Diff

- Confirm the change reduces net code, complexity, dependency reach, or review burden.
- Look for code that was merely moved, renamed, or abstracted without making behavior easier to verify.
- Run validation matched to the touched behavior before reporting the cleanup as complete.
