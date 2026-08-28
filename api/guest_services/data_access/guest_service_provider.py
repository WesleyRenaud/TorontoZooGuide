from __future__ import annotations

from .guest_service_mapper import GuestServiceMapper
from ...models import GuestService
from ...types import Types


class GuestServiceProvider():
   @classmethod
   def fetch_guest_services( cls, conn: Types.Connection ) -> list[ GuestService ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     SERVICE_TYPE,
                     X_COORD,
                     Y_COORD
                  FROM GuestService;
            """ )

         return GuestServiceMapper.map_records( data.fetchall() )

      finally:
         cur.close()
