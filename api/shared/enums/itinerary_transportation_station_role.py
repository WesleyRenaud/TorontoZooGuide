from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


_MEMBERS = SharedEnumValues.load_object_members(
   'itineraryTransportationStationRole.json' )
_ONBOARDING_BY_ROLE: dict[ 'ItineraryTransportationStationRole', bool ] = {}
_OFFBOARDING_BY_ROLE: dict[ 'ItineraryTransportationStationRole', bool ] = {}


class ItineraryTransportationStationRole( str, Enum ):
   # Enum bodies register a member per assigned name, so the shared JSON members
   # have to be written into the class namespace one name at a time.
   _ignore_ = [ 'member_name', 'member_definition' ]

   for member_name, member_definition in _MEMBERS.items():
      locals()[ member_name ] = member_definition[ 'kind' ]


   @property
   def onboarding( self ) -> bool:
      return _ONBOARDING_BY_ROLE.get( self, False )


   @property
   def offboarding( self ) -> bool:
      return _OFFBOARDING_BY_ROLE.get( self, False )


   @classmethod
   def onboarding_roles(
         cls ) -> frozenset[ ItineraryTransportationStationRole ]:
      return frozenset(
         role
         for role in cls
         if role.onboarding
      )


   @classmethod
   def offboarding_roles(
         cls ) -> frozenset[ ItineraryTransportationStationRole ]:
      return frozenset(
         role
         for role in cls
         if role.offboarding
      )


   @classmethod
   def onboarding_role_values( cls ) -> list[ str ]:
      return sorted( role.value for role in cls.onboarding_roles() )


   @classmethod
   def offboarding_role_values( cls ) -> list[ str ]:
      return sorted( role.value for role in cls.offboarding_roles() )


_ONBOARDING_BY_ROLE.update( {
   ItineraryTransportationStationRole[ member_name ]: bool(
      member_definition.get( 'onboarding', False )
   )
   for member_name, member_definition in _MEMBERS.items()
} )
_OFFBOARDING_BY_ROLE.update( {
   ItineraryTransportationStationRole[ member_name ]: bool(
      member_definition.get( 'offboarding', False )
   )
   for member_name, member_definition in _MEMBERS.items()
} )
