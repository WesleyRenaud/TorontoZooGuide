from __future__ import annotations

from ...models import PicnicSite
from .picnic_site_mapper import PicnicSiteMapper
from ...types import Connection


class PicnicSiteProvider():
   @classmethod
   def fetch_picnic_sites( cls, conn: Connection ) -> list[ PicnicSite ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     X_COORD,
                     Y_COORD
                  FROM PicnicSite;
            """ )

         return PicnicSiteMapper.map_records( data.fetchall() )

      finally:
         cur.close()
