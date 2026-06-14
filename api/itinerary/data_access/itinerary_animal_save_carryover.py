from __future__ import annotations

from dataclasses import dataclass

from ...animals.search.animals_matching_query import species_exhibit_key_from_values
from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_animal_record import ItineraryAnimalRecord
from ...types import DateKey, ScheduleTimeKey


@dataclass( frozen=True )
class ItineraryAnimalSaveCarryover:
   species: str
   exhibit: str
   old_likelihood: int | None
   is_added: bool
   start_time: ScheduleTimeKey
   end_time: ScheduleTimeKey


def itinerary_animal_save_carryover(
      saved_rows: list[ ItineraryAnimalRecord ] | None,
      animal: ItineraryAnimalInput,
      *,
      old_visit_date: DateKey | None ) -> ItineraryAnimalSaveCarryover:
   species = animal.species
   exhibit = animal.exhibit

   if old_visit_date == None:
      return ItineraryAnimalSaveCarryover(
         species=species,
         exhibit=exhibit,
         old_likelihood=None,
         is_added=False,
         start_time=None,
         end_time=None,
      )

   pair = species_exhibit_key_from_values( species, exhibit )

   for row in saved_rows or []:
      if row.species_exhibit_key() == pair:
         return ItineraryAnimalSaveCarryover(
            species=species,
            exhibit=exhibit,
            old_likelihood=row.new_likelihood,
            is_added=animal.is_added or row.is_added,
            start_time=row.start_time,
            end_time=row.end_time,
         )

   return ItineraryAnimalSaveCarryover(
      species=species,
      exhibit=exhibit,
      old_likelihood=None,
      is_added=animal.is_added,
      start_time=None,
      end_time=None,
   )
