from __future__ import annotations

from ...types import Cursor


def delete_itinerary_transportation_route_markers(
      cur: Cursor,
      transportation: str,
      added_as_attraction: bool ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryTransportationRouteMarker
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = ?;
      """,
      ( transportation, added_as_attraction ),
   )


def clear_itinerary_transportation_route_markers( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryTransportationRouteMarker;' )


def insert_itinerary_transportation_route_markers(
      cur: Cursor,
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
