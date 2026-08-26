from __future__ import annotations

from .transportation_route_mapper import TransportationRouteMapper
from .transportation_route_record import TransportationRouteRecord
from ...types import Connection


class TransportationRouteProvider():
   @classmethod
   def fetch_transportation_routes_by_name(
         cls,
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

         return TransportationRouteMapper.map_records( data.fetchall() )

      finally:
         cur.close()
