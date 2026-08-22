from __future__ import annotations

from ...types import Cursor


def delete_itinerary_transportation_route_markers(
      cur: Cursor,
      *,
      transportation: str ) -> None:
   cur.execute(
      """   DELETE FROM ItineraryTransportationRouteMarker
            WHERE TRANSPORTATION = ?;
      """,
      ( transportation, ),
   )


def clear_itinerary_transportation_route_markers( cur: Cursor ) -> None:
   cur.execute( 'DELETE FROM ItineraryTransportationRouteMarker;' )


def insert_itinerary_transportation_route_markers(
      cur: Cursor,
      *,
      transportation: str,
      route_marker_sequences: list[ list[ str ] ] ) -> None:
   for sequence, marker_ids in enumerate( route_marker_sequences ):
      for marker_order, marker_id in enumerate( marker_ids ):
         cur.execute(
            """   INSERT INTO ItineraryTransportationRouteMarker (
                     TRANSPORTATION,
                     SEQUENCE,
                     MARKER_ORDER,
                     MARKER_ID
                  )
                  VALUES ( ?, ?, ?, ? );
            """,
            ( transportation, sequence, marker_order, marker_id ),
         )
