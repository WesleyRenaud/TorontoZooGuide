from __future__ import annotations

from collections.abc import Iterable

from .itinerary_event_default_record import ItineraryEventDefaultRecord
from ...shared.enums import ItineraryEventType
from ...types import Row


def map_itinerary_event_default_record( row: Row ) -> ItineraryEventDefaultRecord:
   return ItineraryEventDefaultRecord(
      event_type=ItineraryEventType.normalize( row[ 'EVENT_TYPE' ] ),
      default_duration_minutes=int( row[ 'DEFAULT_ITINERARY_DURATION_MINUTES' ] ),
   )


def map_itinerary_event_default_records(
      rows: Iterable[ Row ] ) -> list[ ItineraryEventDefaultRecord ]:
   return [
      map_itinerary_event_default_record( row )
      for row in rows
   ]
