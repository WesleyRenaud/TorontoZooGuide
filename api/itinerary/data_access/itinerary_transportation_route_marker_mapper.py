from __future__ import annotations

from .itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord
from ...shared.value_conversion import ValueConversion
from ...types import Types


class ItineraryTransportationRouteMarkerMapper():
   @classmethod
   def map_record(
         cls,
         row: Types.Row,
   ) -> ItineraryTransportationRouteMarkerRecord:
      return ItineraryTransportationRouteMarkerRecord(
         transportation=row[ 'TRANSPORTATION' ],
         added_as_attraction=ValueConversion.as_boolean(
            row[ 'ADDED_AS_ATTRACTION' ] ),
         sequence=row[ 'SEQUENCE' ],
         marker_order=row[ 'MARKER_ORDER' ],
         marker_id=row[ 'MARKER_ID' ],
      )


   @classmethod
   def map_records(
         cls,
         rows: list[ Types.Row ],
   ) -> list[ ItineraryTransportationRouteMarkerRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]


   @classmethod
   def route_marker_sequences_for_markers(
         cls,
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
