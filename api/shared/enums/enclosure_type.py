from __future__ import annotations

from enum import Enum
from typing import Any

from .shared_enum_values import SharedEnumValues
from ..value_conversion import ValueConversion


EnclosureType = Enum(
   'EnclosureType',
   SharedEnumValues.load( 'enclosureType.json' ),
   type=str,
)


def _viewing_location_label( self: EnclosureType ) -> str:
   if self == EnclosureType.INDOOR:
      return 'inside'

   return 'outside'


def _habitat_label( self: EnclosureType ) -> str:
   if self == EnclosureType.INDOOR:
      return 'indoor'

   return 'outdoor'


@classmethod
def _normalize( cls: type[ EnclosureType ],
      value: Any ) -> EnclosureType | None:
   normalized_value = ValueConversion.as_trimmed_string( value )

   if not normalized_value:
      return None

   for enclosure_type in cls:
      if normalized_value == enclosure_type.value:
         return enclosure_type

   return None


@classmethod
def _normalized_enclosure_type( cls: type[ EnclosureType ],
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
def _is_indoor( cls: type[ EnclosureType ], value: Any ) -> bool:
   return cls.normalized_enclosure_type( value ) == cls.INDOOR.value.lower()


@classmethod
def _is_outdoor( cls: type[ EnclosureType ], value: Any ) -> bool:
   return cls.normalized_enclosure_type( value ) == cls.OUTDOOR.value.lower()


@classmethod
def _opposite_type( cls: type[ EnclosureType ], value: EnclosureType ) -> EnclosureType:
   if value == cls.INDOOR:
      return cls.OUTDOOR

   return cls.INDOOR


@classmethod
def _normalize_viewing_spot_name( cls: type[ EnclosureType ],
      value: Any ) -> str | None:
   normalized = ValueConversion.as_nullable_string( value )

   if normalized is None or cls.normalize( normalized ) is not None:
      return None

   return normalized


EnclosureType.viewing_location_label = property( _viewing_location_label )
EnclosureType.habitat_label = property( _habitat_label )
EnclosureType.normalize = _normalize
EnclosureType.normalized_enclosure_type = _normalized_enclosure_type
EnclosureType.is_indoor = _is_indoor
EnclosureType.is_outdoor = _is_outdoor
EnclosureType.opposite_type = _opposite_type
EnclosureType.normalize_viewing_spot_name = _normalize_viewing_spot_name
