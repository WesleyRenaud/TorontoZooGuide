from __future__ import annotations

from api.itinerary.routing.transit_ride_endpoint import TransitRideEndpoint
from api.itinerary.routing.transportation_boarding_station_resolver import TransportationBoardingStationResolver
from api.itinerary.routing.transportation_boarding_station_resolver import TransportationBoardingStationResolver
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg


def test_boarding_station_is_first_leg_from_station() -> None:
   legs = [
      ItineraryTransportationLeg(
         'Main Zoomobile Station',
         'Canadian Domain Zoomobile Station',
         '10:00 AM',
         '10:20 AM',
         'Zoomobile',
         False ),
      ItineraryTransportationLeg(
         'Canadian Domain Zoomobile Station',
         'Africa Zoomobile Station',
         '10:20 AM',
         '10:30 AM',
         'Zoomobile',
         False ),
      ItineraryTransportationLeg(
         'Tundra Zoomobile Station',
         'Eurasia Zoomobile Station',
         '10:30 AM',
         '10:45 AM',
         'Zoomobile',
         False ),
   ]

   assert TransportationBoardingStationResolver.boarding_station_for_legs( legs ) == (
      'Main Zoomobile Station' )
   assert TransportationBoardingStationResolver.station_for_legs(
      legs,
      TransitRideEndpoint.ONBOARDING ) == 'Main Zoomobile Station'
   assert TransportationBoardingStationResolver.station_for_legs(
      legs,
      TransitRideEndpoint.OFFBOARDING ) == 'Eurasia Zoomobile Station'
