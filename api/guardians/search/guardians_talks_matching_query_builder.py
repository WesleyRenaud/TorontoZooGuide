from __future__ import annotations

from ...models import GuardiansTalk
from ...shared.name_matching_query_builder import NameMatchingQueryBuilder


class GuardiansTalksMatchingQueryBuilder():
   @classmethod
   def filter_matching_query(
         cls,
         guardians_talks: list[ GuardiansTalk ],
         query: str ) -> list[ GuardiansTalk ]:
      return NameMatchingQueryBuilder.filter_matching(
         guardians_talks,
         query,
         GuardiansTalk.name_key )


   @classmethod
   def build(
         cls,
         guardians_talks: list[ GuardiansTalk ],
         query: str ) -> list[ GuardiansTalk ]:
      return NameMatchingQueryBuilder.build(
         guardians_talks,
         query,
         GuardiansTalk.name_key )
