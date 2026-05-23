from __future__ import annotations

from ... import zoo


def restroom_title_key( restroom: zoo.Restroom ) -> str:
   return ( restroom.title or '' ).strip().lower()


def filter_restrooms_matching_query(
      restrooms: list[ zoo.Restroom ],
      query: str ) -> list[ zoo.Restroom ]:
   if not query:
      return list( restrooms )

   query_lower = query.strip().lower()
   return [
      restroom for restroom in restrooms
      if query_lower in restroom_title_key( restroom )
   ]


def build_restrooms_matching_query(
      restrooms: list[ zoo.Restroom ],
      query: str ) -> list[ zoo.Restroom ]:
   return filter_restrooms_matching_query(
      restrooms,
      query )
