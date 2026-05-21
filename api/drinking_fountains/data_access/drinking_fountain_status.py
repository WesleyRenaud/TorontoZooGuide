from .drinking_fountain_status_mapper import map_drinking_fountain_status_record


def fetch_drinking_fountain_status_record( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  IS_CLOSED,
                  START_DATE,
                  END_DATE,
                  CLOSED_MESSAGE
               FROM DrinkingFountainStatus
               LIMIT 1;
         """ )

      row = data.fetchone()

      if row is None:
         return None

      return map_drinking_fountain_status_record( row )

   finally:
      cur.close()



def fetch_drinking_fountain_seasonal_likelihood( conn, target_date ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  LIKELIHOOD
               FROM DrinkingFountainDaySeasonalAvailabilityMultiplier
               WHERE MONTH = ?
                  AND DAY = ?;
         """,
         (
            target_date.month,
            target_date.day
         ) )

      row = data.fetchone()

      return row[ 'LIKELIHOOD' ] if row else 1.0

   finally:
      cur.close()



def save_drinking_fountain_closed_status( conn, status ):
   cur = conn.cursor()

   try:
      cur.execute( 'DELETE FROM DrinkingFountainStatus;' )

      cur.execute(
         """   INSERT INTO DrinkingFountainStatus (
                  IS_CLOSED,
                  START_DATE,
                  END_DATE,
                  CLOSED_MESSAGE
               )
               VALUES (1, ?, ?, ?);
         """,
         (
            status.start_date,
            status.end_date,
            status.message,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()



def save_drinking_fountain_open_status( conn, status ):
   cur = conn.cursor()

   try:
      cur.execute( 'DELETE FROM DrinkingFountainStatus;' )

      cur.execute(
         """   INSERT INTO DrinkingFountainStatus (
                  IS_CLOSED,
                  START_DATE,
                  END_DATE,
                  CLOSED_MESSAGE
               )
               VALUES (0, ?, ?, NULL);
         """,
         (
            status.start_date,
            status.end_date,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
