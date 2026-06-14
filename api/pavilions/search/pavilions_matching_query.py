from __future__ import annotations

from ...models import Pavilion


def pavilion_name_key( pavilion: Pavilion ) -> str:
   return ( pavilion.name or '' ).strip().lower()


def filter_pavilions_matching_query(
      pavilions: list[ Pavilion ],
      query: str ) -> list[ Pavilion ]:
   if not query:
      return list( pavilions )

   query_lower = query.strip().lower()
   return [
      pavilion for pavilion in pavilions
      if query_lower in pavilion_name_key( pavilion )
   ]


def sort_pavilions_by_name(
      pavilions: list[ Pavilion ] ) -> list[ Pavilion ]:
   sorted_pavilions = list( pavilions )
   sorted_pavilions.sort( key=pavilion_name_key )
   return sorted_pavilions


def build_pavilions_matching_query(
      pavilions: list[ Pavilion ],
      query: str ) -> list[ Pavilion ]:
   pavilions = filter_pavilions_matching_query( pavilions, query )
   return sort_pavilions_by_name( pavilions )
