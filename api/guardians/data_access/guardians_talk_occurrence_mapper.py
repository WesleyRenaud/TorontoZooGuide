from __future__ import annotations

from .guardians_talk_occurrence_record import GuardiansTalkOccurrenceRecord
from ...types import Row


class GuardiansTalkOccurrenceMapper():
   @classmethod
   def map_record( cls, row: Row ) -> GuardiansTalkOccurrenceRecord:
      return GuardiansTalkOccurrenceRecord(
         occurrence_date=row[ 'OCCURRENCE_DATE' ],
         talk_time=row[ 'TALK_TIME' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ GuardiansTalkOccurrenceRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
