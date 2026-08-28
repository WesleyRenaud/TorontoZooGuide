from __future__ import annotations

from ...models import Update
from ...types import Types


class UpdateMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> Update:
      return Update(
         title=row[ 'TITLE' ],
         description=row[ 'DESCRIPTION' ],
         update_type=row[ 'UPDATE_TYPE' ],
         start_date=row[ 'START_DATE' ],
         end_date=row[ 'END_DATE' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ Update ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
