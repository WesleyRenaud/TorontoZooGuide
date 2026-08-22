from __future__ import annotations

from ...models import Transportation
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import normalize_search_key


def transportation_name_key( transportation: Transportation ) -> str:
   return normalize_search_key( transportation.name )


def build_transportations_matching_query(
      transportations: list[ Transportation ],
      query: str ) -> list[ Transportation ]:
   return build_matching_query(
      transportations,
      query,
      transportation_name_key )
