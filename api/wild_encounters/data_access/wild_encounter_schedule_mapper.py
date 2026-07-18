from __future__ import annotations

from ...types import Row
from .wild_encounter_schedule_record import WildEncounterScheduleRecord


def map_wild_encounter_schedule_record( row: Row ) -> WildEncounterScheduleRecord:
   return WildEncounterScheduleRecord(
      name=row[ 'NAME' ],
      meeting_spot=row[ 'MEETING_SPOT' ],
      link=row[ 'LINK' ],
      maximum_duration=row[ 'MAXIMUM_DURATION' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ],
      schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
      schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
      monday=row[ 'MONDAY' ],
      tuesday=row[ 'TUESDAY' ],
      wednesday=row[ 'WEDNESDAY' ],
      thursday=row[ 'THURSDAY' ],
      friday=row[ 'FRIDAY' ],
      saturday=row[ 'SATURDAY' ],
      sunday=row[ 'SUNDAY' ],
      encounter_time=row[ 'ENCOUNTER_TIME' ],
      is_cancelled=row[ 'IS_CANCELLED' ] )



def map_wild_encounter_schedule_records( rows: list[ Row ] ) -> list[ WildEncounterScheduleRecord ]:
   return [
      map_wild_encounter_schedule_record( row )
      for row in rows
   ]
