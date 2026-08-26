from __future__ import annotations

from ...models import Update
from ...types import Row


class UpdateMapper():
   @classmethod
   def map_record( cls, row: Row ) -> Update:
      return Update(
         title=row[ 'TITLE' ],
         description=row[ 'DESCRIPTION' ],
         update_type=row[ 'UPDATE_TYPE' ],
         start_date=row[ 'START_DATE' ],
         end_date=row[ 'END_DATE' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ Update ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
