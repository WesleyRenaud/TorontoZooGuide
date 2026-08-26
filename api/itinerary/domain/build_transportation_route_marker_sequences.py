from __future__ import annotations

from .itinerary_transportation_stations import group_consecutive_transportation_leg_sequences
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...transportation.data_access.transportation_route_leg_marker_provider import TransportationRouteLegMarkerProvider
from ...types import Connection


def build_transportation_route_marker_sequences(
      conn: Connection,
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

   for leg_sequence in group_consecutive_transportation_leg_sequences( legs ):
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
