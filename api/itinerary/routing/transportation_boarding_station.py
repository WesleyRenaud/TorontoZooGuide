from __future__ import annotations

from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.enums.sequence_index import SequenceIndex
from .transit_ride_endpoint import TransitRideEndpoint


def station_for_transportation_legs(
      legs: list[ ItineraryTransportationLeg ],
      endpoint: TransitRideEndpoint,
   ) -> str:
   if endpoint is TransitRideEndpoint.ONBOARDING:
      return legs[ SequenceIndex.FIRST ].from_station

   return legs[ SequenceIndex.LAST ].to_station


def boarding_station_for_transportation_legs(
      legs: list[ ItineraryTransportationLeg ],
   ) -> str:
   return station_for_transportation_legs(
      legs,
      TransitRideEndpoint.ONBOARDING )
