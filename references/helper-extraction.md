# Helper Extraction

Extract helpers when the new helper gives a real concept a name, creates a clear contract, and reduces net complexity.

A successful extraction makes the caller easier to read, the extracted logic easier to name or test, and the behavior contract easier to verify. Moving lines into another function without reducing branching, data flow, dependency reach, review burden, or cognitive load is not a successful cleanup.

## Good Extraction Candidates

- Repeated logic with the same inputs, outputs, and error behavior.
- Long functions with separable stages such as parse, validate, transform, persist, or render.
- Logic that can be tested without I/O, framework state, or global mutation.
- Domain rules that benefit from a meaningful name.
- Dense expressions where a named intermediate concept is clearer than an inline chain.
- Pure calculations currently mixed into I/O, framework glue, or orchestration code.
- Repeated setup, normalization, or error mapping that already behaves as one concept.

## Poor Extraction Candidates

- Code used once where extraction only moves lines elsewhere.
- Helpers whose parameters are mostly pass-through state from a large outer scope.
- Generic utilities with vague names such as `handleData`, `processItem`, or `common`.
- Helpers that hide important ordering, locking, transaction, or error semantics.
- Helpers with Boolean flags or option bags that make call sites less readable than the original branches.
- Helpers created only to satisfy imagined future reuse.
- Helpers that must be exported only so tests or distant modules can reach them.
- Helpers that increase call depth without reducing conditional complexity or data flow.

## Before Extracting

- Search for an existing helper with the same contract before creating a new one.
- Identify the readability target: clearer caller intent, fewer repeated branches, shorter caller, narrower data shape, isolated pure logic, or simpler tests.
- Check whether inlining an existing weak helper would shrink the code more than extracting another one.
- Preserve public APIs, exported names, serialized shapes, error text, and framework-discovered entry points.
- Stop if the extraction requires broadening visibility, weakening types, or changing behavior to make the helper fit.

## Extraction Steps

1. Write down the helper contract: inputs, output, side effects, exceptions, and ordering assumptions.
2. Move the smallest coherent block first.
3. Pass only the data the helper needs; avoid forwarding broad context objects or mutable outer state.
4. Keep the helper private and near its callers unless there is proven reuse across modules.
5. Preserve names and behavior at call boundaries.
6. Add or update targeted tests for the helper if it contains meaningful branching.
7. Recheck the diff for net clarity: the caller should read simpler, duplication should drop, or validation should become easier.

## Naming

- Use domain-specific verbs and nouns that make the call site read naturally.
- Avoid names that describe implementation mechanics only.
- If no clear name exists, the block may not be ready to extract.

Prefer names that state the contract from the caller's point of view, such as `normalizeInvoiceLines` or `buildRetryPolicy`, over names that describe the act of extraction, such as `sharedLogic` or `doValidation`.

## Placement

- Keep one-off helpers in the same file as private functions or local closures when that keeps the behavior easier to read.
- Move helpers to a sibling domain module only when multiple files already need the same contract.
- Do not create or expand `utils`, `helpers`, `common`, or `shared` modules unless the project already has a narrow, domain-specific convention for them.
- Avoid barrel exports for new helpers unless the repository already uses that pattern for the same layer.
