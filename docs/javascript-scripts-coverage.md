# Frontend scripts coverage

CI runs `npm run coverage:js` (via `npm run coverage` / `build`). Target is **100% line coverage** of included scripts, each with a mirrored test file.

## What counts

Included: `scripts/**/*.js`, minus patterns in
[`tools/coverage/jsCoverageExcludes.json`](../tools/coverage/jsCoverageExcludes.json).

| Omitted | Why |
|---|---|
| `scripts/strings.js`, `scripts/strings/**` | Pure copy catalogs |
| `scripts/*Bootstrap.js`, `scripts/**/*Bootstrap.js` | Page/console entry wiring |

**Views are not omitted.** They are DOM structure factories and should gain tests over time (same mocks as Fragments/Controllers).

## Progress

After the Node coverage table, `coverage:js` prints three counts over included scripts:

1. **Mirrored test files** — `scripts/foo/bar.js` → `tests/scripts/foo/bar.test.mjs`
2. **Fully line-covered** — 100% line coverage in the run (files never loaded count as 0%)
3. **Mirrored + fully covered** — the goal metric (dedicated test file and 100% lines)

Inventory helpers live in [`tools/coverage/jsScriptsCoverageInventory.js`](../tools/coverage/jsScriptsCoverageInventory.js).

## Growing coverage

Prefer new tests for Normalizers, Formatters, Checkers, Matchers, Resolvers, Keys, and Models before heavy Controllers. Mirror paths under `tests/scripts/` and follow [javascript-unit-test-style.md](javascript-unit-test-style.md).
