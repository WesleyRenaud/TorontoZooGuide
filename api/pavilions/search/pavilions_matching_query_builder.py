from __future__ import annotations

from ...models import Pavilion
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key
from ...shared.name_matching_query import sort_items_by_key


class PavilionsMatchingQueryBuilder():
   @classmethod
   def _name_key( cls, pavilion: Pavilion ) -> str:
      return normalize_search_key( pavilion.name )


   @classmethod
   def filter_matching_query(
         cls,
         pavilions: list[ Pavilion ],
         query: str ) -> list[ Pavilion ]:
      return filter_items_matching_query(
         pavilions,
         query,
         cls._name_key )


   @classmethod
   def sort_by_name(
         cls,
         pavilions: list[ Pavilion ] ) -> list[ Pavilion ]:
      return sort_items_by_key( pavilions, cls._name_key )


   @classmethod
   def build(
         cls,
         pavilions: list[ Pavilion ],
         query: str ) -> list[ Pavilion ]:
      return build_matching_query(
         pavilions,
         query,
         cls._name_key,
         sort=True )
