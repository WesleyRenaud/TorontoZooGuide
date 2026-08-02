from __future__ import annotations

from ...models import Event
from ...types import Row


def map_event_record( row: Row ) -> Event:
   return Event(
      name=row[ 'NAME' ],
      location=row[ 'LOCATION' ],
      description=row[ 'DESCRIPTION' ],
      link=row[ 'LINK' ],
      start_date=row[ 'START_DATE' ],
      end_date=row[ 'END_DATE' ] )


def map_event_records( rows: list[ Row ] ) -> list[ Event ]:
   return [
      map_event_record( row )
      for row in rows
   ]
