from __future__ import annotations

from ..shared.enums import ItineraryEventType
from ..types import ScheduleTimeKey


class ItineraryEvent:
   def __init__(
         self,
         event_type: ItineraryEventType,
         start_time: ScheduleTimeKey = None,
         end_time: ScheduleTimeKey = None ) -> None:
      self.event_type = event_type
      self.start_time = start_time
      self.end_time = end_time


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'event_type': self.event_type.value,
         'start_time': self.start_time,
         'end_time': self.end_time,
         'type': 'itineraryEvent',
      }
