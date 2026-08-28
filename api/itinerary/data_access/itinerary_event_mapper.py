from __future__ import annotations

from .itinerary_event_record import ItineraryEventRecord
from ...shared.enums import ItineraryEventType
from ...types import Types


class ItineraryEventMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ItineraryEventRecord:
      return ItineraryEventRecord(
         event_type=ItineraryEventType.normalize( row[ 'EVENT_TYPE' ] ),
         start_time=row[ 'START_TIME' ],
         end_time=row[ 'END_TIME' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ ItineraryEventRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
