from __future__ import annotations

from .itinerary_attraction_record import ItineraryAttractionRecord
from ...types import Row


def map_itinerary_attraction_record( row: Row ) -> ItineraryAttractionRecord:
   return ItineraryAttractionRecord(
      attraction=row[ 'ATTRACTION' ],
      old_likelihood=row[ 'OLD_LIKELIHOOD' ],
      new_likelihood=row[ 'NEW_LIKELIHOOD' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ] )


def map_itinerary_attraction_records( rows: list[ Row ] ) -> list[ ItineraryAttractionRecord ]:
   return [
      map_itinerary_attraction_record( row )
      for row in rows
   ]
