from __future__ import annotations

from ...types import Types


class AttractionHoursSchedule:
   def __init__(
         self,
         attraction: str,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None,
         weekday_start_time: Types.ScheduleTimeKey,
         weekday_end_time: Types.ScheduleTimeKey,
         weekend_holiday_start_time: Types.ScheduleTimeKey,
         weekend_holiday_end_time: Types.ScheduleTimeKey ) -> None:
      self.attraction = attraction
      self.start_date = start_date
      self.end_date = end_date
      self.weekday_start_time = weekday_start_time
      self.weekday_end_time = weekday_end_time
      self.weekend_holiday_start_time = weekend_holiday_start_time
      self.weekend_holiday_end_time = weekend_holiday_end_time
