from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from .itinerary_transportation_input import ItineraryTransportationInput
from .itinerary_transportation_record import ItineraryTransportationRecord
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryTransportationSaveCarryover:
   name: str
   old_likelihood: int | None
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey
   legs: list[ ItineraryTransportationLeg ] = field( default_factory=list )


def _saved_transportation_row_for_input(
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


def _empty_transportation_save_carryover(
      transportation: ItineraryTransportationInput ) -> ItineraryTransportationSaveCarryover:
   return ItineraryTransportationSaveCarryover(
      name=transportation.name,
      old_likelihood=None,
      start_time=None,
      end_time=None,
   )


def _transportation_save_carryover_from_row(
      saved_row: ItineraryTransportationRecord,
      transportation: ItineraryTransportationInput ) -> ItineraryTransportationSaveCarryover:
   return ItineraryTransportationSaveCarryover(
      name=transportation.name,
      old_likelihood=saved_row.new_likelihood,
      start_time=saved_row.start_time,
      end_time=saved_row.end_time,
      legs=saved_row.legs,
   )


def itinerary_transportation_save_carryover(
      saved_transportation_rows: list[ ItineraryTransportationRecord ] | None,
      transportation: ItineraryTransportationInput,
      old_visit_date: DateKey | None ) -> ItineraryTransportationSaveCarryover:
   if old_visit_date is not None:
      saved_row = _saved_transportation_row_for_input(
         saved_transportation_rows,
         transportation )

      if saved_row is not None:
         return _transportation_save_carryover_from_row(
            saved_row,
            transportation )

   return _empty_transportation_save_carryover( transportation )
