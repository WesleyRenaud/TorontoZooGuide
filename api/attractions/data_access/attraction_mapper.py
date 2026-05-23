from __future__ import annotations

from collections.abc import Iterable

from .attraction_record import AttractionRecord
from .attraction_schedule_override_record import AttractionScheduleOverrideRecord
from .attraction_schedule_record import AttractionScheduleRecord
from ...types import Row


def map_attraction_record( row: Row ) -> AttractionRecord:
   return AttractionRecord(
      name=row[ 'NAME' ],
      free_with_admission=row[ 'FREE_WITH_ADMISSION' ],
      description=row[ 'DESCRIPTION' ],
      info_link=row[ 'INFO_LINK' ],
      hyperlink_text=row[ 'HYPERLINK_TEXT' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ],
      weekday_multiplier=row[ 'ATTRACTION_DAY_SEASONAL_WEEKDAY_MULTIPLIER' ],
      weekend_holiday_multiplier=row[ 'ATTRACTION_DAY_SEASONAL_WEEKEND_HOLIDAY_MULTIPLIER' ] )


def map_attraction_records( rows: Iterable[ Row ] ) -> list[ AttractionRecord ]:
   return [
      map_attraction_record( row )
      for row in rows
   ]


def map_attraction_schedule_record( row: Row ) -> AttractionScheduleRecord:
   return AttractionScheduleRecord(
      attraction=row[ 'ATTRACTION' ],
      schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
      schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
      monday=row[ 'MONDAY' ],
      tuesday=row[ 'TUESDAY' ],
      wednesday=row[ 'WEDNESDAY' ],
      thursday=row[ 'THURSDAY' ],
      friday=row[ 'FRIDAY' ],
      saturday=row[ 'SATURDAY' ],
      sunday=row[ 'SUNDAY' ],
      holidays_only=row[ 'HOLIDAYS_ONLY' ],
      schedule_message=row[ 'SCHEDULE_MESSAGE' ] )


def map_attraction_schedule_records( rows: Iterable[ Row ] ) -> list[ AttractionScheduleRecord ]:
   return [
      map_attraction_schedule_record( row )
      for row in rows
   ]


def map_attraction_schedule_override_record( row: Row ) -> AttractionScheduleOverrideRecord:
   return AttractionScheduleOverrideRecord(
      attraction=row[ 'ATTRACTION' ],
      override_start_date=row[ 'OVERRIDE_START_DATE' ],
      override_end_date=row[ 'OVERRIDE_END_DATE' ],
      is_closed=row[ 'IS_CLOSED' ],
      override_message=row[ 'OVERRIDE_MESSAGE' ] )


def map_attraction_schedule_override_records( rows: Iterable[ Row ] ) -> list[ AttractionScheduleOverrideRecord ]:
   return [
      map_attraction_schedule_override_record( row )
      for row in rows
   ]
