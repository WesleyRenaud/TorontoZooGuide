from __future__ import annotations

import math


def normalize_duration_minutes(
      duration_minutes: float | int | None ) -> int | None:
   if duration_minutes is None:
      return None

   duration_value = float( duration_minutes )

   if duration_value <= 0:
      return None

   return max( 1, math.ceil( duration_value ) )
