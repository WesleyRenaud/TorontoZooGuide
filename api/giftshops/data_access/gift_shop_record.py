from __future__ import annotations

from dataclasses import dataclass

from ...types import Types


@dataclass( frozen=True )
class GiftShopRecord:
   name: str
   location: str
   description: str
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   weekday_multiplier: Types.SeasonalMultiplier
   weekend_holiday_multiplier: Types.SeasonalMultiplier
