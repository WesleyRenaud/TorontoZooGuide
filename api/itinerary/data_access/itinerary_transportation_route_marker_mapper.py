from __future__ import annotations

from .itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord
from ...types import Row


def map_itinerary_transportation_route_marker(
      row: Row,
) -> ItineraryTransportationRouteMarkerRecord:
   return ItineraryTransportationRouteMarkerRecord(
      transportation=row[ 'TRANSPORTATION' ],
      sequence=row[ 'SEQUENCE' ],
      marker_order=row[ 'MARKER_ORDER' ],
      marker_id=row[ 'MARKER_ID' ],
   )


def map_itinerary_transportation_route_markers(
      rows: list[ Row ],
) -> list[ ItineraryTransportationRouteMarkerRecord ]:
   return [
      map_itinerary_transportation_route_marker( row )
      for row in rows
   ]


def route_marker_sequences_for_markers(
      markers: list[ ItineraryTransportationRouteMarkerRecord ],
) -> list[ list[ str ] ]:
   sequences: list[ list[ str ] ] = []
   current_sequence: int | None = None
   current_marker_ids: list[ str ] = []

   for marker in markers:
      if (
            current_sequence is not None
            and marker.sequence != current_sequence
      ):
         sequences.append( current_marker_ids )
         current_marker_ids = []

      current_sequence = marker.sequence
      current_marker_ids.append( marker.marker_id )

   if current_marker_ids:
      sequences.append( current_marker_ids )

   return sequences
