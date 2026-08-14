from __future__ import annotations

from .transportation_route_mapper import map_transportation_route_records
from .transportation_route_record import TransportationRouteRecord
from ...types import Connection


def fetch_transportation_routes_by_name(
      conn: Connection ) -> list[ TransportationRouteRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  t.NAME,
                  r.ROUTE
               FROM Transportation t
               INNER JOIN TransportationRoute r
                  ON r.TRANSPORTATION = t.NAME
               ORDER BY t.NAME ASC, r.ROUTE ASC;
         """ )

      return map_transportation_route_records( data.fetchall() )

   finally:
      cur.close()
