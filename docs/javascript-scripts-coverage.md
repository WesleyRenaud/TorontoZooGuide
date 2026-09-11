# Frontend scripts coverage

CI runs `npm run coverage:js` (via `npm run coverage` / `build`). Target is **100% line coverage** of included scripts, each with a mirrored test file (`scripts/foo/bar.js` → `tests/scripts/foo/bar.test.mjs`).

## What counts

Included: `scripts/**/*.js`, minus patterns in
[`tools/coverage/jsCoverageExcludes.json`](../tools/coverage/jsCoverageExcludes.json).

| Omitted | Why |
|---|---|
| `scripts/strings.js`, `scripts/strings/**` | Pure copy catalogs |
| `scripts/*Bootstrap.js`, `scripts/**/*Bootstrap.js` | Page/console entry wiring |

**Views are not omitted.** They are DOM structure factories and should be covered with tests (same mocks as Fragments/Controllers).

## Growing coverage

Prefer new tests for Normalizers, Formatters, Checkers, Matchers, Resolvers, Keys, and Models before heavy Controllers. Mirror paths under `tests/scripts/` and follow [javascript-unit-test-style.md](javascript-unit-test-style.md).
