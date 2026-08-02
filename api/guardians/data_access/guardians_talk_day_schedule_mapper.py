from __future__ import annotations

from .guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from ...types import Row


def map_guardians_talk_day_schedule_record(
      row: Row ) -> GuardiansTalkDayScheduleRecord:
   return GuardiansTalkDayScheduleRecord(
      name=row[ 'NAME' ],
      location=row[ 'LOCATION' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ],
      maximum_duration=row[ 'MAXIMUM_DURATION' ],
      talk_time=row[ 'TALK_TIME' ] )


def map_guardians_talk_day_schedule_records(
      rows: list[ Row ] ) -> list[ GuardiansTalkDayScheduleRecord ]:
   return [
      map_guardians_talk_day_schedule_record( row )
      for row in rows
   ]
