from __future__ import annotations

from enum import Enum


class ItineraryTransportationStationRole( str, Enum ):
   ONBOARDING = 'onboarding_station'
   OFFBOARDING = 'offboarding_station'
   ROUND_TRIP = 'round_trip'


   @classmethod
   def onboarding_roles( cls ) -> frozenset[ ItineraryTransportationStationRole ]:
      return frozenset( {
         cls.ONBOARDING,
         cls.ROUND_TRIP,
      } )


   @classmethod
   def offboarding_roles( cls ) -> frozenset[ ItineraryTransportationStationRole ]:
      return frozenset( {
         cls.OFFBOARDING,
         cls.ROUND_TRIP,
      } )


   @classmethod
   def to_config_dict( cls ) -> dict[ str, str ]:
      return {
         role.name: role.value
         for role in cls
      }


   @classmethod
   def onboarding_role_values( cls ) -> list[ str ]:
      return sorted(
         role.value
         for role in cls.onboarding_roles()
      )


   @classmethod
   def offboarding_role_values( cls ) -> list[ str ]:
      return sorted(
         role.value
         for role in cls.offboarding_roles()
      )
