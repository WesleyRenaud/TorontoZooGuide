from __future__ import annotations

from ...models import Pavilion
from ...types import Row


class PavilionMapper():
   @classmethod
   def map_record( cls, row: Row ) -> Pavilion:
      return Pavilion(
         name=row[ 'NAME' ],
         region=row[ 'REGION' ],
         description=row[ 'DESCRIPTION' ],
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ Pavilion ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
