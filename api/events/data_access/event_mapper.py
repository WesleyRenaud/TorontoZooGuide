from __future__ import annotations

from ...models import Event
from ...types import Types


class EventMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> Event:
      return Event(
         name=row[ 'NAME' ],
         location=row[ 'LOCATION' ],
         description=row[ 'DESCRIPTION' ],
         link=row[ 'LINK' ],
         start_date=row[ 'START_DATE' ],
         end_date=row[ 'END_DATE' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ Event ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
