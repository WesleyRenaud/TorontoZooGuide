from __future__ import annotations

from enum import Enum
from typing import Any

from ..value_conversion import ValueConversion


class EnclosureType( str, Enum ):
   INDOOR = 'Indoor'
   OUTDOOR = 'Outdoor'


   @classmethod
   def normalize(
         cls,
         value: Any ) -> EnclosureType | None:
      normalized_value = ValueConversion.as_trimmed_string( value )

      if not normalized_value:
         return None

      for enclosure_type in cls:
         if normalized_value == enclosure_type.value:
            return enclosure_type

      return None


   @classmethod
   def normalize_viewing_spot_name(
         cls,
         value: Any ) -> str | None:
      normalized = ValueConversion.as_nullable_string( value )

      if normalized is None or cls.normalize( normalized ) is not None:
         return None

      return normalized
