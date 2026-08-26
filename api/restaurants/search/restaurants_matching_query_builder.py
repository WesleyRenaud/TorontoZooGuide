from __future__ import annotations

from ...models import Restaurant
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query


class RestaurantsMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         restaurants: list[ Restaurant ],
         query: str ) -> list[ Restaurant ]:
      return filter_items_matching_query(
         restaurants,
         query,
         Restaurant.name_key )


   @classmethod
   def build(
         cls,
         restaurants: list[ Restaurant ],
         query: str ) -> list[ Restaurant ]:
      return build_matching_query(
         restaurants,
         query,
         Restaurant.name_key )
