from __future__ import annotations

from .event_site_mapper import map_event_site_records
from ...models import EventSite
from ...types import Connection


def fetch_event_sites( conn: Connection ) -> list[ EventSite ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  NAME,
                  X_COORD,
                  Y_COORD
               FROM EventSite;
         """ )

      return map_event_site_records( data.fetchall() )

   finally:
      cur.close()
