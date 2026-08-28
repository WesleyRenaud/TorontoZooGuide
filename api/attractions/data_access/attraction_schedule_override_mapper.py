from __future__ import annotations

from .attraction_schedule_override_record import AttractionScheduleOverrideRecord
from ...types import Types


class AttractionScheduleOverrideMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AttractionScheduleOverrideRecord:
      return AttractionScheduleOverrideRecord(
         attraction=row[ 'ATTRACTION' ],
         override_start_date=row[ 'OVERRIDE_START_DATE' ],
         override_end_date=row[ 'OVERRIDE_END_DATE' ],
         is_closed=row[ 'IS_CLOSED' ],
         override_message=row[ 'OVERRIDE_MESSAGE' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ AttractionScheduleOverrideRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
