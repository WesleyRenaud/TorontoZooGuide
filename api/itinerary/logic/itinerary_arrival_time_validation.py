from __future__ import annotations

from .itinerary_schedule_time_order_validation import departure_follows_arrival
from ...shared.date_values import DateValues
from ...shared.enums import ItineraryErrorType
from ...types import ScheduleTimeKey
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


def earliest_arrival_minutes(
      zoo_hours_record: ZooHoursRecord ) -> int | None:
   return DateValues.time_value_in_minutes(
      earliest_arrival_time( zoo_hours_record ) )


def earliest_arrival_time(
      zoo_hours_record: ZooHoursRecord ) -> ScheduleTimeKey:
   return (
      zoo_hours_record.early_admission_time
      if zoo_hours_record.early_admission_time != None
      else zoo_hours_record.open_time )


def arrival_time_is_valid_for_zoo_hours(
      arrival_time: ScheduleTimeKey,
      zoo_hours_record: ZooHoursRecord,
      *,
      departure_time: ScheduleTimeKey ) -> ItineraryErrorType:
   arrival_minutes = DateValues.time_value_in_minutes( arrival_time )
   earliest_minutes = earliest_arrival_minutes( zoo_hours_record )
   last_admission_minutes = DateValues.time_value_in_minutes(
      zoo_hours_record.last_admission_time )

   if not earliest_minutes <= arrival_minutes <= last_admission_minutes:
      return ItineraryErrorType.TIME_OUT_OF_BOUNDS

   if not departure_follows_arrival( arrival_time, departure_time ):
      return ItineraryErrorType.TIME_ORDER_INVALID

   return ItineraryErrorType.SUCCESS
