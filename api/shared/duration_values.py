from __future__ import annotations

import math

from ..types import DurationInput


def normalize_duration_minutes(
      duration_minutes: DurationInput ) -> int | None:
   if duration_minutes is None:
      return None

   if duration_minutes <= 0:
      return None

   return max( 1, math.ceil( duration_minutes ) )
