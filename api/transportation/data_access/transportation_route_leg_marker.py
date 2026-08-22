from __future__ import annotations

from typing import Protocol

from .transportation_route_leg_marker_mapper import map_transportation_route_leg_markers
from .transportation_route_leg_marker_mapper import markers_by_leg_for_markers
from ...types import Connection


class TransportationLegStations( Protocol ):
   from_station: str
   to_station: str


def fetch_transportation_route_leg_markers_by_leg(
      conn: Connection,
      *,
      transportation: str,
      route: str,
) -> dict[ tuple[ str, str ], list[ str ] ]:
   cur = conn.cursor()

   try:
      # Seed inserts markers in travel order; rowid preserves that order
      # (including wraparound legs where MARKER_ID is not monotonic).
      rows = cur.execute(
         """   SELECT
                  FROM_STATION,
                  TO_STATION,
                  MARKER_ID
               FROM TransportationRouteLegMarker
               WHERE TRANSPORTATION = ?
                 AND ROUTE = ?
               ORDER BY rowid;
         """,
         ( transportation, route ),
      ).fetchall()
   finally:
      cur.close()

   return markers_by_leg_for_markers(
      map_transportation_route_leg_markers( rows ) )


def fetch_transportation_route_leg_marker_ids(
      conn: Connection,
      *,
      transportation: str,
      route: str,
      legs: list[ TransportationLegStations ],
) -> list[ str ]:
   if not legs:
      return []

   markers_by_leg = fetch_transportation_route_leg_markers_by_leg(
      conn,
      transportation=transportation,
      route=route,
   )

   return [
      marker_id
      for leg in legs
      for marker_id in markers_by_leg.get(
         ( leg.from_station, leg.to_station ),
         [],
      )
   ]
