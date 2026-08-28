from __future__ import annotations

from ...models import Transportation
from ...shared.name_matching_query_builder import NameMatchingQueryBuilder


class TransportationsMatchingQueryBuilder():
   @classmethod
   def build(
         cls,
         transportations: list[ Transportation ],
         query: str ) -> list[ Transportation ]:
      return NameMatchingQueryBuilder.build(
         transportations,
         query,
         Transportation.name_key )
