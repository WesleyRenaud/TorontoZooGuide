from __future__ import annotations

from ..domain.animal_visibility_schedule import AnimalVisibilitySchedule
from ...types import Types


class AnimalVisibilityScheduleMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AnimalVisibilitySchedule:
      return AnimalVisibilitySchedule(
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         start_date=row[ 'SCHEDULE_START_DATE' ],
         end_date=row[ 'SCHEDULE_END_DATE' ],
         daily_start_time=row[ 'DAILY_START_TIME' ] or '',
         daily_end_time=row[ 'DAILY_END_TIME' ] or '',
         message=row[ 'VIEWING_MESSAGE' ] or '',
      )


   @classmethod
   def map_records(
         cls,
         rows: list[ Types.Row ] ) -> list[ AnimalVisibilitySchedule ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
