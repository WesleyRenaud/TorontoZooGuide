from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from .text_values import TextValues

T = TypeVar( 'T' )


class NameMatchingQueryBuilder():
   @classmethod
   def filter_matching(
         cls,
         items: list[ T ],
         query: str,
         key_fn: Callable[ [ T ], str ] ) -> list[ T ]:
      if not query:
         return list( items )

      query_lower = TextValues.normalize_for_matching( query )
      return [
         item for item in items
         if query_lower in key_fn( item )
      ]


   @classmethod
   def sort_by_key(
         cls,
         items: list[ T ],
         key_fn: Callable[ [ T ], str ] ) -> list[ T ]:
      sorted_items = list( items )
      sorted_items.sort( key=key_fn )
      return sorted_items


   @classmethod
   def build(
         cls,
         items: list[ T ],
         query: str,
         key_fn: Callable[ [ T ], str ],
         *,
         sort: bool = False ) -> list[ T ]:
      filtered = cls.filter_matching( items, query, key_fn )

      if sort:
         return cls.sort_by_key( filtered, key_fn )

      return filtered
