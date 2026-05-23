from __future__ import annotations

from ... import zoo
from ...types import Connection
from .guest_service_mapper import map_guest_service_records


def fetch_guest_services( conn: Connection ) -> list[ zoo.GuestService ]:
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
