from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


ItineraryEventType = Enum(
   'ItineraryEventType',
   SharedEnumValues.load( 'itineraryEventType.json' ),
   type=str,
)


@classmethod
def _normalize( cls: type[ ItineraryEventType ], value: str | None ) -> ItineraryEventType | None:
   if value is None:
      return None

   normalized_value = value.strip().lower()

   for event_type in cls:
      if normalized_value == event_type.value:
         return event_type

   return None


ItineraryEventType.normalize = _normalize
