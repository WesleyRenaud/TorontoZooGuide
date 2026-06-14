from __future__ import annotations

from ...models import Attraction
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key


def attraction_name_key( attraction: Attraction ) -> str:
   return normalize_search_key( attraction.name )


def filter_attractions_matching_query(
      attractions: list[ Attraction ],
      query: str ) -> list[ Attraction ]:
   return filter_items_matching_query(
      attractions,
      query,
      attraction_name_key )


def build_attractions_matching_query(
      attractions: list[ Attraction ],
      query: str ) -> list[ Attraction ]:
   return build_matching_query(
      attractions,
      query,
      attraction_name_key )
