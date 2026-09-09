from __future__ import annotations

from api.shared.enums.itinerary_transportation_station_role import ItineraryTransportationStationRole


def Test_ItineraryTransportationStationRole_TestWireValues_ExpectKinds() -> None:
   assert ItineraryTransportationStationRole.ONBOARDING.value == 'onboarding_station'
   assert ItineraryTransportationStationRole.OFFBOARDING.value == 'offboarding_station'
   assert ItineraryTransportationStationRole.ROUND_TRIP.value == 'round_trip'


def Test_ItineraryTransportationStationRole_TestFlags_ExpectBoardingMembership() -> None:
   assert ItineraryTransportationStationRole.ONBOARDING.onboarding is True
   assert ItineraryTransportationStationRole.ONBOARDING.offboarding is False
   assert ItineraryTransportationStationRole.OFFBOARDING.onboarding is False
   assert ItineraryTransportationStationRole.OFFBOARDING.offboarding is True
   assert ItineraryTransportationStationRole.ROUND_TRIP.onboarding is True
   assert ItineraryTransportationStationRole.ROUND_TRIP.offboarding is True


def Test_ItineraryTransportationStationRole_TestRoleValueHelpers_ExpectSortedKinds() -> None:
   assert ItineraryTransportationStationRole.onboarding_role_values() == [
      'onboarding_station',
      'round_trip',
   ]
   assert ItineraryTransportationStationRole.offboarding_role_values() == [
      'offboarding_station',
      'round_trip',
   ]
