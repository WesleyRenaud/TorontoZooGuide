from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate, SeasonalMultiplier


@dataclass( frozen=True )
class GiftShopRecord:
   name: str
   location: str
   description: str
   x_coord: Coordinate
   y_coord: Coordinate
   weekday_multiplier: SeasonalMultiplier
   weekend_holiday_multiplier: SeasonalMultiplier
