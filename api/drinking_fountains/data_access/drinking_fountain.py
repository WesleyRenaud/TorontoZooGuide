from .drinking_fountain_mapper import map_drinking_fountain_records


def fetch_drinking_fountain_records( conn ):
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
