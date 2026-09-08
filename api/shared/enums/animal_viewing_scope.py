from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


AnimalViewingScope = Enum(
   'AnimalViewingScope',
   SharedEnumValues.load( 'animalViewingScope.json' ),
   type=str,
)


@classmethod
def _normalize( cls: type[ AnimalViewingScope ],
      value: str | None ) -> AnimalViewingScope | None:
   if value is None:
      return None

   normalized_value = value.strip().lower()

   for scope in cls:
      if normalized_value == scope.value:
         return scope

   return None


@classmethod
def _opposite_scope( cls: type[ AnimalViewingScope ],
      value: AnimalViewingScope ) -> AnimalViewingScope | None:
   if value == cls.INDOOR:
      return cls.OUTDOOR

   if value == cls.OUTDOOR:
      return cls.INDOOR

   return None


AnimalViewingScope.normalize = _normalize
AnimalViewingScope.opposite_scope = _opposite_scope
