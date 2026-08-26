from __future__ import annotations

from ...models import EventSite
from ...types import Row


class EventSiteMapper():
   @classmethod
   def map_record( cls, row: Row ) -> EventSite:
      return EventSite(
         name=row[ 'NAME' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ EventSite ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
