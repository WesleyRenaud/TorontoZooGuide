from __future__ import annotations

from api.shared.enums.itinerary_transportation_station_role import ItineraryTransportationStationRole
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_ItineraryTransportationStationRole_TestSharedJson_ExpectSingleSourceOfTruth() -> None:
   members = SharedEnumValues.load_object_members( 'itineraryTransportationStationRole.json' )

   assert {
      name: member.value
      for name, member in ItineraryTransportationStationRole.__members__.items()
   } == { name: definition[ 'kind' ] for name, definition in members.items() }
   assert {
      name: member.onboarding
      for name, member in ItineraryTransportationStationRole.__members__.items()
   } == {
      name: bool( definition.get( 'onboarding', False ) )
      for name, definition in members.items()
   }
   assert {
      name: member.offboarding
      for name, member in ItineraryTransportationStationRole.__members__.items()
   } == {
      name: bool( definition.get( 'offboarding', False ) )
      for name, definition in members.items()
   }


def Test_ItineraryTransportationStationRole_TestFlags_ExpectBoardingMembership() -> None:
   assert ItineraryTransportationStationRole.ONBOARDING.onboarding is True
   assert ItineraryTransportationStationRole.ONBOARDING.offboarding is False
   assert ItineraryTransportationStationRole.OFFBOARDING.onboarding is False
   assert ItineraryTransportationStationRole.OFFBOARDING.offboarding is True
   assert ItineraryTransportationStationRole.ROUND_TRIP.onboarding is True
   assert ItineraryTransportationStationRole.ROUND_TRIP.offboarding is True


def Test_ItineraryTransportationStationRole_TestRoleValueHelpers_ExpectSortedKinds() -> None:
   assert ItineraryTransportationStationRole.onboarding_role_values() == sorted(
      member.value
      for member in ItineraryTransportationStationRole
      if member.onboarding
   )
   assert ItineraryTransportationStationRole.offboarding_role_values() == sorted(
      member.value
      for member in ItineraryTransportationStationRole
      if member.offboarding
   )
