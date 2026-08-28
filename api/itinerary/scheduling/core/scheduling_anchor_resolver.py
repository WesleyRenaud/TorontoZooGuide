from __future__ import annotations

from ....shared.calendar_dates import DateValues
from ....types import Types
from ...validation.itinerary_arrival_time_validator import ItineraryArrivalTimeValidator
from ....zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


class SchedulingAnchorResolver():
   @classmethod
   def anchor_seconds(
         cls,
         zoo_hours_record: ZooHoursRecord | None,
         arrival_time: Types.ScheduleTimeKey,
         *,
         allow_early_admission: bool = False ) -> int | None:
      if arrival_time is not None:
         return DateValues.time_value_in_seconds( arrival_time )

      if zoo_hours_record is None:
         return None

      if allow_early_admission:
         return DateValues.time_value_in_seconds(
            ItineraryArrivalTimeValidator.earliest_arrival_time( zoo_hours_record ) )

      return DateValues.time_value_in_seconds( zoo_hours_record.open_time )


   @classmethod
   def covering_fixed_zoo_starts(
         cls,
         zoo_hours_record: ZooHoursRecord | None,
         arrival_time: Types.ScheduleTimeKey,
         fixed_zoo_start_times: list[ Types.ScheduleTimeKey ] | None = None,
         *,
         allow_early_admission: bool = False ) -> int | None:
      anchor_seconds = cls.anchor_seconds(
         zoo_hours_record,
         arrival_time,
         allow_early_admission=allow_early_admission )

      if anchor_seconds is None:
         return None

      for start_time in fixed_zoo_start_times or []:
         start_seconds = DateValues.time_value_in_seconds( start_time )

         if start_seconds is None:
            continue

         if start_seconds < anchor_seconds:
            anchor_seconds = start_seconds

      return anchor_seconds


   @classmethod
   def day_end_seconds(
         cls,
         zoo_hours_record: ZooHoursRecord | None,
         departure_time: Types.ScheduleTimeKey ) -> int | None:
      if zoo_hours_record is None:
         return None

      close_seconds = DateValues.time_value_in_seconds( zoo_hours_record.close_time )

      if close_seconds is None:
         return None

      if departure_time is None:
         return close_seconds

      departure_seconds = DateValues.time_value_in_seconds( departure_time )

      if departure_seconds is None:
         return close_seconds

      return min( close_seconds, departure_seconds )
