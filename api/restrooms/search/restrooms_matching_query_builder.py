from __future__ import annotations

from ...models import Restroom
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key


class RestroomsMatchingQueryBuilder():
   @classmethod
   def _title_key( cls, restroom: Restroom ) -> str:
      return normalize_search_key( restroom.title )


   @classmethod
   def filter_matching_query(
         cls,
         restrooms: list[ Restroom ],
         query: str ) -> list[ Restroom ]:
      return filter_items_matching_query(
         restrooms,
         query,
         cls._title_key )


   @classmethod
   def build(
         cls,
         restrooms: list[ Restroom ],
         query: str ) -> list[ Restroom ]:
      return build_matching_query(
         restrooms,
         query,
         cls._title_key )
