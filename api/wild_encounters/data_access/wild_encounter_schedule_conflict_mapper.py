from __future__ import annotations

from ...types import Types
from .wild_encounter_schedule_conflict_record import WildEncounterScheduleConflictRecord


class WildEncounterScheduleConflictMapper():
   @classmethod
   def map_record(
         cls,
         row: Types.Row ) -> WildEncounterScheduleConflictRecord:
      return WildEncounterScheduleConflictRecord(
         wild_encounter=row[ 'WILD_ENCOUNTER' ],
         encounter_time=row[ 'ENCOUNTER_TIME' ],
         schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
         schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
         monday=row[ 'MONDAY' ],
         tuesday=row[ 'TUESDAY' ],
         wednesday=row[ 'WEDNESDAY' ],
         thursday=row[ 'THURSDAY' ],
         friday=row[ 'FRIDAY' ],
         saturday=row[ 'SATURDAY' ],
         sunday=row[ 'SUNDAY' ],
         message=row[ 'SCHEDULE_MESSAGE' ] )


   @classmethod
   def map_records(
         cls,
         rows: list[ Types.Row ] ) -> list[ WildEncounterScheduleConflictRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
