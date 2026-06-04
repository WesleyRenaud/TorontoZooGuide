from __future__ import annotations

from ...shared.date_values import DateValues
from ...types import ScheduleTimeKey
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


def scheduling_anchor_seconds(
      zoo_hours_record: ZooHoursRecord | None,
      arrival_time: ScheduleTimeKey ) -> int | None:
   if arrival_time is not None:
      return DateValues.time_value_in_seconds( arrival_time )

   if zoo_hours_record is None:
      return None

   return DateValues.time_value_in_seconds( zoo_hours_record.open_time )


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
