from __future__ import annotations

from api.itinerary.routing.transit_ride_endpoint import TransitRideEndpoint
from api.itinerary.routing.transportation_boarding_station_resolver import TransportationBoardingStationResolver
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


MAIN_STATION = 'Main Zoomobile Station'
CANADA_STATION = 'Canadian Domain Zoomobile Station'
AFRICA_STATION = 'Africa Zoomobile Station'
EURASIA_STATION = 'Eurasia Zoomobile Station'
TRANSPORTATION_LEGS = [
   ItineraryTransportationLeg(
      MAIN_STATION,
      CANADA_STATION,
      '10:00 AM',
      '10:20 AM',
      TransportationName.ZOOMOBILE,
      False ),
   ItineraryTransportationLeg(
      CANADA_STATION,
      AFRICA_STATION,
      '10:20 AM',
      '10:30 AM',
      TransportationName.ZOOMOBILE,
      False ),
   ItineraryTransportationLeg(
      'Tundra Zoomobile Station',
      EURASIA_STATION,
      '10:30 AM',
      '10:45 AM',
      TransportationName.ZOOMOBILE,
      False ),
]


def Test_BoardingStationForLegs_TestMultiLegRide_ExpectFirstFromStation() -> None:
   station = TransportationBoardingStationResolver.boarding_station_for_legs(
      TRANSPORTATION_LEGS )

   assert station == TRANSPORTATION_LEGS[ Position.FIRST ].from_station


def Test_StationForLegs_TestOnboardingEndpoint_ExpectFirstFromStation() -> None:
   station = TransportationBoardingStationResolver.station_for_legs(
      TRANSPORTATION_LEGS,
      TransitRideEndpoint.ONBOARDING )

   assert station == TRANSPORTATION_LEGS[ Position.FIRST ].from_station


def Test_StationForLegs_TestOffboardingEndpoint_ExpectLastToStation() -> None:
   station = TransportationBoardingStationResolver.station_for_legs(
      TRANSPORTATION_LEGS,
      TransitRideEndpoint.OFFBOARDING )

   assert station == TRANSPORTATION_LEGS[ Position.LAST ].to_station
