from __future__ import annotations

from collections.abc import Iterable

from ...types import Row
from .drinking_fountain_record import DrinkingFountainRecord


def map_drinking_fountain_record( row: Row ) -> DrinkingFountainRecord:
   return DrinkingFountainRecord(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_drinking_fountain_records( rows: Iterable[ Row ] ) -> list[ DrinkingFountainRecord ]:
   return [
      map_drinking_fountain_record( row )
      for row in rows
   ]
