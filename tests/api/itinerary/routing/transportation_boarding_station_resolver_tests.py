from __future__ import annotations

from api.itinerary.routing.transit_ride_endpoint import TransitRideEndpoint
from api.itinerary.routing.transportation_boarding_station_resolver import TransportationBoardingStationResolver
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg


ZOOMOBILE = 'Zoomobile'
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
      ZOOMOBILE,
      False ),
   ItineraryTransportationLeg(
      CANADA_STATION,
      AFRICA_STATION,
      '10:20 AM',
      '10:30 AM',
      ZOOMOBILE,
      False ),
   ItineraryTransportationLeg(
      'Tundra Zoomobile Station',
      EURASIA_STATION,
      '10:30 AM',
      '10:45 AM',
      ZOOMOBILE,
      False ),
]


def Test_BoardingStationForLegs_TestMultiLegRide_ExpectFirstFromStation() -> None:
   assert TransportationBoardingStationResolver.boarding_station_for_legs(
      TRANSPORTATION_LEGS ) == MAIN_STATION


def Test_StationForLegs_TestOnboardingEndpoint_ExpectFirstFromStation() -> None:
   assert TransportationBoardingStationResolver.station_for_legs(
      TRANSPORTATION_LEGS,
      TransitRideEndpoint.ONBOARDING ) == MAIN_STATION


def Test_StationForLegs_TestOffboardingEndpoint_ExpectLastToStation() -> None:
   assert TransportationBoardingStationResolver.station_for_legs(
      TRANSPORTATION_LEGS,
      TransitRideEndpoint.OFFBOARDING ) == EURASIA_STATION
