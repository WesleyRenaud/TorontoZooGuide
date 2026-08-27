from __future__ import annotations

from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.enums.sequence_index import SequenceIndex
from .transit_ride_endpoint import TransitRideEndpoint


class TransportationBoardingStationResolver():
   @classmethod
   def station_for_legs(
         cls,
         legs: list[ ItineraryTransportationLeg ],
         endpoint: TransitRideEndpoint,
         ) -> str:
      if endpoint is TransitRideEndpoint.ONBOARDING:
         return legs[ SequenceIndex.FIRST ].from_station

      return legs[ SequenceIndex.LAST ].to_station


   @classmethod
   def boarding_station_for_legs(
         cls,
         legs: list[ ItineraryTransportationLeg ],
         ) -> str:
      return cls.station_for_legs(
         legs,
         TransitRideEndpoint.ONBOARDING )
