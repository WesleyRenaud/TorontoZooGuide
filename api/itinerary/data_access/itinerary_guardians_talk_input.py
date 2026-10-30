from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class ItineraryGuardiansTalkInput:
   name: str
   start_time: Types.ScheduleTimeKey = None
   end_time: Types.ScheduleTimeKey = None
   location: str = ''
   enclosure_name: str | None = None
