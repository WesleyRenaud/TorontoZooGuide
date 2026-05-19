from .defibrillator_mapper import map_defibrillator_records


def fetch_defibrillators( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  X_COORD,
                  Y_COORD
               FROM Defibrillator;
         """ )

      return map_defibrillator_records( data.fetchall() )

   finally:
      cur.close()
