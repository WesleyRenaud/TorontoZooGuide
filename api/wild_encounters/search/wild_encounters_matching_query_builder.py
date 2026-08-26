from __future__ import annotations

from ...models import WildEncounter
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query


class WildEncountersMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         wild_encounters: list[ WildEncounter ],
         query: str ) -> list[ WildEncounter ]:
      return filter_items_matching_query(
         wild_encounters,
         query,
         WildEncounter.name_key )


   @classmethod
   def build(
         cls,
         wild_encounters: list[ WildEncounter ],
         query: str ) -> list[ WildEncounter ]:
      return build_matching_query(
         wild_encounters,
         query,
         WildEncounter.name_key )
