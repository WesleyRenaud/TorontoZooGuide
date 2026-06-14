from __future__ import annotations

from ...models import Restaurant


def restaurant_name_key( restaurant: Restaurant ) -> str:
   return ( restaurant.name or '' ).strip().lower()


def filter_restaurants_matching_query(
      restaurants: list[ Restaurant ],
      query: str ) -> list[ Restaurant ]:
   if not query:
      return list( restaurants )

   query_lower = query.strip().lower()
   return [
      restaurant for restaurant in restaurants
      if query_lower in restaurant_name_key( restaurant )
   ]


def build_restaurants_matching_query(
      restaurants: list[ Restaurant ],
      query: str ) -> list[ Restaurant ]:
   return filter_restaurants_matching_query(
      restaurants,
      query )
