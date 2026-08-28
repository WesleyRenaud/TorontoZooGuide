from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums import ItineraryEventType
from ...types import Types


@dataclass( frozen=True )
class ItineraryEventRecord:
   event_type: ItineraryEventType
   start_time: Types.ScheduleTimeKey
   end_time: Types.ScheduleTimeKey
