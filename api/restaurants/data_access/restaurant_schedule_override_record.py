from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class RestaurantScheduleOverrideRecord:
   restaurant: str
   override_start_date: Types.DateKey
   override_end_date: Types.DateKey | None
   is_closed: bool
   override_message: str | None
