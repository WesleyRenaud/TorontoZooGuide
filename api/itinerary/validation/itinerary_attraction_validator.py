from __future__ import annotations

from datetime import date

from ...attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ..data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ..data_access.itinerary_attraction_save_carryover_mapper import ItineraryAttractionSaveCarryoverMapper
from ..domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder
from ...models import AttractionDiff
from ...types import DateKey, ScheduleTimeKey


class ItineraryAttractionValidator():
   @classmethod
   def validate(
         cls,
         attraction_coordinator: type[ AttractionCoordinator ],
         attractions: list[ str ],
         new_visit_date: date,
         *,
         arrival_time: ScheduleTimeKey,
         departure_time: ScheduleTimeKey,
         old_visit_date: DateKey | None = None,
         saved_attraction_rows: list[ ItineraryAttractionRecord ] | None = None,
         visit_date_is_changing: bool = False ) -> list[ AttractionDiff ]:
      diffs: list[ AttractionDiff ] = []

      for attraction_name in attractions:
         carryover = ItineraryAttractionSaveCarryoverMapper.map_from_saved_attraction_rows(
            saved_attraction_rows,
            attraction_name,
            old_visit_date=old_visit_date )

         new_likelihood = attraction_coordinator.get_attraction_likelihood_for_visit_date(
            visit_date=new_visit_date,
            attraction_name=attraction_name )
         start_time, end_time = (
            ( carryover.start_time, carryover.end_time )
            if visit_date_is_changing
            else ItineraryVisitWindowBuilder.cleared_schedule_times(
               carryover.start_time,
               carryover.end_time,
               arrival_time=arrival_time,
               departure_time=departure_time ) )

         diffs.append(
            AttractionDiff(
               name=carryover.name,
               old_likelihood=carryover.old_likelihood,
               new_likelihood=new_likelihood,
               start_time=start_time,
               end_time=end_time,
            )
         )

      return diffs
