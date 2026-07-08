# Library Replacement

Use this when local code implements generic functionality that may be better delegated to a maintained third-party library.

The goal is not to add dependencies by default. The goal is to reduce owned code, maintenance load, line count, and readability burden when an external library is clearly a better owner of the problem.

## Research When

- Local code implements commodity behavior such as parsing, validation, diffing, date/time handling, markdown, schema conversion, CLI parsing, file watching, retries, caching, formatting, protocol glue, or API client plumbing.
- The implementation is long, fragile, duplicated, hard to test, or full of edge cases already handled by mature packages.
- The code exists mainly to adapt to a public standard, wire format, protocol, or ecosystem convention.
- The repository already depends on a library that can cover the behavior with a smaller wrapper.

## Research Sources

- Browse GitHub, package registries, official docs, changelogs, release notes, issue trackers, security advisories, and migration guides.
- Prefer primary sources and current maintenance signals over blog posts or old examples.
- Check the repository's existing dependency manager, lockfile, framework, runtime, bundler, and platform constraints before recommending a package.

## Evaluation Checklist

- Behavior fit: API covers the current contract, edge cases, error semantics, serialization, and platform needs.
- Maintenance: recent releases, active issue triage, clear ownership, stable public API, and realistic upgrade path.
- Risk: license, security history, transitive dependency weight, bundle size, startup/runtime cost, and supply-chain exposure.
- Integration: type support where relevant, testability, tree-shaking or build compatibility, ESM/CJS or language-version compatibility, and supported runtimes.
- Migration cost: local adapter size, call-site churn, lockfile changes, config changes, and future readability.

## Decision Rule

Replace local code only when the library reduces owned complexity enough to justify the new dependency risk.

Keep local code when the behavior is domain-specific, small, stable, security-sensitive, performance-critical, or the library forces awkward adapters that hide the original contract.

Prefer a thin domain wrapper around an external library when the wrapper preserves local error semantics, isolates dependency churn, or keeps public APIs stable. Do not wrap a library only to rename its API.

## Validation

- Capture baseline behavior before replacing code.
- Add or update tests for compatibility edge cases, error paths, serialization, and public entry points.
- Verify dependency manifest and lockfile changes are intentional.
- Run targeted tests, type checks, build checks, and any runtime flow affected by the dependency.
- Recheck the final diff for net shrink: less owned code, clearer call sites, smaller maintenance surface, or fewer custom edge cases.
