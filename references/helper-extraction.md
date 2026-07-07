# Helper Extraction

Extract helpers to make code smaller only when the new helper has a clear contract.

## Good Extraction Candidates

- Repeated logic with the same inputs, outputs, and error behavior.
- Long functions with separable stages such as parse, validate, transform, persist, or render.
- Logic that can be tested without I/O, framework state, or global mutation.
- Domain rules that benefit from a meaningful name.

## Poor Extraction Candidates

- Code used once where extraction only moves lines elsewhere.
- Helpers whose parameters are mostly pass-through state from a large outer scope.
- Generic utilities with vague names such as `handleData`, `processItem`, or `common`.
- Helpers that hide important ordering, locking, transaction, or error semantics.

## Extraction Steps

1. Write down the helper contract: inputs, output, side effects, exceptions, and ordering assumptions.
2. Move the smallest coherent block first.
3. Keep the helper near its callers unless there is proven reuse across modules.
4. Preserve names and behavior at call boundaries.
5. Add or update targeted tests for the helper if it contains meaningful branching.

## Naming

- Use domain-specific verbs and nouns.
- Avoid names that describe implementation mechanics only.
- If no clear name exists, the block may not be ready to extract.

