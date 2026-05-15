from .restroom_mapper import map_restroom_records


def fetch_restroom_records( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  r.TITLE,
                  r.X_COORD,
                  r.Y_COORD,
                  s.IS_CLOSED,
                  s.CLOSED_MESSAGE,
                  s.CLOSED_START,
                  s.CLOSED_END,
                  a.ALERT_MESSAGE,
                  a.ALERT_START_DATE,
                  a.ALERT_END_DATE
               FROM Restroom r
               LEFT JOIN RestroomStatus s
                  ON s.RESTROOM = r.TITLE
               LEFT JOIN RestroomAlert a
                  ON a.RESTROOM = r.TITLE;
         """ )

      return map_restroom_records( data.fetchall() )

   finally:
      cur.close()
