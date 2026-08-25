from __future__ import annotations

from .drinking_fountain_status_record import DrinkingFountainStatusRecord
from ...types import Row


class DrinkingFountainStatusMapper():
   @classmethod
   def map_record( cls, row: Row ) -> DrinkingFountainStatusRecord:
      return DrinkingFountainStatusRecord(
         is_closed=row[ 'IS_CLOSED' ],
         start_date=row[ 'START_DATE' ],
         end_date=row[ 'END_DATE' ],
         closed_message=row[ 'CLOSED_MESSAGE' ] )
