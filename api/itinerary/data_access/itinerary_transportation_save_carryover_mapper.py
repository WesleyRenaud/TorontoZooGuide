from __future__ import annotations

from .itinerary_transportation_input import ItineraryTransportationInput
from .itinerary_transportation_record import ItineraryTransportationRecord
from .itinerary_transportation_save_carryover_record import ItineraryTransportationSaveCarryover
from ...types import DateKey


class ItineraryTransportationSaveCarryoverMapper():
   @classmethod
   def _saved_transportation_row_for_input(
         cls,
         saved_transportation_rows: list[ ItineraryTransportationRecord ] | None,
         transportation: ItineraryTransportationInput,
   ) -> ItineraryTransportationRecord | None:
      return next(
         (
            row
            for row in saved_transportation_rows or []
            if row.transportation == transportation.name
            and row.added_as_attraction == transportation.added_as_attraction
         ),
         None,
      )


   @classmethod
   def map_empty_from_input(
         cls,
         transportation: ItineraryTransportationInput ) -> ItineraryTransportationSaveCarryover:
      return ItineraryTransportationSaveCarryover(
         name=transportation.name,
         old_likelihood=None,
         start_time=None,
         end_time=None,
      )


   @classmethod
   def map_from_saved_row(
         cls,
         saved_row: ItineraryTransportationRecord,
         transportation: ItineraryTransportationInput ) -> ItineraryTransportationSaveCarryover:
      return ItineraryTransportationSaveCarryover(
         name=transportation.name,
         old_likelihood=saved_row.new_likelihood,
         start_time=saved_row.start_time,
         end_time=saved_row.end_time,
         legs=saved_row.legs,
         bulk_transit_evaluated=saved_row.bulk_transit_evaluated,
      )


   @classmethod
   def map_from_saved_transportation_rows(
         cls,
         saved_transportation_rows: list[ ItineraryTransportationRecord ] | None,
         transportation: ItineraryTransportationInput,
         old_visit_date: DateKey | None ) -> ItineraryTransportationSaveCarryover:
      if old_visit_date is not None:
         saved_row = cls._saved_transportation_row_for_input(
            saved_transportation_rows,
            transportation )

         if saved_row is not None:
            return cls.map_from_saved_row(
               saved_row,
               transportation )

      return cls.map_empty_from_input( transportation )
