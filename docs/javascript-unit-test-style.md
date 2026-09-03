# JavaScript Unit Test Style

Enforced in CI by `tools/lint/jsUnitTestStyle.js` (`npm run lint:js`).

Test **case** names follow the same rule as Python
([`docs/python-unit-test-style.md`](python-unit-test-style.md)). The name is the
string passed to Node’s `test()` (or `it()`).

## Test file names

- One test file per production module.
- Mirror the `scripts/` path under `tests/scripts/`.
- Use the `.test.mjs` suffix (not `_tests.mjs`).
- `npm run test:js` discovers files via `tests/scripts/**/*.test.mjs` (no barrel import file).

| Production file | Test file |
|---|---|
| `scripts/shared/joinedTimesFormatter.js` | `tests/scripts/shared/joinedTimesFormatter.test.mjs` |
| `scripts/api/valueNormalizer.js` | `tests/scripts/api/valueNormalizer.test.mjs` |

## Test case names

Default pattern:

`Test_[Method]_Test[Scenario]_Expect[Outcome]`

- **Method** — method or function under test, in PascalCase.
- **Scenario** — input or condition being exercised.
- **Outcome** — expected result or behavior.

```js
test('Test_Format_TestTrimmedTimes_ExpectJoined', () => {
   assert.equal(
      JoinedTimesFormatter.format(['11:00 AM', '2:00 PM']),
      '11:00 AM, 2:00 PM'
   );
});
```

Table-driven tests may use the short form `Test_[Method]` when a single test
covers multiple input/output pairs:

```js
test('Test_AsBoolean', () => {
   const cases = [
      [true, true],
      [0, false],
   ];

   for (const [value, expected] of cases) {
      assert.equal(ValueNormalizer.asBoolean(value), expected);
   }
});
```

`describe(...)` suite titles are not checked.

## Opt-in enforcement

`tools/lint/jsUnitTestStyle.json` uses an include list. Add a test file when its
titles follow this convention; leave legacy prose titles out until they are
renamed.
