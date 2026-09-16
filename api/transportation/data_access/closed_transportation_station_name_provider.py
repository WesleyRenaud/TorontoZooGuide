from __future__ import annotations

from ...shared.enums.position import Position
from ...types import Types


class ClosedTransportationStationNameProvider():
   @classmethod
   def fetch_closed_transportation_station_names(
         cls,
         conn: Types.Connection,
         transportation: str,
         today: Types.DateKey ) -> list[ str ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT DISTINCT
                     STATION
                  FROM TransportationStationStatus
                  WHERE TRANSPORTATION = ?
                     AND IS_CLOSED = 1
                     AND (
                        CLOSED_END IS NULL
                        OR CLOSED_END >= ?
                     )
                  ORDER BY STATION;
            """,
            ( transportation, today ) )

         return [ row[ Position.FIRST ] for row in data.fetchall() ]

      finally:
         cur.close()
