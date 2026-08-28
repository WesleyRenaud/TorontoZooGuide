from __future__ import annotations

from ...models import Defibrillator
from ...types import Types


class DefibrillatorMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> Defibrillator:
      return Defibrillator(
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ Defibrillator ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
