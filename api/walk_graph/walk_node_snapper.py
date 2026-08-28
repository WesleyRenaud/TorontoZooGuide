from __future__ import annotations

import math

from .domain.walk_graph import WalkGraph
from .map_coordinate_converter import MapCoordinateConverter


class WalkNodeSnapper():
   @classmethod
   def snap(
         cls,
         x_percent: float,
         y_percent: float,
         graph: WalkGraph ) -> tuple[ str, float ]:
      x_px, y_px = MapCoordinateConverter.percent_to_px(
         x_percent,
         y_percent,
         map_width_px=graph[ 'map_width_px' ],
         map_height_px=graph[ 'map_height_px' ] )

      nearest_node = min(
         graph[ 'nodes' ],
         key=lambda node: math.hypot(
            node[ 'x_px' ] - x_px,
            node[ 'y_px' ] - y_px ) )

      snap_distance_px = math.hypot(
         nearest_node[ 'x_px' ] - x_px,
         nearest_node[ 'y_px' ] - y_px )

      return nearest_node[ 'id' ], snap_distance_px


   @classmethod
   def distance(
         cls,
         x_percent: float,
         y_percent: float,
         walk_node_id: str,
         graph: WalkGraph ) -> float:
      x_px, y_px = MapCoordinateConverter.percent_to_px(
         x_percent,
         y_percent,
         map_width_px=graph[ 'map_width_px' ],
         map_height_px=graph[ 'map_height_px' ] )
      walk_node = next(
         node for node in graph[ 'nodes' ] if node[ 'id' ] == walk_node_id )

      return math.hypot(
         walk_node[ 'x_px' ] - x_px,
         walk_node[ 'y_px' ] - y_px )
