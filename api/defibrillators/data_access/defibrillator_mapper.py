from __future__ import annotations

from collections.abc import Iterable

from ... import zoo
from ...types import Row


def map_defibrillator_record( row: Row ) -> zoo.Defibrillator:
   return zoo.Defibrillator(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_defibrillator_records( rows: Iterable[ Row ] ) -> list[ zoo.Defibrillator ]:
   return [
      map_defibrillator_record( row )
      for row in rows
   ]
