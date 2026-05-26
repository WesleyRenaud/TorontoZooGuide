from __future__ import annotations

from enum import Enum


class AnimalViewingScope( str, Enum ):
   ALL = 'all'
   INDOOR = 'indoor'
   OUTDOOR = 'outdoor'


   @classmethod
   def normalize(
         cls,
         value: str | None ) -> AnimalViewingScope | None:
      if value is None:
         return None

      normalized_value = value.strip().lower()

      for scope in cls:
         if normalized_value == scope.value:
            return scope

      return None


   @classmethod
   def opposite_scope(
         cls,
         value: AnimalViewingScope ) -> AnimalViewingScope | None:
      if value == cls.INDOOR:
         return cls.OUTDOOR

      if value == cls.OUTDOOR:
         return cls.INDOOR

      return None
