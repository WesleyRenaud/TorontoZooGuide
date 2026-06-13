from __future__ import annotations

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
   open_minutes = DateValues.time_value_in_minutes( zoo_hours_record.open_time )
   close_minutes = DateValues.time_value_in_minutes( zoo_hours_record.close_time )

   if not open_minutes <= departure_minutes <= close_minutes:
      return ItineraryErrorType.TIME_OUT_OF_BOUNDS

   if not departure_follows_arrival( arrival_time, departure_time ):
      return ItineraryErrorType.TIME_ORDER_INVALID

   return ItineraryErrorType.SUCCESS
