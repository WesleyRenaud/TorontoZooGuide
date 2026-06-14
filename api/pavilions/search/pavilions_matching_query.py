from __future__ import annotations

from ...models import Pavilion
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key
from ...shared.name_matching_query import sort_items_by_key


def pavilion_name_key( pavilion: Pavilion ) -> str:
   return normalize_search_key( pavilion.name )


def filter_pavilions_matching_query(
      pavilions: list[ Pavilion ],
      query: str ) -> list[ Pavilion ]:
   return filter_items_matching_query(
      pavilions,
      query,
      pavilion_name_key )


def sort_pavilions_by_name(
      pavilions: list[ Pavilion ] ) -> list[ Pavilion ]:
   return sort_items_by_key( pavilions, pavilion_name_key )


def build_pavilions_matching_query(
      pavilions: list[ Pavilion ],
      query: str ) -> list[ Pavilion ]:
   return build_matching_query(
      pavilions,
      query,
      pavilion_name_key,
      sort=True )
