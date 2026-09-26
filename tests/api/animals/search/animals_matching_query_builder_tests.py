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
   zebra = _animal( species='Zebra', exhibit='Africa Savanna' )
   african_lion = _animal( species='African Lion', exhibit='Africa Savanna' )
   masai_giraffe = _animal( species='Masai Giraffe', exhibit='Africa Savanna' )
   animals = [ zebra, african_lion, masai_giraffe ]
   query = ''

   matches = AnimalsMatchingQueryBuilder.build( animals, query )

   assert [ animal.species for animal in matches ] == [
      african_lion.species,
      masai_giraffe.species,
      zebra.species,
   ]


def Test_Build_TestSpeciesQuery_ExpectMatchingAnimalOnly() -> None:
   zebra = _animal( species='Zebra', exhibit='Africa Savanna' )
   african_lion = _animal( species='African Lion', exhibit='Africa Savanna' )
   animals = [ zebra, african_lion ]
   query = 'zebra'

   matches = AnimalsMatchingQueryBuilder.build( animals, query )

   assert [ animal.species for animal in matches ] == [ zebra.species ]


def Test_FilterMatchingQuery_TestSpeciesQuery_ExpectMatchingAnimalOnly() -> None:
   zebra = _animal( species='Zebra', exhibit='Africa Savanna' )
   african_lion = _animal( species='African Lion', exhibit='Africa Savanna' )
   animals = [ zebra, african_lion ]
   query = 'zebra'

   matches = AnimalsMatchingQueryBuilder.filter_matching_query( animals, query )

   assert [ animal.species for animal in matches ] == [ zebra.species ]


def Test_SortBySpeciesAndExhibit_TestMixedExhibits_ExpectSpeciesThenExhibitOrder() -> None:
   tundra_zebra = _animal(
      species='Zebra',
      exhibit='Tundra Trek',
      enclosure_name='Outdoor' )
   savanna_zebra = _animal( species='Zebra', exhibit='Africa Savanna' )
   african_lion = _animal(
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name='Indoor' )
   animals = [ tundra_zebra, savanna_zebra, african_lion ]

   sorted_animals = AnimalsMatchingQueryBuilder.sort_by_species_and_exhibit( animals )

   assert [
      ( animal.species, animal.exhibit, animal.enclosure_name )
      for animal in sorted_animals
   ] == [
      ( african_lion.species, african_lion.exhibit, african_lion.enclosure_name ),
      ( savanna_zebra.species, savanna_zebra.exhibit, savanna_zebra.enclosure_name ),
      ( tundra_zebra.species, tundra_zebra.exhibit, tundra_zebra.enclosure_name ),
   ]
