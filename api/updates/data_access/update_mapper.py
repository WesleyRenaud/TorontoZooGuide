from __future__ import annotations

from ...models import Update
from ...types import Row


def map_update_record( row: Row ) -> Update:
   return Update(
      title=row[ 'TITLE' ],
      description=row[ 'DESCRIPTION' ],
      update_type=row[ 'UPDATE_TYPE' ],
      start_date=row[ 'START_DATE' ],
      end_date=row[ 'END_DATE' ] )



def map_update_records( rows: list[ Row ] ) -> list[ Update ]:
   return [
      map_update_record( row )
      for row in rows
   ]
