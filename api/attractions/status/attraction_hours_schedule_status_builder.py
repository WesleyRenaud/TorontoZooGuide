from __future__ import annotations

from ..scheduling.attraction_hours_schedule import AttractionHoursSchedule
from ...shared.calendar_dates import DateValues
from ...types import DateInput, TimeInput


class AttractionHoursScheduleStatusBuilder():
   @classmethod
   def build_hours_schedule(
         cls,
         attraction: str,
         start_date: DateInput,
         end_date: DateInput,
         weekday_start_time: TimeInput,
         weekday_end_time: TimeInput,
         weekend_holiday_start_time: TimeInput,
         weekend_holiday_end_time: TimeInput ) -> AttractionHoursSchedule:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )
      return AttractionHoursSchedule(
         attraction=attraction,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         weekday_start_time=weekday_start_time,
         weekday_end_time=weekday_end_time,
         weekend_holiday_start_time=weekend_holiday_start_time,
         weekend_holiday_end_time=weekend_holiday_end_time )
