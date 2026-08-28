from __future__ import annotations

from ...models import Restaurant
from ...shared.name_matching_query_builder import NameMatchingQueryBuilder


class RestaurantsMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         restaurants: list[ Restaurant ],
         query: str ) -> list[ Restaurant ]:
      return NameMatchingQueryBuilder.filter_matching(
         restaurants,
         query,
         Restaurant.name_key )


   @classmethod
   def build(
         cls,
         restaurants: list[ Restaurant ],
         query: str ) -> list[ Restaurant ]:
      return NameMatchingQueryBuilder.build(
         restaurants,
         query,
         Restaurant.name_key )
