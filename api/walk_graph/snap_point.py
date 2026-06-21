from __future__ import annotations

import math

from .domain.walk_graph import WalkGraph


def percent_to_map_px(
      x_percent: float,
      y_percent: float,
      *,
      map_width_px: int,
      map_height_px: int ) -> tuple[ float, float ]:
   return (
      x_percent / 100 * map_width_px,
      y_percent / 100 * map_height_px,
   )


def snap_point_to_nearest_walk_node(
      x_percent: float,
      y_percent: float,
      graph: WalkGraph ) -> tuple[ str, float ]:
   x_px, y_px = percent_to_map_px(
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
