from .exhibit_closure_mapper import map_exhibit_closure_records


def fetch_exhibit_closure_records( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  EXHIBIT,
                  CLOSED_START,
                  CLOSED_END
               FROM ExhibitStatus
               WHERE IS_CLOSED = 1;
         """ )

      return map_exhibit_closure_records( data.fetchall() )

   finally:
      cur.close()
