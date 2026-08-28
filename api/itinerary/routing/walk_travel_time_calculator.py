from __future__ import annotations

import math

from ...shared.duration_values import DurationValues
from ...shared.enums import ScheduleItemKind
from ...walk_graph.domain.walk_graph import WalkGraph
from ...walk_graph.shortest_path import ShortestPath
from ...walk_graph.shortest_path import WalkGraphAdjacency
from ...walk_graph.shortest_path_calculator import ShortestPathCalculator
from .walk_route_leg import WalkRouteLeg


class WalkTravelTimeCalculator():
   # Calibrated so entrance → Grizzly Bear (~4548 px) is ~31 minutes.
   WALK_PX_PER_MINUTE = 4548 / 31


   @classmethod
   def minutes_from_length_px( cls, length_px: float ) -> int:
      if length_px <= 0:
         return 0

      return math.floor( length_px / cls.WALK_PX_PER_MINUTE )


   @classmethod
   def seconds_from_length_px( cls, length_px: float ) -> int:
      return DurationValues.minutes_to_seconds(
         cls.minutes_from_length_px( length_px ) )


   @classmethod
   def seconds_between_nodes(
         cls,
         walk_graph: WalkGraph,
         from_node_id: str,
         to_node_id: str,
         *,
         adjacency: WalkGraphAdjacency | None = None ) -> int:
      path = ShortestPathCalculator.find(
         walk_graph,
         from_node_id,
         to_node_id,
         adjacency=adjacency )

      if path is None:
         return 0

      return cls.seconds_from_length_px( path.length_px )


   @classmethod
   def seconds_for_shortest_path( cls, path: ShortestPath | None ) -> int:
      if path is None:
         return 0

      return cls.seconds_from_length_px( path.length_px )


   @classmethod
   def route_leg_with_travel_time(
         cls,
         *,
         from_item_key: str,
         to_item_key: str,
         from_schedule_item_kind: ScheduleItemKind,
         to_schedule_item_kind: ScheduleItemKind,
         node_ids: list[ str ],
         length_px: float ) -> WalkRouteLeg:
      return WalkRouteLeg(
         from_item_key=from_item_key,
         to_item_key=to_item_key,
         from_schedule_item_kind=from_schedule_item_kind,
         to_schedule_item_kind=to_schedule_item_kind,
         node_ids=node_ids,
         travel_time_minutes=cls.minutes_from_length_px( length_px ) )

