from __future__ import annotations

from dataclasses import dataclass

from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryAttractionSaveCarryover:
   name: str
   old_likelihood: int | None
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
