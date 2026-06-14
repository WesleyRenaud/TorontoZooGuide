from __future__ import annotations

from ...models import Restroom
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key


def restroom_title_key( restroom: Restroom ) -> str:
   return normalize_search_key( restroom.title )


def filter_restrooms_matching_query(
      restrooms: list[ Restroom ],
      query: str ) -> list[ Restroom ]:
   return filter_items_matching_query(
      restrooms,
      query,
      restroom_title_key )


def build_restrooms_matching_query(
      restrooms: list[ Restroom ],
      query: str ) -> list[ Restroom ]:
   return build_matching_query(
      restrooms,
      query,
      restroom_title_key )
