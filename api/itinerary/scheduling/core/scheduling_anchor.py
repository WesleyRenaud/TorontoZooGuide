from __future__ import annotations

from ....shared.calendar_dates import DateValues
from ....types import ScheduleTimeKey
from ...validation.itinerary_arrival_time_validator import ItineraryArrivalTimeValidator
from ....zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


def scheduling_anchor_seconds(
      zoo_hours_record: ZooHoursRecord | None,
      arrival_time: ScheduleTimeKey,
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


def scheduling_anchor_seconds_covering_fixed_zoo_starts(
      zoo_hours_record: ZooHoursRecord | None,
      arrival_time: ScheduleTimeKey,
      fixed_zoo_start_times: list[ ScheduleTimeKey ] | None = None,
      *,
      allow_early_admission: bool = False ) -> int | None:
   anchor_seconds = scheduling_anchor_seconds(
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


def scheduling_day_end_seconds(
      zoo_hours_record: ZooHoursRecord | None,
      departure_time: ScheduleTimeKey ) -> int | None:
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
