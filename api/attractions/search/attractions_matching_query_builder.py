from __future__ import annotations

from ...models import Attraction
from ...shared.name_matching_query_builder import NameMatchingQueryBuilder


class AttractionsMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         attractions: list[ Attraction ],
         query: str ) -> list[ Attraction ]:
      return NameMatchingQueryBuilder.filter_matching( attractions, query, Attraction.name_key )


   @classmethod
   def build(
         cls,
         attractions: list[ Attraction ],
         query: str ) -> list[ Attraction ]:
      return NameMatchingQueryBuilder.build( attractions, query, Attraction.name_key )
