# Python Unit Test Style

Enforced in CI by `tools/lint/pythonUnitTestStyle.py` (`npm run lint:py`).

## Test file names

- One test file per production module.
- Mirror the `api/` path under `tests/api/`.
- Use the `_tests.py` suffix.

| Production file | Test file |
|---|---|
| `api/models/animal_diff.py` | `tests/api/models/animal_diff_tests.py` |
| `api/itinerary/scheduling/items/schedule_item_travel_time_calculator.py` | `tests/api/itinerary/scheduling/items/schedule_item_travel_time_calculator_tests.py` |

The test file stem must match the production module stem exactly. Do not add extra suffixes, and do not create multiple test files for the same production module.

```python
# ❌ BAD — extra suffix; animal_coordinator.py already has animal_coordinator_tests.py
# tests/api/animals/coordinators/animal_coordinator_saved_itinerary_tests.py

# ✅ GOOD
# tests/api/animals/coordinators/animal_coordinator_tests.py
```

## Test function names

Default pattern:

`Test_[Method]_Test[Scenario]_Expect[Outcome]`

- **Method** — method or function under test, in PascalCase.
- **Scenario** — input or condition being exercised.
- **Outcome** — expected result or behavior.

```python
def Test_WalkNodeIdForAnimal_TestKnownAnimal_ExpectResolvedNode() -> None:
   ...

def Test_GetRestaurantNames_TestProviderNames_ExpectReturned() -> None:
   ...
```

Parametrized table-driven tests may use the short form `Test_[Method]` when decorated with `@pytest.mark.parametrize`:

```python
@pytest.mark.parametrize( 'value, expected', [ ( True, True ), ( 0, False ) ] )
def Test_AsBoolean( value: Any, expected: bool ) -> None:
   ...
```

## Helpers and tests grouped

Keep this top-to-bottom order. Do not place helpers, constants, or fixtures between `Test_` functions.

```
imports
constants
private helpers (def _...)
module-level test data / stubs
@pytest.fixture definitions
all Test_... functions
```

## Imports

All `import` and `from ... import ...` statements must appear at the top of the file, after any `from __future__` imports and the module docstring. Never place imports inside functions, test bodies, or class bodies.

```python
# ❌ BAD
def Test_Build_TestUntimedEncounter_ExpectTalkOnly() -> None:
   from dataclasses import dataclass, replace

# ✅ GOOD
from dataclasses import dataclass, replace
```

Enforced by `tools/lint/pythonImportStyle.py`.

## Request connection stubs

Do not define a local `StubConnection` class to satisfy `Types.Connection` typing. Use the shared helpers in `tests/api/api_test_support/request_connection_test_support.py`:

- `STUB_REQUEST_CONNECTION` — when a test passes a connection object directly
- `stub_request_connection` pytest fixture (in `tests/api/conftest.py`) — when coordinators call `RequestConnectionProvider.get()`

If a test needs connection behavior (for example `commit()`), define a focused stub in that file only, as in `opening_schedule_conflict_saver_tests.py`.
