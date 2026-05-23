from __future__ import annotations

from ...models import Attraction


def attraction_name_key( attraction: Attraction ) -> str:
   return ( attraction.name or '' ).strip().lower()


def filter_attractions_matching_query(
      attractions: list[ Attraction ],
      query: str ) -> list[ Attraction ]:
   if not query:
      return list( attractions )

   query_lower = query.strip().lower()
   return [
      attraction for attraction in attractions
      if query_lower in attraction_name_key( attraction )
   ]


def build_attractions_matching_query(
      attractions: list[ Attraction ],
      query: str ) -> list[ Attraction ]:
   return filter_attractions_matching_query(
      attractions,
      query )
