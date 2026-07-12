from __future__ import annotations

from typing import Any

from ...models import Animal
from ...shared.name_matching_query import normalize_search_key
from ...shared.value_conversion import ValueConversion


def species_exhibit_key_from_values( species: str, exhibit: str ) -> tuple[ str, str ]:
   return (
      normalize_search_key( species ),
      normalize_search_key( exhibit ),
   )


def viewing_spot_name_from_value( value: Any ) -> str | None:
   return ValueConversion.as_nullable_string( value )


def viewing_spot_key_from_values(
      species: str,
      exhibit: str,
      enclosure_name: Any = None ) -> tuple[ str, str, str | None ]:
   return (
      *species_exhibit_key_from_values( species, exhibit ),
      viewing_spot_name_from_value( enclosure_name ),
   )


def species_exhibit_key( animal: Animal ) -> tuple[ str, str ]:
   return species_exhibit_key_from_values( animal.species, animal.exhibit )


def species_exhibit_keys( animals: list[ Any ] ) -> set[ tuple[ str, str ] ]:
   return {
      species_exhibit_key_from_values( animal.species, animal.exhibit )
      for animal in animals
   }


def viewing_spot_key( animal: Animal ) -> tuple[ str, str, str | None ]:
   return viewing_spot_key_from_values(
      animal.species,
      animal.exhibit,
      animal.enclosure_name )


def animal_matches_query( animal: Animal, query_lower: str ) -> bool:
   species, _exhibit = species_exhibit_key( animal )
   return query_lower in species


def filter_animals_matching_query(
      animals: list[ Animal ],
      query: str ) -> list[ Animal ]:
   if not query:
      return list( animals )

   query_lower = query.strip().lower()
   return [
      animal for animal in animals
      if animal_matches_query( animal, query_lower )
   ]


def filter_animals_by_species_exhibit_keys(
      animals: list[ Animal ],
      species_exhibit_keys: list[ tuple[ str, str ] ] ) -> list[ Animal ]:
   keys = set( species_exhibit_keys )

   if not keys:
      return []

   return [
      animal for animal in animals
      if species_exhibit_key( animal ) in keys
   ]


def sort_animals_by_species_and_exhibit(
      animals: list[ Animal ] ) -> list[ Animal ]:
   def sort_key( animal: Animal ) -> tuple[ str, str, str ]:
      species, exhibit, enclosure_name = viewing_spot_key( animal )
      return ( species, exhibit, enclosure_name or '' )

   sorted_animals = list( animals )
   sorted_animals.sort( key=sort_key )
   return sorted_animals


def build_animals_matching_query(
      animals: list[ Animal ],
      query: str ) -> list[ Animal ]:
   animals = filter_animals_matching_query( animals, query )
   return sort_animals_by_species_and_exhibit( animals )
