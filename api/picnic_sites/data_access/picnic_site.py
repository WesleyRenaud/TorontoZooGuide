from .picnic_site_mapper import map_picnic_site_records


def fetch_picnic_sites( conn ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  X_COORD,
                  Y_COORD
               FROM PicnicSite;
         """ )

      return map_picnic_site_records( data.fetchall() )

   finally:
      cur.close()
