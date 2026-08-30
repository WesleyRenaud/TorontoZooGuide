from __future__ import annotations

from api.animals.search.animals_matching_query_builder import AnimalsMatchingQueryBuilder
from api.models.animal import Animal


def _animal(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> Animal:
   return Animal(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name )


def Test_Build_TestEmptyQuery_ExpectSortedAllAnimals() -> None:
   animals = [
      _animal( species='Zebra', exhibit='Africa Savanna' ),
      _animal( species='African Lion', exhibit='Africa Savanna' ),
      _animal( species='Masai Giraffe', exhibit='Africa Savanna' ),
   ]

   matches = AnimalsMatchingQueryBuilder.build( animals, '' )

   assert [ animal.species for animal in matches ] == [
      'African Lion',
      'Masai Giraffe',
      'Zebra',
   ]


def Test_Build_TestSpeciesQuery_ExpectMatchingAnimalOnly() -> None:
   animals = [
      _animal( species='Zebra', exhibit='Africa Savanna' ),
      _animal( species='African Lion', exhibit='Africa Savanna' ),
   ]

   matches = AnimalsMatchingQueryBuilder.build( animals, 'zebra' )

   assert [ animal.species for animal in matches ] == [ 'Zebra' ]


def Test_SortBySpeciesAndExhibit_TestMixedExhibits_ExpectSpeciesThenExhibitOrder() -> None:
   animals = [
      _animal( species='Zebra', exhibit='Tundra Trek', enclosure_name='Outdoor' ),
      _animal( species='Zebra', exhibit='Africa Savanna' ),
      _animal( species='African Lion', exhibit='Africa Savanna', enclosure_name='Indoor' ),
   ]

   sorted_animals = AnimalsMatchingQueryBuilder.sort_by_species_and_exhibit( animals )

   assert [
      ( animal.species, animal.exhibit, animal.enclosure_name )
      for animal in sorted_animals
   ] == [
      ( 'African Lion', 'Africa Savanna', 'Indoor' ),
      ( 'Zebra', 'Africa Savanna', None ),
      ( 'Zebra', 'Tundra Trek', 'Outdoor' ),
   ]
