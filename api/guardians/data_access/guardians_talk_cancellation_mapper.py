from __future__ import annotations

from .guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from ...types import Row


class GuardiansTalkCancellationMapper():
   @classmethod
   def map_record( cls, row: Row ) -> GuardiansTalkCancellationRecord:
      return GuardiansTalkCancellationRecord(
         cancellation_date=row[ 'CANCELLATION_DATE' ],
         talk_time=row[ 'TALK_TIME' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ GuardiansTalkCancellationRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
