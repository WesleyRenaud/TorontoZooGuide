from __future__ import annotations

from api.shared.enums.itinerary_transportation_station_role import ItineraryTransportationStationRole
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_ItineraryTransportationStationRole_TestSharedJson_ExpectSingleSourceOfTruth() -> None:
   members = SharedEnumValues.load_object_members( 'itineraryTransportationStationRole.json' )

   kinds = {
      name: member.value
      for name, member in ItineraryTransportationStationRole.__members__.items()
   }
   onboarding_flags = {
      name: member.onboarding
      for name, member in ItineraryTransportationStationRole.__members__.items()
   }
   offboarding_flags = {
      name: member.offboarding
      for name, member in ItineraryTransportationStationRole.__members__.items()
   }

   assert kinds == { name: definition[ 'kind' ] for name, definition in members.items() }
   assert onboarding_flags == {
      name: bool( definition.get( 'onboarding', False ) )
      for name, definition in members.items()
   }
   assert offboarding_flags == {
      name: bool( definition.get( 'offboarding', False ) )
      for name, definition in members.items()
   }


def Test_ItineraryTransportationStationRole_TestOnboarding_ExpectBoardingFlags() -> None:
   role = ItineraryTransportationStationRole.ONBOARDING

   assert role.onboarding is True
   assert role.offboarding is False


def Test_ItineraryTransportationStationRole_TestOffboarding_ExpectBoardingFlags() -> None:
   role = ItineraryTransportationStationRole.OFFBOARDING

   assert role.onboarding is False
   assert role.offboarding is True


def Test_ItineraryTransportationStationRole_TestRoundTrip_ExpectBothFlags() -> None:
   role = ItineraryTransportationStationRole.ROUND_TRIP

   assert role.onboarding is True
   assert role.offboarding is True


def Test_ItineraryTransportationStationRole_TestOnboardingRoleValues_ExpectSortedKinds() -> None:
   role_values = ItineraryTransportationStationRole.onboarding_role_values()

   assert role_values == sorted(
      member.value
      for member in ItineraryTransportationStationRole
      if member.onboarding )


def Test_ItineraryTransportationStationRole_TestOffboardingRoleValues_ExpectSortedKinds() -> None:
   role_values = ItineraryTransportationStationRole.offboarding_role_values()

   assert role_values == sorted(
      member.value
      for member in ItineraryTransportationStationRole
      if member.offboarding )
