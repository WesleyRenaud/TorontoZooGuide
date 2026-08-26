from __future__ import annotations

from .attraction_schedule_record import AttractionScheduleRecord
from ...types import Row


class AttractionScheduleMapper():
   @classmethod
   def map_record( cls, row: Row ) -> AttractionScheduleRecord:
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


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ AttractionScheduleRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
