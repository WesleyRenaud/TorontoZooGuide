from __future__ import annotations

from .itinerary_arrival_time_validation import earliest_arrival_time
from .itinerary_schedule_time_order_validation import departure_follows_arrival
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryErrorType
from ...types import ScheduleTimeKey
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


def departure_time_is_valid_for_zoo_hours(
      departure_time: ScheduleTimeKey,
      zoo_hours_record: ZooHoursRecord,
      *,
      arrival_time: ScheduleTimeKey ) -> ItineraryErrorType:
   departure_minutes = DateValues.time_value_in_minutes( departure_time )
   earliest_minutes = DateValues.time_value_in_minutes(
      earliest_arrival_time( zoo_hours_record ) )
   close_minutes = DateValues.time_value_in_minutes( zoo_hours_record.close_time )

   if (
         departure_minutes is None
         or earliest_minutes is None
         or close_minutes is None
         or not earliest_minutes <= departure_minutes <= close_minutes
   ):
      return ItineraryErrorType.TIME_OUT_OF_BOUNDS

   if not departure_follows_arrival( arrival_time, departure_time ):
      return ItineraryErrorType.TIME_ORDER_INVALID

   return ItineraryErrorType.SUCCESS
