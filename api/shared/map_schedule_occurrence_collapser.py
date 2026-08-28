from __future__ import annotations

from collections.abc import Callable, Hashable
from typing import Any, TypeVar

from .calendar_dates import DateValues
from .map_schedule_time_sorter import MapScheduleTimeSorter
from ..types import Types


T = TypeVar( 'T' )


class MapScheduleOccurrenceCollapser():
   @classmethod
   def collapse(
         cls,
         items: list[ T ],
         *,
         group_key: Callable[ [ T ], Hashable ],
         get_start_time: Callable[ [ T ], Types.ScheduleTimeKey ] ) -> list[ dict[ str, Any ] ]:
      if not items:
         return []

      grouped_items: dict[ Hashable, list[ T ] ] = {}

      for item in items:
         grouped_items.setdefault( group_key( item ), [] ).append( item )

      collapsed_items: list[ dict[ str, Any ] ] = []

      for group in grouped_items.values():
         times = MapScheduleTimeSorter.unique_sorted(
            get_start_time( item )
            for item in group )

         def occurrence_sort_key( item: T ) -> float:
            time_seconds = DateValues.time_value_in_seconds( get_start_time( item ) )
            return float( time_seconds ) if time_seconds is not None else float( 'inf' )

         earliest_item = min( group, key=occurrence_sort_key )
         payload = earliest_item.to_dict()
         payload[ 'times' ] = times

         if len( times ) > 1:
            payload[ 'end_time' ] = None

         collapsed_items.append( payload )

      return collapsed_items
