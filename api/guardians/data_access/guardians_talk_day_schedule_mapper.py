from __future__ import annotations

from .guardians_talk_day_schedule_record import GuardiansTalkDayScheduleRecord
from ...types import Types


class GuardiansTalkDayScheduleMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> GuardiansTalkDayScheduleRecord:
      return GuardiansTalkDayScheduleRecord(
         name=row[ 'NAME' ],
         location=row[ 'LOCATION' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         maximum_duration=row[ 'MAXIMUM_DURATION' ],
         talk_time=row[ 'TALK_TIME' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ GuardiansTalkDayScheduleRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
