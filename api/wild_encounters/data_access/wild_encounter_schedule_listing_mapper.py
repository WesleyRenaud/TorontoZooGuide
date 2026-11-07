from __future__ import annotations

from ...types import Types
from .wild_encounter_schedule_listing_record import WildEncounterScheduleListingRecord


class WildEncounterScheduleListingMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> WildEncounterScheduleListingRecord:
      return WildEncounterScheduleListingRecord(
         wild_encounter=row[ 'WILD_ENCOUNTER' ],
         schedule_start_date=row[ 'SCHEDULE_START_DATE' ],
         schedule_end_date=row[ 'SCHEDULE_END_DATE' ],
         encounter_time=row[ 'ENCOUNTER_TIME' ],
         monday=bool( row[ 'MONDAY' ] ),
         tuesday=bool( row[ 'TUESDAY' ] ),
         wednesday=bool( row[ 'WEDNESDAY' ] ),
         thursday=bool( row[ 'THURSDAY' ] ),
         friday=bool( row[ 'FRIDAY' ] ),
         saturday=bool( row[ 'SATURDAY' ] ),
         sunday=bool( row[ 'SUNDAY' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ WildEncounterScheduleListingRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
