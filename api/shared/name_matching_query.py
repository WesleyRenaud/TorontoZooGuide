from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar( 'T' )


def normalize_search_key( value: str | None ) -> str:
   return ( value or '' ).strip().lower()


def filter_items_matching_query(
      items: list[ T ],
      query: str,
      key_fn: Callable[ [ T ], str ] ) -> list[ T ]:
   if not query:
      return list( items )

   query_lower = query.strip().lower()
   return [
      item for item in items
      if query_lower in key_fn( item )
   ]


def sort_items_by_key(
      items: list[ T ],
      key_fn: Callable[ [ T ], str ] ) -> list[ T ]:
   sorted_items = list( items )
   sorted_items.sort( key=key_fn )
   return sorted_items


def build_matching_query(
      items: list[ T ],
      query: str,
      key_fn: Callable[ [ T ], str ],
      *,
      sort: bool = False ) -> list[ T ]:
   filtered = filter_items_matching_query( items, query, key_fn )

   if sort:
      return sort_items_by_key( filtered, key_fn )

   return filtered
