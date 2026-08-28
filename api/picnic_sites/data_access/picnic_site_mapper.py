from __future__ import annotations

from ...models import PicnicSite
from ...types import Types


class PicnicSiteMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> PicnicSite:
      return PicnicSite(
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ PicnicSite ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
