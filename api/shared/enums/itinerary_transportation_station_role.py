from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


ItineraryTransportationStationRole = Enum(
   'ItineraryTransportationStationRole',
   SharedEnumValues.load( 'itineraryTransportationStationRole.json' ),
   type=str,
)


@classmethod
def _onboarding_roles(
      cls: type[ ItineraryTransportationStationRole ],
      ) -> frozenset[ ItineraryTransportationStationRole ]:
   return frozenset( {
      cls.ONBOARDING,
      cls.ROUND_TRIP,
   } )


@classmethod
def _offboarding_roles(
      cls: type[ ItineraryTransportationStationRole ],
      ) -> frozenset[ ItineraryTransportationStationRole ]:
   return frozenset( {
      cls.OFFBOARDING,
      cls.ROUND_TRIP,
   } )


@classmethod
def _to_config_dict(
      cls: type[ ItineraryTransportationStationRole ] ) -> dict[ str, str ]:
   return {
      role.name: role.value
      for role in cls
   }


@classmethod
def _onboarding_role_values(
      cls: type[ ItineraryTransportationStationRole ] ) -> list[ str ]:
   return sorted(
      role.value
      for role in cls.onboarding_roles()
   )


@classmethod
def _offboarding_role_values(
      cls: type[ ItineraryTransportationStationRole ] ) -> list[ str ]:
   return sorted(
      role.value
      for role in cls.offboarding_roles()
   )


ItineraryTransportationStationRole.onboarding_roles = _onboarding_roles
ItineraryTransportationStationRole.offboarding_roles = _offboarding_roles
ItineraryTransportationStationRole.to_config_dict = _to_config_dict
ItineraryTransportationStationRole.onboarding_role_values = _onboarding_role_values
ItineraryTransportationStationRole.offboarding_role_values = _offboarding_role_values
