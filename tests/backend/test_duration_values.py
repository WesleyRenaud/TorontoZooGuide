from __future__ import annotations

import pytest

from api.shared.duration_values import normalize_duration_minutes
from api.shared.duration_values import normalize_duration_seconds


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( 0, None ),
      ( 7.2, 8 ),
      ( 8, 8 ),
      ( 20, 20 ),
   ]
)
def test_normalize_duration_minutes( value: float | None, expected: int | None ) -> None:
   assert normalize_duration_minutes( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( 0, None ),
      ( 0.5, 30 ),
      ( 7.2, 432 ),
      ( 8, 480 ),
      ( 20, 1200 ),
   ]
)
def test_normalize_duration_seconds( value: float | None, expected: int | None ) -> None:
   assert normalize_duration_seconds( value ) == expected
