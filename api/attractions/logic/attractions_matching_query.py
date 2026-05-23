from __future__ import annotations

from ... import zoo


def attraction_name_key( attraction: zoo.Attraction ) -> str:
   return ( attraction.name or '' ).strip().lower()


def filter_attractions_matching_query(
      attractions: list[ zoo.Attraction ],
      query: str ) -> list[ zoo.Attraction ]:
   if not query:
      return list( attractions )

   query_lower = query.strip().lower()
   return [
      attraction for attraction in attractions
      if query_lower in attraction_name_key( attraction )
   ]


def build_attractions_matching_query(
      attractions: list[ zoo.Attraction ],
      query: str ) -> list[ zoo.Attraction ]:
   return filter_attractions_matching_query(
      attractions,
      query )
