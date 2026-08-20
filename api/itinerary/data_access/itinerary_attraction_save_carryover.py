from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .itinerary_attraction_record import ItineraryAttractionRecord
from .itinerary_transportation_record import ItineraryTransportationRecord
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...types import DateKey, ScheduleTimeKey


ItineraryNamedSaveRow = ItineraryAttractionRecord | ItineraryTransportationRecord


@dataclass( frozen=True )
class ItineraryAttractionSaveCarryover:
   name: str
   old_likelihood: int | None
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
   legs: list[ ItineraryTransportationLeg ] = field( default_factory=list )


def itinerary_attraction_save_carryover(
      saved_rows: list[ ItineraryNamedSaveRow ] | None,
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
            legs=list( row.legs )
            if isinstance( row, ItineraryTransportationRecord )
            else [],
         )

   return ItineraryAttractionSaveCarryover(
      name=attraction_name,
      old_likelihood=None,
      start_time=None,
      end_time=None,
   )
