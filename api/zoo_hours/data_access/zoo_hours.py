from .zoo_hours_mapper import map_zoo_hours_record


def fetch_zoo_hours_record( conn, operating_date ):
   cur = conn.cursor()

   try:
      row = cur.execute(
         """   SELECT
                  OPERATING_DATE,
                  EARLY_ADMISSION_TIME,
                  OPEN_TIME,
                  LAST_ADMISSION_TIME,
                  CLOSE_TIME
               FROM ZooHours
               WHERE OPERATING_DATE = ?;
         """,
         ( operating_date, ) ).fetchone()

      if row == None:
         return None

      return map_zoo_hours_record( row )

   finally:
      cur.close()
