from __future__ import annotations

from ...itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...models import Animal
from ..search.animals_matching_query import filter_animals_by_species_exhibit_keys
from ..search.animals_matching_query import sort_animals_by_species_and_exhibit
from ..search.animals_matching_query import species_exhibit_key


def apply_itinerary_animal_old_likelihood(
      animals: list[ Animal ],
      saved_animals: list[ ItineraryAnimalRecord ] ) -> None:
   saved_animal_by_pair = {
      saved_animal.species_exhibit_key(): saved_animal
      for saved_animal in saved_animals
   }

   for animal in animals:
      saved_animal = saved_animal_by_pair.get( species_exhibit_key( animal ) )

      if saved_animal == None:
         continue

      animal.old_likelihood = saved_animal.old_likelihood


def apply_itinerary_animal_is_added(
      animals: list[ Animal ],
      saved_animals: list[ ItineraryAnimalRecord ] ) -> None:
   saved_animal_by_pair = {
      saved_animal.species_exhibit_key(): saved_animal
      for saved_animal in saved_animals
   }

   for animal in animals:
      saved_animal = saved_animal_by_pair.get( species_exhibit_key( animal ) )

      if saved_animal == None:
         continue

      animal.is_added = saved_animal.is_added


def apply_itinerary_animal_schedule(
      animals: list[ Animal ],
      saved_animals: list[ ItineraryAnimalRecord ] ) -> None:
   saved_animal_by_pair = {
      saved_animal.species_exhibit_key(): saved_animal
      for saved_animal in saved_animals
   }

   for animal in animals:
      saved_animal = saved_animal_by_pair.get( species_exhibit_key( animal ) )

      if saved_animal == None:
         continue

      animal.start_time = saved_animal.start_time
      animal.end_time = saved_animal.end_time


def build_itinerary_animals(
      viewable_animals: list[ Animal ],
      saved_animals: list[ ItineraryAnimalRecord ] ) -> list[ Animal ]:
   species_exhibit_pairs = [
      saved_animal.species_exhibit_key()
      for saved_animal in saved_animals
   ]

   animals = filter_animals_by_species_exhibit_keys(
      viewable_animals,
      species_exhibit_pairs )
   animals = sort_animals_by_species_and_exhibit( animals )
   apply_itinerary_animal_old_likelihood( animals, saved_animals )
   apply_itinerary_animal_is_added( animals, saved_animals )
   apply_itinerary_animal_schedule( animals, saved_animals )

   return animals
