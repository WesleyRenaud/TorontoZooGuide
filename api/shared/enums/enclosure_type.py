from __future__ import annotations

from enum import Enum
from typing import Any

from ..value_conversion import ValueConversion


class EnclosureType( str, Enum ):
   INDOOR = 'Indoor'
   OUTDOOR = 'Outdoor'


   @property
   def viewing_location_label( self ) -> str:
      if self == EnclosureType.INDOOR:
         return 'inside'

      return 'outside'


   @property
   def habitat_label( self ) -> str:
      if self == EnclosureType.INDOOR:
         return 'indoor'

      return 'outdoor'


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
   def normalized_enclosure_type(
         cls,
         value: Any ) -> str | None:
      if value is None:
         return None

      normalized_value = ValueConversion.as_trimmed_string( value ).lower()

      if not normalized_value:
         return None

      for enclosure_type in cls:
         if normalized_value == enclosure_type.value.lower():
            return normalized_value

      return None


   @classmethod
   def is_indoor( cls, value: Any ) -> bool:
      return cls.normalized_enclosure_type( value ) == cls.INDOOR.value.lower()


   @classmethod
   def is_outdoor( cls, value: Any ) -> bool:
      return cls.normalized_enclosure_type( value ) == cls.OUTDOOR.value.lower()


   @classmethod
   def opposite_type( cls, value: EnclosureType ) -> EnclosureType:
      if value == cls.INDOOR:
         return cls.OUTDOOR

      return cls.INDOOR


   @classmethod
   def normalize_viewing_spot_name(
         cls,
         value: Any ) -> str | None:
      normalized = ValueConversion.as_nullable_string( value )

      if normalized is None or cls.normalize( normalized ) is not None:
         return None

      return normalized
