from __future__ import annotations

from ...models import Restroom


def restroom_title_key( restroom: Restroom ) -> str:
   return ( restroom.title or '' ).strip().lower()


def filter_restrooms_matching_query(
      restrooms: list[ Restroom ],
      query: str ) -> list[ Restroom ]:
   if not query:
      return list( restrooms )

   query_lower = query.strip().lower()
   return [
      restroom for restroom in restrooms
      if query_lower in restroom_title_key( restroom )
   ]


def build_restrooms_matching_query(
      restrooms: list[ Restroom ],
      query: str ) -> list[ Restroom ]:
   return filter_restrooms_matching_query(
      restrooms,
      query )
