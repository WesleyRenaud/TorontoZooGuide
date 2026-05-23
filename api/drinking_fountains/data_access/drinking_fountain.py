from __future__ import annotations

from .drinking_fountain_mapper import map_drinking_fountain_records
from .drinking_fountain_record import DrinkingFountainRecord
from ...types import Connection


def fetch_drinking_fountain_records( conn: Connection ) -> list[ DrinkingFountainRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  X_COORD,
                  Y_COORD
               FROM DrinkingFountain;
         """ )

      return map_drinking_fountain_records( data.fetchall() )

   finally:
      cur.close()
