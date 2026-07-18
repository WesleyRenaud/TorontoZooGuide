from __future__ import annotations

from ...models import EventSite
from ...types import Row


def map_event_site_record( row: Row ) -> EventSite:
   return EventSite(
      name=row[ 'NAME' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_event_site_records( rows: list[ Row ] ) -> list[ EventSite ]:
   return [
      map_event_site_record( row )
      for row in rows
   ]
