from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class ItineraryAttractionSaveCarryover:
   name: str
   old_likelihood: int | None
   start_time: Types.ScheduleTimeKey
   end_time: Types.ScheduleTimeKey
