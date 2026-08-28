from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class RestaurantRecord:
   name: str
   location: str
   sub_location: str | None
   description: str
   menu_link: str | None
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   weekday_multiplier: Types.SeasonalMultiplier
   weekend_holiday_multiplier: Types.SeasonalMultiplier
