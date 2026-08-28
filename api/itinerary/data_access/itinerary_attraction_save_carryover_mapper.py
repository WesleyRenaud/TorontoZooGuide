from __future__ import annotations

from .itinerary_attraction_record import ItineraryAttractionRecord
from .itinerary_attraction_save_carryover import ItineraryAttractionSaveCarryover
from ...types import Types


class ItineraryAttractionSaveCarryoverMapper():
   @classmethod
   def _saved_attraction_row_for_name(
         cls,
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


   @classmethod
   def map_empty_from_name(
         cls,
         name: str ) -> ItineraryAttractionSaveCarryover:
      return ItineraryAttractionSaveCarryover(
         name=name,
         old_likelihood=None,
         start_time=None,
         end_time=None,
      )


   @classmethod
   def map_from_saved_row(
         cls,
         saved_row: ItineraryAttractionRecord,
         name: str ) -> ItineraryAttractionSaveCarryover:
      return ItineraryAttractionSaveCarryover(
         name=name,
         old_likelihood=saved_row.new_likelihood,
         start_time=saved_row.start_time,
         end_time=saved_row.end_time,
      )


   @classmethod
   def map_from_saved_attraction_rows(
         cls,
         saved_attraction_rows: list[ ItineraryAttractionRecord ] | None,
         name: str,
         old_visit_date: Types.DateKey | None ) -> ItineraryAttractionSaveCarryover:
      if old_visit_date is not None:
         saved_row = cls._saved_attraction_row_for_name(
            saved_attraction_rows,
            name )

         if saved_row is not None:
            return cls.map_from_saved_row( saved_row, name )

      return cls.map_empty_from_name( name )
