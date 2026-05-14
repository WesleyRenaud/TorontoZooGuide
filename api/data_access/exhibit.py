from .exhibit_mapper import map_region_exhibit_rows


def fetch_exhibit_names_in_region( conn, region ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """  SELECT
                 e.NAME
              FROM Exhibit e
              WHERE e.REGION = ?;
         """, ( region, ) )

      return [ row[ 0 ] for row in data.fetchall() ]

   finally:
      cur.close()


def fetch_region_exhibit_rows( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  r.NAME AS REGION_NAME,
                  e.NAME AS EXHIBIT_NAME
               FROM Region r
               LEFT JOIN Exhibit e
                  ON e.REGION = r.NAME
               ORDER BY r.NAME, e.NAME;
         """ )

      return map_region_exhibit_rows( data.fetchall() )

   finally:
      cur.close()
