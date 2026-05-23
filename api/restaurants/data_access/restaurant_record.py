from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate, SeasonalMultiplier


@dataclass( frozen=True )
class RestaurantRecord:
   name: str
   location: str
   sub_location: str | None
   description: str
   menu_link: str | None
   x_coord: Coordinate
   y_coord: Coordinate
   weekday_multiplier: SeasonalMultiplier
   weekend_holiday_multiplier: SeasonalMultiplier
