from __future__ import annotations

from .itinerary_event_record import ItineraryEventRecord
from ...shared.enums import ItineraryEventType
from ...types import Row


def map_itinerary_event_record( row: Row ) -> ItineraryEventRecord:
   return ItineraryEventRecord(
      event_type=ItineraryEventType.normalize( row[ 'EVENT_TYPE' ] ),
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ] )


def map_itinerary_event_records(
      rows: list[ Row ] ) -> list[ ItineraryEventRecord ]:
   return [
      map_itinerary_event_record( row )
      for row in rows
   ]
