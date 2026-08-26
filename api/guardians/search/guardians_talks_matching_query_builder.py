from __future__ import annotations

from ...models import GuardiansTalk
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query


class GuardiansTalksMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         guardians_talks: list[ GuardiansTalk ],
         query: str ) -> list[ GuardiansTalk ]:
      return filter_items_matching_query(
         guardians_talks,
         query,
         GuardiansTalk.name_key )


   @classmethod
   def build(
         cls,
         guardians_talks: list[ GuardiansTalk ],
         query: str ) -> list[ GuardiansTalk ]:
      return build_matching_query(
         guardians_talks,
         query,
         GuardiansTalk.name_key )
