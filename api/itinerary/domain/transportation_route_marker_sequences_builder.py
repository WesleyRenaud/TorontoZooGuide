from __future__ import annotations

from .itinerary_transportation_stations_builder import ItineraryTransportationStationsBuilder
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...transportation.data_access.transportation_route_leg_marker_provider import TransportationRouteLegMarkerProvider
from ...types import Types


class TransportationRouteMarkerSequencesBuilder():
   @classmethod
   def build(
         cls,
         conn: Types.Connection,
         *,
         transportation: str,
         route: str,
         legs: list[ ItineraryTransportationLeg ],
   ) -> list[ list[ str ] ]:
      if not legs:
         return []

      markers_by_leg = TransportationRouteLegMarkerProvider.fetch_transportation_route_leg_markers_by_leg(
         conn,
         transportation=transportation,
         route=route,
      )
      sequences: list[ list[ str ] ] = []

      for leg_sequence in ItineraryTransportationStationsBuilder.group_consecutive_leg_sequences(
            legs ):
         marker_ids = [
            marker_id
            for leg in leg_sequence
            for marker_id in markers_by_leg.get(
               ( leg.from_station, leg.to_station ),
               [],
            )
         ]

         if marker_ids:
            sequences.append( marker_ids )

      return sequences
