from __future__ import annotations

from ...animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from .itinerary_animal_input import ItineraryAnimalInput
from .itinerary_animal_record import ItineraryAnimalRecord
from .itinerary_animal_save_carryover_record import ItineraryAnimalSaveCarryover
from ...types import DateKey


class ItineraryAnimalSaveCarryoverMapper():
   @classmethod
   def _saved_animal_row_for_input(
         cls,
         saved_animal_rows: list[ ItineraryAnimalRecord ] | None,
         animal: ItineraryAnimalInput,
   ) -> ItineraryAnimalRecord | None:
      spot_key = ViewingSpotKeyBuilder.from_values(
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


   @classmethod
   def map_empty_from_input(
         cls,
         animal: ItineraryAnimalInput,
         *,
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


   @classmethod
   def map_from_input_and_saved_row(
         cls,
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


   @classmethod
   def map_from_saved_animal_rows(
         cls,
         saved_animal_rows: list[ ItineraryAnimalRecord ] | None,
         animal: ItineraryAnimalInput,
         old_visit_date: DateKey | None ) -> ItineraryAnimalSaveCarryover:
      if old_visit_date is None:
         return cls.map_empty_from_input( animal, is_added=False )

      saved_row = cls._saved_animal_row_for_input( saved_animal_rows, animal )

      if saved_row is None:
         return cls.map_empty_from_input( animal, is_added=animal.is_added )

      return cls.map_from_input_and_saved_row( saved_row, animal )
