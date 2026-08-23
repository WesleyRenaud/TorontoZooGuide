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


def _saved_attraction_row_for_name(
      saved_attraction_rows: list[ ItineraryAttractionRecord ] | None,
      attraction_name: str,
) -> ItineraryAttractionRecord | None:
   return next(
      (
         row
         for row in saved_attraction_rows or []
         if row.attraction == attraction_name
      ),
      None,
   )


def _empty_attraction_save_carryover(
      name: str ) -> ItineraryAttractionSaveCarryover:
   return ItineraryAttractionSaveCarryover(
      name=name,
      old_likelihood=None,
      start_time=None,
      end_time=None,
   )


def _attraction_save_carryover_from_row(
      saved_row: ItineraryAttractionRecord,
      name: str ) -> ItineraryAttractionSaveCarryover:
   return ItineraryAttractionSaveCarryover(
      name=name,
      old_likelihood=saved_row.new_likelihood,
      start_time=saved_row.start_time,
      end_time=saved_row.end_time,
   )


def itinerary_attraction_save_carryover(
      saved_attraction_rows: list[ ItineraryAttractionRecord ] | None,
      name: str,
      old_visit_date: DateKey | None ) -> ItineraryAttractionSaveCarryover:
   if old_visit_date is not None:
      saved_row = _saved_attraction_row_for_name(
         saved_attraction_rows,
         name )

      if saved_row is not None:
         return _attraction_save_carryover_from_row( saved_row, name )

   return _empty_attraction_save_carryover( name )
