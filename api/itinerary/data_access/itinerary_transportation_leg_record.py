from __future__ import annotations

from dataclasses import dataclass

from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryTransportationLegRecord:
   transportation: str
   from_station: str
   to_station: str
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
