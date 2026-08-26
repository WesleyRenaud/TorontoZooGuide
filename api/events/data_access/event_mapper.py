from __future__ import annotations

from ...models import Event
from ...types import Row


class EventMapper():
   @classmethod
   def map_record( cls, row: Row ) -> Event:
      return Event(
         name=row[ 'NAME' ],
         location=row[ 'LOCATION' ],
         description=row[ 'DESCRIPTION' ],
         link=row[ 'LINK' ],
         start_date=row[ 'START_DATE' ],
         end_date=row[ 'END_DATE' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ Event ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
