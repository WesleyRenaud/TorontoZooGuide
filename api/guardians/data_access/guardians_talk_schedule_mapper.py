from __future__ import annotations

from .guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from ...types import Types


class GuardiansTalkScheduleMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> GuardiansTalkScheduleRecord:
      return GuardiansTalkScheduleRecord(
         name=row[ 'NAME' ],
         location=row[ 'LOCATION' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ],
         maximum_duration=row[ 'MAXIMUM_DURATION' ],
         schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
         schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
         monday=row[ 'MONDAY' ],
         tuesday=row[ 'TUESDAY' ],
         wednesday=row[ 'WEDNESDAY' ],
         thursday=row[ 'THURSDAY' ],
         friday=row[ 'FRIDAY' ],
         saturday=row[ 'SATURDAY' ],
         sunday=row[ 'SUNDAY' ],
         talk_time=row[ 'TALK_TIME' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ GuardiansTalkScheduleRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
