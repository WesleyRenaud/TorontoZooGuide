from __future__ import annotations

from ...models import Defibrillator
from ...types import Row


def map_defibrillator_record( row: Row ) -> Defibrillator:
   return Defibrillator(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_defibrillator_records( rows: list[ Row ] ) -> list[ Defibrillator ]:
   return [
      map_defibrillator_record( row )
      for row in rows
   ]
