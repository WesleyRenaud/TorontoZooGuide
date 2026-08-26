from __future__ import annotations

from dataclasses import dataclass

from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryAnimalSaveCarryover:
   species: str
   exhibit: str
   enclosure_name: str | None
   old_likelihood: int | None
   is_added: bool
   covered_by_talk: bool
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
