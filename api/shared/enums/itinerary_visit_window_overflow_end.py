from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


ItineraryVisitWindowOverflowEnd = Enum(
   'ItineraryVisitWindowOverflowEnd',
   SharedEnumValues.load( 'itineraryVisitWindowOverflowEnd.json' ),
   type=str,
)
