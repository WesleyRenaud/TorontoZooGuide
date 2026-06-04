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


def normalize_duration_seconds( duration_minutes: DurationInput ) -> int | None:
   if duration_minutes is None:
      return None

   if duration_minutes <= 0:
      return None

   return int( math.ceil( float( duration_minutes ) * 60 ) )


def duration_minutes_to_seconds( duration_minutes: int ) -> int:
   return duration_minutes * 60
