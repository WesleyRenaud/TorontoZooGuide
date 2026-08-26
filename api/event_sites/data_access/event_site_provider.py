from __future__ import annotations

from .event_site_mapper import EventSiteMapper
from ...models import EventSite
from ...types import Connection


class EventSiteProvider():
   @classmethod
   def fetch_event_sites( cls, conn: Connection ) -> list[ EventSite ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     NAME,
                     X_COORD,
                     Y_COORD
                  FROM EventSite;
            """ )

         return EventSiteMapper.map_records( data.fetchall() )

      finally:
         cur.close()
