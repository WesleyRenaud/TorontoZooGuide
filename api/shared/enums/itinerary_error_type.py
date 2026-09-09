from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


ItineraryErrorType = Enum(
   'ItineraryErrorType',
   SharedEnumValues.load( 'itineraryErrorType.json' ),
   type=str,
)
