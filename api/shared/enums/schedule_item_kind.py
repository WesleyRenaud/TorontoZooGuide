from __future__ import annotations

from enum import Enum

_ITEM_TYPE_BY_KIND: dict[ 'ScheduleItemKind', str ] = {}


class ScheduleItemKind( str, Enum ):
   ENTRANCE = 'entrance'
   ANIMAL = 'animal'
   ATTRACTION = 'attraction'
   EVENT = 'event'
   GUARDIANS_TALK = 'guardians_talk'
   TRANSPORTATION = 'transportation'
   WILD_ENCOUNTER = 'wild_encounter'


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
   ScheduleItemKind.ANIMAL: 'animals',
   ScheduleItemKind.ATTRACTION: 'attractions',
   ScheduleItemKind.GUARDIANS_TALK: 'guardians_talks',
   ScheduleItemKind.TRANSPORTATION: 'transportations',
   ScheduleItemKind.WILD_ENCOUNTER: 'wild_encounters',
} )
