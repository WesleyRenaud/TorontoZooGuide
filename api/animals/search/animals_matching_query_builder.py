from __future__ import annotations

from ...models import Animal
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from .viewing_spot_key_builder import ViewingSpotKeyBuilder


class AnimalsMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         animals: list[ Animal ],
         query: str ) -> list[ Animal ]:
      return filter_items_matching_query(
         animals,
         query,
         Animal.name_key )


   @classmethod
   def sort_by_species_and_exhibit(
         cls,
         animals: list[ Animal ] ) -> list[ Animal ]:
      def sort_key( animal: Animal ) -> tuple[ str, str, str ]:
         species, exhibit, enclosure_name = ViewingSpotKeyBuilder.from_animal( animal )
         return ( species, exhibit, enclosure_name or '' )

      sorted_animals = list( animals )
      sorted_animals.sort( key=sort_key )
      return sorted_animals


   @classmethod
   def build(
         cls,
         animals: list[ Animal ],
         query: str ) -> list[ Animal ]:
      filtered = build_matching_query(
         animals,
         query,
         Animal.name_key )
      return cls.sort_by_species_and_exhibit( filtered )
