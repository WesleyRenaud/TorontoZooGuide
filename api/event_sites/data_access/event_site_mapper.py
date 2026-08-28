from __future__ import annotations

from ...models import EventSite
from ...types import Types


class EventSiteMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> EventSite:
      return EventSite(
         name=row[ 'NAME' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ EventSite ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
