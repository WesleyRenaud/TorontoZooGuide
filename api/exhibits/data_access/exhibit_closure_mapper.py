from __future__ import annotations

from .exhibit_closure_record import ExhibitClosureRecord
from ...types import Types


class ExhibitClosureMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ExhibitClosureRecord:
      return ExhibitClosureRecord(
         exhibit=row[ 'EXHIBIT' ],
         closed_start=row[ 'CLOSED_START' ],
         closed_end=row[ 'CLOSED_END' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ ExhibitClosureRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
