from __future__ import annotations

from enum import Enum


class ItineraryEventType( str, Enum ):
   ARRIVAL = 'arrival'
   BREAKFAST = 'breakfast'
   BREAK = 'break'
   DEPARTURE = 'departure'
   DINNER = 'dinner'
   LUNCH = 'lunch'
   SHOPPING = 'shopping'
   SNACK = 'snack'


   @classmethod
   def normalize( cls, value: str | None ) -> 'ItineraryEventType | None':
      if value is None:
         return None

      normalized_value = value.strip().lower()

      for event_type in cls:
         if normalized_value == event_type.value:
            return event_type

      return None
