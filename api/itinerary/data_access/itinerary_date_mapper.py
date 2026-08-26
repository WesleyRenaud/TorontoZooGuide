from __future__ import annotations

from .itinerary_date_record import ItineraryDateRecord
from ...shared.calendar_dates import DateValues
from ...types import Row


class ItineraryDateMapper():
   @classmethod
   def map_record( cls, row: Row | None ) -> ItineraryDateRecord | None:
      if row == None:
         return None

      return ItineraryDateRecord(
         itinerary_date=DateValues.normalize_date_key( row[ 'ITINERARY_DATE' ] ),
         arrival_time=DateValues.normalize_itinerary_schedule_time(
            row[ 'ARRIVAL_TIME' ] ),
         departure_time=DateValues.normalize_itinerary_schedule_time(
            row[ 'DEPARTURE_TIME' ] ) )
