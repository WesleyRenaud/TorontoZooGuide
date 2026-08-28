from __future__ import annotations


class MapCoordinateConverter():
   @classmethod
   def percent_to_px(
         cls,
         x_percent: float,
         y_percent: float,
         *,
         map_width_px: int,
         map_height_px: int ) -> tuple[ float, float ]:
      return (
         x_percent / 100 * map_width_px,
         y_percent / 100 * map_height_px,
      )
