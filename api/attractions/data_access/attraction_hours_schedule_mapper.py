from __future__ import annotations

from .attraction_hours_schedule_record import AttractionHoursScheduleRecord
from ...types import Row


class AttractionHoursScheduleMapper():
   @classmethod
   def map_record( cls, row: Row ) -> AttractionHoursScheduleRecord:
      return AttractionHoursScheduleRecord(
         attraction=row[ 'ATTRACTION' ],
         schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
         schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
         weekday_start_time=row[ 'WEEKDAY_START_TIME' ],
         weekday_end_time=row[ 'WEEKDAY_END_TIME' ],
         weekend_holiday_start_time=row[ 'WEEKEND_HOLIDAY_START_TIME' ],
         weekend_holiday_end_time=row[ 'WEEKEND_HOLIDAY_END_TIME' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ AttractionHoursScheduleRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
