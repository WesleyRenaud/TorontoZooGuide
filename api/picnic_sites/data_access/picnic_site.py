from __future__ import annotations

from ...models import PicnicSite
from .picnic_site_mapper import map_picnic_site_records
from ...types import Connection


def fetch_picnic_sites( conn: Connection ) -> list[ PicnicSite ]:
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
