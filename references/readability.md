# Readability

Use this when deciding whether a cleanup genuinely makes code easier to understand. The test is practical: would a maintainer who knows the project, but not this exact code, understand the result faster and with less risk of misreading behavior?

## Contents

- [Readability Targets](#readability-targets)
- [Decision Rules](#decision-rules)
- [Names](#names)
- [Explicitness](#explicitness)
- [Comments And Documentation](#comments-and-documentation)
- [Duplication And Abstraction](#duplication-and-abstraction)
- [Idiomatic Local Style](#idiomatic-local-style)
- [Responsibility Checks](#responsibility-checks)
- [Red Flags](#red-flags)

## Readability Targets

Prioritize changes that improve at least one of these:

- Intent: names and structure reveal what the code means, not only how it works.
- Flow: the main path is easy to follow, with edge cases and exits made explicit.
- Locality: related concepts live close enough that readers do not bounce between files unnecessarily.
- Responsibility: functions, classes, modules, and files have one clear reason to change.
- Idiom: code uses the language and project conventions naturally without becoming clever.
- Reviewability: the diff lets reviewers distinguish behavior preservation from cleanup.

Line count is not a target by itself. More lines can be more readable when they remove dense expressions, name intermediate concepts, or make error paths explicit.

## Decision Rules

Use these rules to choose the smallest useful cleanup:

| Situation | Prefer | Avoid |
| --- | --- | --- |
| Name hides the domain role | Rename private/local concept to domain language | Broad public rename without approval |
| Main path is buried in nesting | Guard clauses or named predicate | Clever boolean algebra |
| Transformation chain is dense | Named intermediate value | A comment that only explains the expression |
| Repeated code has one contract | Focused helper near callers | Generic utility or Boolean flags |
| Similar code may evolve separately | Keep limited duplication | Premature abstraction |
| File has multiple responsibilities | Split by existing responsibility boundary | Split by line count |

## Names

- Use names that describe the value's role in the current domain.
- Prefer a few informative words over cryptic abbreviations or numbered suffixes.
- Keep universal abbreviations such as `id`, `url`, `api`, and project-standard acronyms.
- Rename misleading names when the current name implies the wrong behavior, side effect, or data shape.
- Name Boolean functions and predicates so call sites read naturally, such as `isReady`, `hasPermission`, or `canRetry`.
- Name functions after the task they perform. If the task cannot be described in a short name, split the responsibility first.
- Do not rename public APIs, exported symbols, serialized fields, config keys, routes, CLI flags, or test snapshots unless the user approves the breaking change.

Avoid generic names unless their scope is tiny and obvious:

- Poor: `data`, `result`, `value`, `item`, `thing`, `manager`, `handler`, `process`.
- Better: names that carry domain meaning, such as `invoiceLines`, `validationErrors`, `retryPolicy`, or `activeSession`.

Example:

```text
Before: result = process(items)
After: validationErrors = validateInvoiceLines(invoiceLines)
```

The improved version tells the reader what kind of result exists, what domain object is being processed, and what task the function performs.

## Explicitness

Prefer code that states the intended condition or transformation directly.

- Replace nested conditionals with guard clauses when they reveal the normal path.
- Name complex conditions when the name explains a domain rule.
- Use intermediate variables when they make a transformation pipeline readable.
- Avoid nested ternaries and dense chains that require readers to keep a mental stack.
- Be careful with implicit truthiness when `0`, empty strings, empty collections, `None`, `null`, or `undefined` have distinct meanings.
- Prefer straightforward control flow over clever boolean algebra.

Explicit does not mean verbose. Remove wording, branches, or variables that repeat what the surrounding code already makes obvious.

Example:

```text
Before: if user and user.account and user.account.status == "active" and not user.account.locked:
After:  if accountCanReceivePayment(user.account):
```

Use the named predicate only when it captures a real domain rule and its implementation is easy to find. If the condition is simple and local, leave it inline.

## Comments And Documentation

Make the code carry as much meaning as it reasonably can, then keep comments for information the code cannot express.

- Delete comments that merely narrate the next line.
- Keep or add short comments that explain why behavior is surprising, constrained, risky, or tied to an external system.
- Preserve comments that document public API contracts, lifecycle ordering, performance constraints, security constraints, or non-obvious compatibility requirements.
- Update comments when cleanup changes structure; stale comments are worse than no comments.

Prefer a named helper or variable over a comment when the comment only supplies a missing concept name.

Example:

```text
Before: // remove orders too old to retry
        orders = orders.filter(...)
After:  retryableOrders = filterRetryableOrders(orders)
```

Keep comments for constraints the code cannot express, such as external API quirks, compatibility requirements, lifecycle ordering, or security assumptions.

## Duplication And Abstraction

Duplication is a readability problem when it makes reviewers compare near-copies or update behavior in several places. It is acceptable when two similar call sites are likely to evolve independently or abstraction would hide intent.

- Use the rule of three as a prompt to inspect repetition, not as an automatic extraction rule.
- Extract repeated logic only when the helper has a clear name, stable inputs, predictable output, and a useful contract.
- Prefer separate named functions over one parameterized function when the branches are conceptually different.
- Avoid option flags that create call sites like `run(true, false, true)`.
- Keep a small amount of duplication when a shared abstraction would introduce vague names, wide parameter lists, or unrelated responsibilities.

Example:

```text
Better helper: buildRetryPolicy(requestType)
Poor helper:   handleStuff(data, true, false)
```

The better helper names a stable concept. The poor helper hides branching behind unexplained arguments.

## Idiomatic Local Style

Readable code follows the repository's conventions first, then the language's common idioms.

- Read neighboring code and project instructions before changing style.
- Use language features that make intent obvious to readers of this codebase.
- Avoid replacing clear code with an idiom that only experts will parse quickly.
- Do not introduce a new style only because it is personally preferred.
- Use existing formatters and linters according to the repository workflow, but do not treat formatting as a substitute for clearer design.

## Responsibility Checks

Before extracting a helper, splitting a file, or renaming a concept, answer:

- What responsibility does this code have?
- What calls it, and what does it call?
- Which behavior, side effects, errors, and ordering must remain unchanged?
- Is this complexity essential to the domain, or accidental complexity from how it is expressed?
- Would the proposed change reduce what a reader must hold in memory?
- Does the new boundary hide meaningful complexity behind a smaller contract, or only move lines?

If the answers are unclear, read more context before editing.

## Red Flags

Stop and reassess when a cleanup:

- Optimizes for fewer lines while making behavior harder to parse.
- Changes tests because the refactor changed behavior.
- Removes error handling, cleanup, ordering, retries, or compatibility code because it looks noisy.
- Creates a helper that is harder to name than the code it replaces.
- Splits a file into shallow modules that expose most of their internals.
- Renames things away from project or domain vocabulary.
- Mixes readability cleanup with unrelated feature work.
