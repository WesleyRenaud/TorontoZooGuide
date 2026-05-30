from __future__ import annotations

from ...shared.date_values import DateValues
from ...types import ScheduleTimeKey
from ...zoo_hours.data_access.zoo_hours_record import ZooHoursRecord


def scheduling_anchor_minutes(
      zoo_hours_record: ZooHoursRecord,
      arrival_time: ScheduleTimeKey ) -> int:
   if arrival_time is not None:
      return DateValues.time_value_in_minutes( arrival_time )

   return DateValues.time_value_in_minutes( zoo_hours_record.open_time )


def scheduling_day_end_minutes(
      zoo_hours_record: ZooHoursRecord,
      departure_time: ScheduleTimeKey ) -> int:
   close_minutes = DateValues.time_value_in_minutes( zoo_hours_record.close_time )

   if departure_time is None:
      return close_minutes

   departure_minutes = DateValues.time_value_in_minutes( departure_time )

   return min( close_minutes, departure_minutes )
