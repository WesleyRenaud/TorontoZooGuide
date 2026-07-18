from __future__ import annotations

from .guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from ...types import Row


def map_guardians_talk_schedule_record( row: Row ) -> GuardiansTalkScheduleRecord:
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



def map_guardians_talk_schedule_records(
      rows: list[ Row ] ) -> list[ GuardiansTalkScheduleRecord ]:
   return [
      map_guardians_talk_schedule_record( row )
      for row in rows
   ]
