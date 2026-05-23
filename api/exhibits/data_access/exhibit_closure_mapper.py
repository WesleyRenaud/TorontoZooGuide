from __future__ import annotations

from collections.abc import Iterable

from .exhibit_closure_record import ExhibitClosureRecord
from ...types import Row


def map_exhibit_closure_record( row: Row ) -> ExhibitClosureRecord:
   return ExhibitClosureRecord(
      exhibit=row[ 'EXHIBIT' ],
      closed_start=row[ 'CLOSED_START' ],
      closed_end=row[ 'CLOSED_END' ] )



def map_exhibit_closure_records( rows: Iterable[ Row ] ) -> list[ ExhibitClosureRecord ]:
   return [
      map_exhibit_closure_record( row )
      for row in rows
   ]
