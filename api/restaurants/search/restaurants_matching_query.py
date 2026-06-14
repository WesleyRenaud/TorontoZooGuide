from __future__ import annotations

from ...models import Restaurant
from ...shared.name_matching_query import build_matching_query
from ...shared.name_matching_query import filter_items_matching_query
from ...shared.name_matching_query import normalize_search_key


def restaurant_name_key( restaurant: Restaurant ) -> str:
   return normalize_search_key( restaurant.name )


def filter_restaurants_matching_query(
      restaurants: list[ Restaurant ],
      query: str ) -> list[ Restaurant ]:
   return filter_items_matching_query(
      restaurants,
      query,
      restaurant_name_key )


def build_restaurants_matching_query(
      restaurants: list[ Restaurant ],
      query: str ) -> list[ Restaurant ]:
   return build_matching_query(
      restaurants,
      query,
      restaurant_name_key )
