from __future__ import annotations

import math

from ..types import Types


class DurationValues():
   @classmethod
   def normalize_minutes(
         cls,
         duration_minutes: Types.DurationInput ) -> int | None:
      if duration_minutes is None:
         return None

      if duration_minutes <= 0:
         return None

      return max( 1, math.ceil( duration_minutes ) )


   @classmethod
   def normalize_seconds(
         cls,
         duration_minutes: Types.DurationInput ) -> int | None:
      if duration_minutes is None:
         return None

      if duration_minutes <= 0:
         return None

      return int( math.ceil( float( duration_minutes ) * 60 ) )


   @classmethod
   def minutes_to_seconds(
         cls,
         duration_minutes: int ) -> int:
      return duration_minutes * 60
