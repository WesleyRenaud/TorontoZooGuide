from __future__ import annotations

from .guest_service_mapper import map_guest_service_records
from ...models import GuestService
from ...types import Connection


def fetch_guest_services( conn: Connection ) -> list[ GuestService ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  SERVICE_TYPE,
                  X_COORD,
                  Y_COORD
               FROM GuestService;
         """ )

      return map_guest_service_records( data.fetchall() )

   finally:
      cur.close()
