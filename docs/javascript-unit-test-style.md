# JavaScript Unit Test Style

Enforced in CI by `tools/lint/jsUnitTestStyle.js` (`npm run lint:js`).

Coverage goals and omit policy for `scripts/` are in
[`javascript-scripts-coverage.md`](javascript-scripts-coverage.md).

Test **case** names and file layout follow the same rules as Python
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

## File layout

Keep this top-to-bottom order. Do not use `test.describe` / `describe` suites.

```
imports
constants
private helpers (function _... / const _... =)
installDomTestHooks / beforeEach / afterEach
all test('Test_...', ...) cases
```

Private helpers use a leading underscore, matching Python’s `def _...` helpers.

```js
function _cleanupPopups() {
   document.querySelector('.tzg-confirm')?.remove();
}

installDomTestHooks({
   after: () => {
      _cleanupPopups();
   },
});

test('Test_Shows_TestRendersPopup_ExpectOk', () => {
   ...
});
```

## Test case names

Default pattern:

`Test_[Method]_Test[Scenario]_Expect[Outcome]`

- **Method** — method or function under test, in PascalCase.
- **Scenario** — input or condition being exercised.
- **Outcome** — expected result or behavior.

```js
test('Test_Format_TestTrimmedTimes_ExpectJoined', () => {
   const morning = '11:00 AM';
   const afternoon = '2:00 PM';
   const times = [morning, afternoon];

   const formatted = JoinedTimesFormatter.format(times);

   assert.equal(formatted, `${morning}, ${afternoon}`);
});
```

Separate tests with two blank lines. Do not pack unrelated scenarios into one
`test()`; give each its own `Test_[Method]_Test[Scenario]_Expect[Outcome]` name.

Table-driven tests may use the short form `Test_[Method]` when a single test
covers a true mapping table (for example boolean conversions). Prefer a named
AAA case when the expected value is the same data as the input, just transformed.

## Arrange, act, assert

Every non-table test uses blank-line arrange / act / assert. Assign the act to a
named result. Do not label the sections with comments.

Expected values must come from arranged inputs or production constants — never
from a second copy of the same literal, and never from a number that was
calculated by hand.

```js
test('Test_AsTrimmedString_TestWhitespace_ExpectTrimmed', () => {
   const name = 'Amur Tiger';
   const value = `  ${name}  `;

   const trimmed = ValueNormalizer.asTrimmedString(value);

   assert.equal(trimmed, name);
});


test('Test_AsFiniteNumber_TestNumericString_ExpectNumber', () => {
   const value = '34';

   const number = ValueNormalizer.asFiniteNumber(value);

   assert.equal(number, Number(value));
});
```

Use `Position.FIRST` / `Position.LAST` and module constants instead of `0`, `-1`,
or copied hex/color/string literals that already live on the production object.

Enforcement covers every `tests/scripts/**/*.test.mjs` file.
