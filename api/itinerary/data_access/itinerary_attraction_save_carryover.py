from __future__ import annotations

from dataclasses import dataclass

from .itinerary_attraction_record import ItineraryAttractionRecord
from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryAttractionSaveCarryover:
   name: str
   old_likelihood: int | None
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey


def itinerary_attraction_save_carryover(
      saved_rows: list[ ItineraryAttractionRecord ] | None,
      attraction_name: str,
      *,
      old_visit_date: DateKey | None ) -> ItineraryAttractionSaveCarryover:
   if old_visit_date == None:
      return ItineraryAttractionSaveCarryover(
         name=attraction_name,
         old_likelihood=None,
         start_time=None,
         end_time=None,
      )

   for row in saved_rows or []:
      if row.attraction == attraction_name:
         return ItineraryAttractionSaveCarryover(
            name=attraction_name,
            old_likelihood=row.new_likelihood,
            start_time=row.start_time,
            end_time=row.end_time,
         )

   return ItineraryAttractionSaveCarryover(
      name=attraction_name,
      old_likelihood=None,
      start_time=None,
      end_time=None,
   )
