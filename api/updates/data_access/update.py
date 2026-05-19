from .update_mapper import map_update_records


def fetch_updates( conn, as_of_date ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  TITLE,
                  DESCRIPTION,
                  UPDATE_TYPE,
                  START_DATE,
                  END_DATE
               FROM ZooUpdate
               WHERE END_DATE IS NULL
                  OR END_DATE >= ?
               ORDER BY START_DATE DESC, TITLE ASC;
         """,
         ( as_of_date, ) )

      return map_update_records( data.fetchall() )

   finally:
      cur.close()
