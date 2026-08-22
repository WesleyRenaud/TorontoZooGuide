from __future__ import annotations

from .itinerary_transportation_route_marker_mapper import map_itinerary_transportation_route_markers
from .itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord
from ...types import Connection


def fetch_itinerary_transportation_route_markers(
      conn: Connection,
) -> list[ ItineraryTransportationRouteMarkerRecord ]:
   cur = conn.cursor()

   try:
      rows = cur.execute(
         """   SELECT
                  TRANSPORTATION,
                  SEQUENCE,
                  MARKER_ORDER,
                  MARKER_ID
               FROM ItineraryTransportationRouteMarker
               ORDER BY TRANSPORTATION, SEQUENCE, MARKER_ORDER;
         """
      ).fetchall()
   finally:
      cur.close()

   return map_itinerary_transportation_route_markers( rows )
