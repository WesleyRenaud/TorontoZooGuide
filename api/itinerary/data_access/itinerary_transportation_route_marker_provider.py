from __future__ import annotations

from .itinerary_transportation_route_marker_mapper import ItineraryTransportationRouteMarkerMapper
from .itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord
from ...types import Types


class ItineraryTransportationRouteMarkerProvider():
   @classmethod
   def fetch_itinerary_transportation_route_markers(
         cls,
         conn: Types.Connection,
   ) -> list[ ItineraryTransportationRouteMarkerRecord ]:
      cur = conn.cursor()

      try:
         rows = cur.execute(
            """   SELECT
                     TRANSPORTATION,
                     ADDED_AS_ATTRACTION,
                     SEQUENCE,
                     MARKER_ORDER,
                     MARKER_ID
                  FROM ItineraryTransportationRouteMarker
                  ORDER BY TRANSPORTATION, ADDED_AS_ATTRACTION, SEQUENCE, MARKER_ORDER;
            """
         ).fetchall()
      finally:
         cur.close()

      return ItineraryTransportationRouteMarkerMapper.map_records( rows )


   @classmethod
   def delete_itinerary_transportation_route_markers(
         cls,
         cur: Types.Cursor,
         transportation: str,
         added_as_attraction: bool ) -> None:
      cur.execute(
         """   DELETE FROM ItineraryTransportationRouteMarker
               WHERE TRANSPORTATION = ?
                 AND ADDED_AS_ATTRACTION = ?;
         """,
         ( transportation, added_as_attraction ),
      )


   @classmethod
   def clear_itinerary_transportation_route_markers( cls, cur: Types.Cursor ) -> None:
      cur.execute( 'DELETE FROM ItineraryTransportationRouteMarker;' )


   @classmethod
   def insert_itinerary_transportation_route_markers(
         cls,
         cur: Types.Cursor,
         transportation: str,
         added_as_attraction: bool,
         route_marker_sequences: list[ list[ str ] ] ) -> None:
      for sequence, marker_ids in enumerate( route_marker_sequences ):
         for marker_order, marker_id in enumerate( marker_ids ):
            cur.execute(
               """   INSERT INTO ItineraryTransportationRouteMarker (
                        TRANSPORTATION,
                        ADDED_AS_ATTRACTION,
                        SEQUENCE,
                        MARKER_ORDER,
                        MARKER_ID
                     )
                     VALUES ( ?, ?, ?, ?, ? );
               """,
               (
                  transportation,
                  added_as_attraction,
                  sequence,
                  marker_order,
                  marker_id,
               ),
            )
