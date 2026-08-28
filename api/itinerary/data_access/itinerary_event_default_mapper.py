from __future__ import annotations

from .itinerary_event_default_record import ItineraryEventDefaultRecord
from ...shared.enums import ItineraryEventType
from ...types import Types


class ItineraryEventDefaultMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ItineraryEventDefaultRecord:
      return ItineraryEventDefaultRecord(
         event_type=ItineraryEventType.normalize( row[ 'EVENT_TYPE' ] ),
         default_duration_minutes=int( row[ 'DEFAULT_ITINERARY_DURATION_MINUTES' ] ),
      )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ ItineraryEventDefaultRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
