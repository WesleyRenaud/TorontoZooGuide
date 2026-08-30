from __future__ import annotations

import pytest

from api.shared.duration_values import DurationValues


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
def Test_NormalizeMinutes( value: float | None, expected: int | None ) -> None:
   assert DurationValues.normalize_minutes( value ) == expected


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
def Test_NormalizeSeconds( value: float | None, expected: int | None ) -> None:
   assert DurationValues.normalize_seconds( value ) == expected
