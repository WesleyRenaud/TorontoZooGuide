from __future__ import annotations

from collections import defaultdict

from .transportation_leg_stations import TransportationLegStations
from .transportation_route_leg_marker_mapper import TransportationRouteLegMarkerMapper
from .transportation_route_leg_marker_record import TransportationRouteLegMarkerRecord
from ...types import Connection


class TransportationRouteLegMarkerProvider():
   @classmethod
   def markers_by_leg_for_markers(
         cls,
         markers: list[ TransportationRouteLegMarkerRecord ],
   ) -> dict[ tuple[ str, str ], list[ str ] ]:
      markers_by_leg: dict[ tuple[ str, str ], list[ str ] ] = defaultdict( list )
      for marker in markers:
         markers_by_leg[ ( marker.from_station, marker.to_station ) ].append(
            marker.marker_id )
      return dict( markers_by_leg )


   @classmethod
   def fetch_transportation_route_leg_markers_by_leg(
         cls,
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

      return cls.markers_by_leg_for_markers(
         TransportationRouteLegMarkerMapper.map_records( rows ) )


   @classmethod
   def fetch_transportation_route_leg_marker_ids(
         cls,
         conn: Connection,
         *,
         transportation: str,
         route: str,
         legs: list[ TransportationLegStations ],
   ) -> list[ str ]:
      if not legs:
         return []

      markers_by_leg = cls.fetch_transportation_route_leg_markers_by_leg(
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
