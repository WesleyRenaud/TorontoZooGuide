from __future__ import annotations

from ...models import Attraction
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query


class AttractionsMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         attractions: list[ Attraction ],
         query: str ) -> list[ Attraction ]:
      return filter_items_matching_query( attractions, query, Attraction.name_key )


   @classmethod
   def build(
         cls,
         attractions: list[ Attraction ],
         query: str ) -> list[ Attraction ]:
      return build_matching_query( attractions, query, Attraction.name_key )
