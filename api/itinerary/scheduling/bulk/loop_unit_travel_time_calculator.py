from __future__ import annotations

from .loop_schedule_stop import LoopScheduleStop
from .loop_schedule_unit import LoopScheduleUnit
from .loop_schedule_unit_builder import LoopScheduleUnitBuilder
from ...routing.walk_travel_time import travel_time_seconds_between_nodes
from ....walk_graph.domain.walk_graph import WalkGraph
from ....walk_graph.shortest_path import WalkGraphAdjacency


class LoopUnitTravelTimeCalculator():
   @classmethod
   def approach_seconds_to_unit(
         cls,
         walk_graph: WalkGraph,
         from_node_id: str,
         unit: LoopScheduleUnit,
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> int:
      entry_walk_node_id = unit.entry_walk_node_id

      if entry_walk_node_id is None or entry_walk_node_id == from_node_id:
         return 0

      return travel_time_seconds_between_nodes(
         walk_graph,
         from_node_id,
         entry_walk_node_id,
         adjacency=adjacency )


   @classmethod
   def inter_stop_seconds(
         cls,
         walk_graph: WalkGraph,
         stops: list[ LoopScheduleStop ],
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> list[ int ]:
      if not stops:
         return []

      # One travel entry per stop; the first is always 0 (approach is separate).
      travels = [ 0 ]
      previous_node_id = LoopScheduleUnitBuilder.walk_node_id_for_stop( stops[ 0 ] )

      for stop in stops[ 1: ]:
         next_node_id = LoopScheduleUnitBuilder.walk_node_id_for_stop( stop )

         if previous_node_id is None or next_node_id is None:
            travels.append( 0 )
         else:
            travels.append(
               travel_time_seconds_between_nodes(
                  walk_graph,
                  previous_node_id,
                  next_node_id,
                  adjacency=adjacency ) )

         previous_node_id = next_node_id

      return travels


   @classmethod
   def total_inter_stop_seconds(
         cls,
         walk_graph: WalkGraph,
         stops: list[ LoopScheduleStop ],
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> int:
      return sum(
         cls.inter_stop_seconds(
            walk_graph,
            stops,
            adjacency=adjacency ) )


   @classmethod
   def packed_units_occupied_seconds(
         cls,
         walk_graph: WalkGraph,
         prepared_units: list,
         *,
         from_node_id: str,
         adjacency: WalkGraphAdjacency | None = None ) -> int:
      total_seconds = 0
      current_node_id = from_node_id

      for prepared_unit in prepared_units:
         total_seconds += cls.approach_seconds_to_unit(
            walk_graph,
            current_node_id,
            prepared_unit.unit,
            adjacency=adjacency )
         total_seconds += prepared_unit.occupied_seconds

         if prepared_unit.unit.exit_walk_node_id is not None:
            current_node_id = prepared_unit.unit.exit_walk_node_id

      return total_seconds
