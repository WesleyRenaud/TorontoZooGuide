from __future__ import annotations

from ...itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...models import Animal
from ..search.animals_matching_query_builder import AnimalsMatchingQueryBuilder
from ..search.viewing_spot_key_builder import ViewingSpotKeyBuilder


class ItineraryAnimalsBuilder():
   @classmethod
   def _find_saved_animal_for_viewable_animal(
         cls,
         saved_animals: list[ ItineraryAnimalRecord ],
         animal: Animal ) -> ItineraryAnimalRecord | None:
      spot_key = ViewingSpotKeyBuilder.from_animal( animal )

      for saved_animal in saved_animals:
         if saved_animal.viewing_spot_key() == spot_key:
            return saved_animal

      return None


   @classmethod
   def _apply_old_likelihood(
         cls,
         animals: list[ Animal ],
         saved_animals: list[ ItineraryAnimalRecord ] ) -> None:
      for animal in animals:
         saved_animal = cls._find_saved_animal_for_viewable_animal(
            saved_animals,
            animal )

         if saved_animal == None:
            continue

         animal.old_likelihood = saved_animal.old_likelihood


   @classmethod
   def _apply_is_added(
         cls,
         animals: list[ Animal ],
         saved_animals: list[ ItineraryAnimalRecord ] ) -> None:
      for animal in animals:
         saved_animal = cls._find_saved_animal_for_viewable_animal(
            saved_animals,
            animal )

         if saved_animal == None:
            continue

         animal.is_added = saved_animal.is_added


   @classmethod
   def _apply_schedule(
         cls,
         animals: list[ Animal ],
         saved_animals: list[ ItineraryAnimalRecord ] ) -> None:
      for animal in animals:
         saved_animal = cls._find_saved_animal_for_viewable_animal(
            saved_animals,
            animal )

         if saved_animal == None:
            continue

         animal.start_time = saved_animal.start_time
         animal.end_time = saved_animal.end_time
         animal.covered_by_talk = saved_animal.covered_by_talk


   @classmethod
   def build(
         cls,
         viewable_animals: list[ Animal ],
         saved_animals: list[ ItineraryAnimalRecord ] ) -> list[ Animal ]:
      saved_spot_keys = {
         saved_animal.viewing_spot_key()
         for saved_animal in saved_animals
      }

      animals = [
         animal
         for animal in viewable_animals
         if ViewingSpotKeyBuilder.from_animal( animal ) in saved_spot_keys
      ]
      animals = AnimalsMatchingQueryBuilder.sort_by_species_and_exhibit( animals )
      cls._apply_old_likelihood( animals, saved_animals )
      cls._apply_is_added( animals, saved_animals )
      cls._apply_schedule( animals, saved_animals )

      return animals
