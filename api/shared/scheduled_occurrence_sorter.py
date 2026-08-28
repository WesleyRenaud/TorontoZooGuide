from __future__ import annotations

from collections.abc import Callable
from typing import Any


class ScheduledOccurrenceSorter():
   @classmethod
   def unique_sorted_by_key(
         cls,
         items: list[ Any ],
         *,
         key: Callable[ [ Any ], Any ],
         sort_key: Callable[ [ Any ], Any ] ) -> list[ Any ]:
      return sorted(
         {
            key( item ): item
            for item in items
         }.values(),
         key=sort_key )
