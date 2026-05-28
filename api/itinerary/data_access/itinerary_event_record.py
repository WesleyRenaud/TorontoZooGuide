from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ItineraryEventType
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryEventRecord:
   event_type: ItineraryEventType
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
