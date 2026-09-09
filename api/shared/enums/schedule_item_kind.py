from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


_MEMBERS = SharedEnumValues.load_object_members( 'scheduleItemKind.json' )
_ITEM_TYPE_BY_KIND: dict[ 'ScheduleItemKind', str ] = {}


class ScheduleItemKind( str, Enum ):
   # Enum bodies register a member per assigned name, so the shared JSON members
   # have to be written into the class namespace one name at a time.
   _ignore_ = [ 'member_name', 'member_definition' ]

   for member_name, member_definition in _MEMBERS.items():
      locals()[ member_name ] = member_definition[ 'kind' ]


   @property
   def item_type( self ) -> str | None:
      return _ITEM_TYPE_BY_KIND.get( self )


   @classmethod
   def normalize( cls, value: str | None ) -> 'ScheduleItemKind | None':
      if value is None:
         return None

      normalized_value = value.strip().lower()

      for kind in cls:
         if normalized_value == kind.value:
            return kind

      return None


   @classmethod
   def from_item_type( cls, value: str | None ) -> 'ScheduleItemKind | None':
      if value is None:
         return None

      normalized_value = value.strip().lower()

      for kind, item_type in _ITEM_TYPE_BY_KIND.items():
         if normalized_value == item_type:
            return kind

      return cls.normalize( normalized_value )


_ITEM_TYPE_BY_KIND.update( {
   ScheduleItemKind[ member_name ]: member_definition[ 'itemType' ]
   for member_name, member_definition in _MEMBERS.items()
   if 'itemType' in member_definition
} )
