from __future__ import annotations

from dataclasses import dataclass

from ...animals.search.animals_matching_query import viewing_spot_key_from_values
from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_animal_record import ItineraryAnimalRecord
from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryAnimalSaveCarryover:
   species: str
   exhibit: str
   enclosure_name: str | None
   old_likelihood: int | None
   is_added: bool
   covered_by_talk: bool
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey


def _saved_animal_row_for_input(
      saved_animal_rows: list[ ItineraryAnimalRecord ] | None,
      animal: ItineraryAnimalInput,
) -> ItineraryAnimalRecord | None:
   spot_key = viewing_spot_key_from_values(
      animal.species,
      animal.exhibit,
      animal.enclosure_name )

   return next(
      (
         row
         for row in saved_animal_rows or []
         if row.viewing_spot_key() == spot_key
      ),
      None,
   )


def _empty_animal_save_carryover(
      animal: ItineraryAnimalInput,
      is_added: bool ) -> ItineraryAnimalSaveCarryover:
   return ItineraryAnimalSaveCarryover(
      species=animal.species,
      exhibit=animal.exhibit,
      enclosure_name=animal.enclosure_name,
      old_likelihood=None,
      is_added=is_added,
      covered_by_talk=False,
      start_time=None,
      end_time=None,
   )


def _animal_save_carryover_from_row(
      saved_row: ItineraryAnimalRecord,
      animal: ItineraryAnimalInput ) -> ItineraryAnimalSaveCarryover:
   return ItineraryAnimalSaveCarryover(
      species=animal.species,
      exhibit=animal.exhibit,
      enclosure_name=animal.enclosure_name,
      old_likelihood=saved_row.new_likelihood,
      is_added=animal.is_added or saved_row.is_added,
      covered_by_talk=saved_row.covered_by_talk,
      start_time=saved_row.start_time,
      end_time=saved_row.end_time,
   )


def itinerary_animal_save_carryover(
      saved_animal_rows: list[ ItineraryAnimalRecord ] | None,
      animal: ItineraryAnimalInput,
      old_visit_date: DateKey | None ) -> ItineraryAnimalSaveCarryover:
   if old_visit_date is None:
      return _empty_animal_save_carryover( animal, is_added=False )

   saved_row = _saved_animal_row_for_input( saved_animal_rows, animal )

   if saved_row is None:
      return _empty_animal_save_carryover( animal, is_added=animal.is_added )

   return _animal_save_carryover_from_row( saved_row, animal )
