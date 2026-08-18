from __future__ import annotations

from ....models import Itinerary
from ....shared.calendar_dates import DateValues
from ....shared.enums import ItineraryEventType
from ....types import ScheduleTimeKey


def has_itinerary_schedule_times(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   return bool(
      DateValues.normalize_schedule_time_key( start_time )
      and DateValues.normalize_schedule_time_key( end_time ) )


def itinerary_has_unscheduled_guest_items( itinerary: Itinerary ) -> bool:
   return any(
      not has_itinerary_schedule_times( item.start_time, item.end_time )
      for item in (
         *itinerary.animals,
         *itinerary.attractions,
         *itinerary.transportations,
      )
   ) or any(
      not has_itinerary_schedule_times( event.start_time, event.end_time )
      for event in itinerary.events
      if event.event_type not in (
            ItineraryEventType.ARRIVAL,
            ItineraryEventType.DEPARTURE,
      )
   )
