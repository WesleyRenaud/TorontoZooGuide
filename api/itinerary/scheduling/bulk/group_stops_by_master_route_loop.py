from __future__ import annotations

from .loop_schedule_stop import loop_schedule_stop_key
from .loop_schedule_stop import LoopScheduleStop
from .sort_stops_by_master_route import sort_stops_by_master_route
from ....walk_graph.master_route import default_loop_index_by_stop_key


def group_stops_by_master_route_loop(
      stops: list[ LoopScheduleStop ] ) -> list[ list[ LoopScheduleStop ] ]:
   sorted_stops = sort_stops_by_master_route( stops )

   if not sorted_stops:
      return []

   loop_indexes = default_loop_index_by_stop_key()
   groups: list[ list[ LoopScheduleStop ] ] = []
   current_loop_index: int | None = None
   current_group: list[ LoopScheduleStop ] = []

   for stop in sorted_stops:
      loop_index = loop_indexes.get( loop_schedule_stop_key( stop ) )

      if loop_index is None:
         if current_group:
            groups.append( current_group )
            current_group = []
            current_loop_index = None

         groups.append( [ stop ] )
         continue

      if loop_index != current_loop_index:
         if current_group:
            groups.append( current_group )

         current_group = [ stop ]
         current_loop_index = loop_index
         continue

      current_group.append( stop )

   if current_group:
      groups.append( current_group )

   return groups
