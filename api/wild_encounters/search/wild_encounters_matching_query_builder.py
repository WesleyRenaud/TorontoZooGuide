from __future__ import annotations

from ...models import WildEncounter
from ...shared.name_matching_query_builder import NameMatchingQueryBuilder


class WildEncountersMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         wild_encounters: list[ WildEncounter ],
         query: str ) -> list[ WildEncounter ]:
      return NameMatchingQueryBuilder.filter_matching(
         wild_encounters,
         query,
         WildEncounter.name_key )


   @classmethod
   def build(
         cls,
         wild_encounters: list[ WildEncounter ],
         query: str ) -> list[ WildEncounter ]:
      return NameMatchingQueryBuilder.build(
         wild_encounters,
         query,
         WildEncounter.name_key )
