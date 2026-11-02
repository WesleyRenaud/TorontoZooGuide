from __future__ import annotations

from .attraction_closure_record import AttractionClosureRecord
from ...types import Types


class AttractionClosureMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AttractionClosureRecord:
      return AttractionClosureRecord(
         attraction=row[ 'ATTRACTION' ],
         closed_start=row[ 'CLOSED_START' ],
         closed_end=row[ 'CLOSED_END' ],
         closed_message=row[ 'CLOSED_MESSAGE' ],
         is_closed_for_season=bool( row[ 'CLOSED_FOR_SEASON' ] ) )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ AttractionClosureRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
