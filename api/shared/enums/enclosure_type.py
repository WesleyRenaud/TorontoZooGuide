from __future__ import annotations

from enum import Enum


class EnclosureType( str, Enum ):
   INDOOR = 'Indoor'
   OUTDOOR = 'Outdoor'


   @classmethod
   def normalize(
         cls,
         value: str | None ) -> EnclosureType | None:
      if value is None:
         return None

      normalized_value = value.strip()

      for enclosure_type in cls:
         if normalized_value == enclosure_type.value:
            return enclosure_type

      return None
