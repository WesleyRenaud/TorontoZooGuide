from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


ItineraryAdjustmentType = Enum(
   'ItineraryAdjustmentType',
   SharedEnumValues.load( 'itineraryAdjustmentType.json' ),
   type=str,
)
