from __future__ import annotations

from ...models import Transportation
from ...shared.name_matching_query import build_matching_query


class TransportationsMatchingQueryBuilder():
   @classmethod
   def build(
         cls,
         transportations: list[ Transportation ],
         query: str ) -> list[ Transportation ]:
      return build_matching_query(
         transportations,
         query,
         Transportation.name_key )
