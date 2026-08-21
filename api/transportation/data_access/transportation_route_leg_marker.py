from __future__ import annotations

from typing import Protocol

from ...types import Connection


class TransportationLegStations( Protocol ):
   from_station: str
   to_station: str


def fetch_transportation_route_leg_marker_ids(
      conn: Connection,
      *,
      transportation: str,
      route: str,
      legs: list[ TransportationLegStations ],
) -> list[ str ]:
   if not legs:
      return []

   leg_keys = {
      ( leg.from_station, leg.to_station )
      for leg in legs
   }
   cur = conn.cursor()

   try:
      rows = cur.execute(
         """   SELECT
                  FROM_STATION,
                  TO_STATION,
                  MARKER_ID
               FROM TransportationRouteLegMarker
               WHERE TRANSPORTATION = ?
                 AND ROUTE = ?
               ORDER BY MARKER_ID;
         """,
         ( transportation, route ),
      ).fetchall()

      return [
         row[ 'MARKER_ID' ]
         for row in rows
         if ( row[ 'FROM_STATION' ], row[ 'TO_STATION' ] ) in leg_keys
      ]

   finally:
      cur.close()
