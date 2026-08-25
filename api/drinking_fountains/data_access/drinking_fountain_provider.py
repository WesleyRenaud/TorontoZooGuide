from __future__ import annotations

from .drinking_fountain_mapper import DrinkingFountainMapper
from .drinking_fountain_record import DrinkingFountainRecord
from ...types import Connection


class DrinkingFountainProvider():
   @classmethod
   def fetch_drinking_fountain_records(
         cls,
         conn: Connection ) -> list[ DrinkingFountainRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     X_COORD,
                     Y_COORD
                  FROM DrinkingFountain;
            """ )

         return DrinkingFountainMapper.map_records( data.fetchall() )

      finally:
         cur.close()
