from __future__ import annotations

from .drinking_fountain_record import DrinkingFountainRecord
from ...types import Row


class DrinkingFountainMapper():
   @classmethod
   def map_record( cls, row: Row ) -> DrinkingFountainRecord:
      return DrinkingFountainRecord(
         x_coord=row[ 'X_COORD' ],
         y_coord=row[ 'Y_COORD' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ DrinkingFountainRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
