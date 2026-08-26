from __future__ import annotations

from .itinerary_attraction_record import ItineraryAttractionRecord
from ...types import Row


class ItineraryAttractionMapper():
   @classmethod
   def map_record( cls, row: Row ) -> ItineraryAttractionRecord:
      return ItineraryAttractionRecord(
         attraction=row[ 'ATTRACTION' ],
         old_likelihood=row[ 'OLD_LIKELIHOOD' ],
         new_likelihood=row[ 'NEW_LIKELIHOOD' ],
         start_time=row[ 'START_TIME' ],
         end_time=row[ 'END_TIME' ] )


   @classmethod
   def map_records( cls, rows: list[ Row ] ) -> list[ ItineraryAttractionRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
