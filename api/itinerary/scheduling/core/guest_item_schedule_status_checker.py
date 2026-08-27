from __future__ import annotations

from ....models import Itinerary
from ....models.itinerary_transportation import ItineraryTransportation
from ....shared.calendar_dates import DateValues
from ....shared.enums import ItineraryEventType
from ....types import ScheduleTimeKey


class GuestItemScheduleStatusChecker():
   @classmethod
   def has_schedule_times(
         cls,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey ) -> bool:
      return bool(
         DateValues.normalize_schedule_time_key( start_time )
         and DateValues.normalize_schedule_time_key( end_time ) )


   @classmethod
   def _transportation_counts_as_unscheduled(
         cls,
         transportation: ItineraryTransportation,
      ) -> bool:
      if transportation.added_as_attraction:
         return not cls.has_schedule_times(
            transportation.start_time,
            transportation.end_time )

      return not transportation.bulk_transit_evaluated


   @classmethod
   def has_unscheduled_guest_items( cls, itinerary: Itinerary ) -> bool:
      return any(
         not cls.has_schedule_times( item.start_time, item.end_time )
         for item in (
            *itinerary.animals,
            *itinerary.attractions,
         )
      ) or any(
         cls._transportation_counts_as_unscheduled( transportation )
         for transportation in itinerary.transportations
      ) or any(
         not cls.has_schedule_times( event.start_time, event.end_time )
         for event in itinerary.events
         if event.event_type not in (
               ItineraryEventType.ARRIVAL,
               ItineraryEventType.DEPARTURE,
         )
      )
