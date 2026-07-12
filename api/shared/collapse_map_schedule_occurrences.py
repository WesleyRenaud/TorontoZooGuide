from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable
from typing import Any, Protocol, TypeVar

from .calendar_dates import DateValues
from ..types import ScheduleTimeKey


class _MapScheduleOccurrence( Protocol ):
   def to_dict( self ) -> dict[ str, Any ]:
      ...


T = TypeVar( 'T', bound=_MapScheduleOccurrence )


def unique_sorted_schedule_times(
      times: Iterable[ ScheduleTimeKey ] ) -> list[ str ]:
   unique_times: dict[ int, str ] = {}

   for time_value in times:
      normalized_time = DateValues.normalize_schedule_time( time_value )

      if not normalized_time:
         continue

      time_seconds = DateValues.time_value_in_seconds( normalized_time )

      if time_seconds is None:
         continue

      unique_times.setdefault( time_seconds, normalized_time )

   return [
      unique_times[ time_seconds ]
      for time_seconds in sorted( unique_times )
   ]


def collapse_map_schedule_occurrences(
      items: list[ T ],
      *,
      group_key: Callable[ [ T ], Hashable ],
      get_start_time: Callable[ [ T ], ScheduleTimeKey ] ) -> list[ dict[ str, Any ] ]:
   if not items:
      return []

   grouped_items: dict[ Hashable, list[ T ] ] = {}

   for item in items:
      grouped_items.setdefault( group_key( item ), [] ).append( item )

   collapsed_items: list[ dict[ str, Any ] ] = []

   for group in grouped_items.values():
      times = unique_sorted_schedule_times(
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
