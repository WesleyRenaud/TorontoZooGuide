from __future__ import annotations

from ...itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...models import Animal
from ..search.animals_matching_query import sort_animals_by_species_and_exhibit
from ..search.animals_matching_query import viewing_spot_key


def _find_saved_animal_for_viewable_animal(
      saved_animals: list[ ItineraryAnimalRecord ],
      animal: Animal ) -> ItineraryAnimalRecord | None:
   spot_key = viewing_spot_key( animal )

   for saved_animal in saved_animals:
      if saved_animal.viewing_spot_key() == spot_key:
         return saved_animal

   return None


def apply_itinerary_animal_old_likelihood(
      animals: list[ Animal ],
      saved_animals: list[ ItineraryAnimalRecord ] ) -> None:
   for animal in animals:
      saved_animal = _find_saved_animal_for_viewable_animal(
         saved_animals,
         animal )

      if saved_animal == None:
         continue

      animal.old_likelihood = saved_animal.old_likelihood


def apply_itinerary_animal_is_added(
      animals: list[ Animal ],
      saved_animals: list[ ItineraryAnimalRecord ] ) -> None:
   for animal in animals:
      saved_animal = _find_saved_animal_for_viewable_animal(
         saved_animals,
         animal )

      if saved_animal == None:
         continue

      animal.is_added = saved_animal.is_added


def apply_itinerary_animal_schedule(
      animals: list[ Animal ],
      saved_animals: list[ ItineraryAnimalRecord ] ) -> None:
   for animal in animals:
      saved_animal = _find_saved_animal_for_viewable_animal(
         saved_animals,
         animal )

      if saved_animal == None:
         continue

      animal.start_time = saved_animal.start_time
      animal.end_time = saved_animal.end_time


def build_itinerary_animals(
      viewable_animals: list[ Animal ],
      saved_animals: list[ ItineraryAnimalRecord ] ) -> list[ Animal ]:
   saved_spot_keys = {
      saved_animal.viewing_spot_key()
      for saved_animal in saved_animals
   }

   animals = [
      animal
      for animal in viewable_animals
      if viewing_spot_key( animal ) in saved_spot_keys
   ]
   animals = sort_animals_by_species_and_exhibit( animals )
   apply_itinerary_animal_old_likelihood( animals, saved_animals )
   apply_itinerary_animal_is_added( animals, saved_animals )
   apply_itinerary_animal_schedule( animals, saved_animals )

   return animals
