from .animals_matching_query import filter_animals_by_species_exhibit_keys
from .animals_matching_query import sort_animals_by_species_and_exhibit
from .animals_matching_query import species_exhibit_key


def species_key( animal ):
   return species_exhibit_key( animal )[ 0 ]


def keep_viewable_animals_per_species( animals ):
   animals_by_species = {}

   for animal in animals:
      animals_by_species.setdefault( species_key( animal ), [] ).append( animal )

   kept_animals = []

   for species_animals in animals_by_species.values():
      viewable_animals = [
         animal for animal in species_animals
         if animal.likelihood > 0
      ]

      if viewable_animals:
         kept_animals.extend( viewable_animals )
      else:
         kept_animals.extend( species_animals )

   return kept_animals


def apply_itinerary_animal_old_likelihood( animals, saved_animals ):
   saved_animal_by_pair = {
      saved_animal.species_exhibit_key(): saved_animal
      for saved_animal in saved_animals
   }

   for animal in animals:
      saved_animal = saved_animal_by_pair.get( species_exhibit_key( animal ) )

      if saved_animal == None:
         continue

      animal.old_likelihood = saved_animal.old_likelihood


def build_itinerary_animals( viewable_animals, saved_animals ):
   species_exhibit_pairs = [
      saved_animal.species_exhibit_key()
      for saved_animal in saved_animals
   ]

   animals = filter_animals_by_species_exhibit_keys(
      viewable_animals,
      species_exhibit_pairs )
   animals = keep_viewable_animals_per_species( animals )
   animals = sort_animals_by_species_and_exhibit( animals )
   apply_itinerary_animal_old_likelihood( animals, saved_animals )

   return animals
