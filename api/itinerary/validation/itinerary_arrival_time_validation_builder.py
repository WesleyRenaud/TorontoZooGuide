from __future__ import annotations

from .itinerary_schedule_time_order_validation_builder import ItineraryScheduleTimeOrderValidationBuilder
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryErrorType
from ...types import ScheduleTimeKey
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


class ItineraryArrivalTimeValidationBuilder():
   @classmethod
   def earliest_arrival_minutes(
         cls,
         zoo_hours_record: ZooHoursRecord ) -> int | None:
      return DateValues.time_value_in_minutes(
         cls.earliest_arrival_time( zoo_hours_record ) )


   @classmethod
   def earliest_arrival_time(
         cls,
         zoo_hours_record: ZooHoursRecord ) -> ScheduleTimeKey:
      return (
         zoo_hours_record.early_admission_time
         if zoo_hours_record.early_admission_time != None
         else zoo_hours_record.open_time )


   @classmethod
   def earliest_allowed_arrival_minutes(
         cls,
         zoo_hours_record: ZooHoursRecord,
         fixed_zoo_start_times: list[ ScheduleTimeKey ] | None = None ) -> int | None:
      earliest_minutes = cls.earliest_arrival_minutes( zoo_hours_record )

      for start_time in fixed_zoo_start_times or []:
         start_minutes = DateValues.time_value_in_minutes( start_time )

         if start_minutes is None:
            continue

         if earliest_minutes is None or start_minutes < earliest_minutes:
            earliest_minutes = start_minutes

      return earliest_minutes


   @classmethod
   def validate_for_zoo_hours(
         cls,
         arrival_time: ScheduleTimeKey,
         zoo_hours_record: ZooHoursRecord,
         *,
         departure_time: ScheduleTimeKey,
         fixed_zoo_start_times: list[ ScheduleTimeKey ] | None = None ) -> ItineraryErrorType:
      arrival_minutes = DateValues.time_value_in_minutes( arrival_time )
      earliest_minutes = cls.earliest_allowed_arrival_minutes(
         zoo_hours_record,
         fixed_zoo_start_times )
      last_admission_minutes = DateValues.time_value_in_minutes(
         zoo_hours_record.last_admission_time )

      if (
            arrival_minutes is None
            or earliest_minutes is None
            or last_admission_minutes is None
            or not earliest_minutes <= arrival_minutes <= last_admission_minutes
      ):
         return ItineraryErrorType.TIME_OUT_OF_BOUNDS

      if not ItineraryScheduleTimeOrderValidationBuilder.departure_follows_arrival(
            arrival_time,
            departure_time ):
         return ItineraryErrorType.TIME_ORDER_INVALID

      return ItineraryErrorType.SUCCESS
