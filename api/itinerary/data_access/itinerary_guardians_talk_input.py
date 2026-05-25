from __future__ import annotations

from dataclasses import dataclass

from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryGuardiansTalkInput:
   name: str
   start_time: ScheduleTimeKey = None
   end_time: ScheduleTimeKey = None
