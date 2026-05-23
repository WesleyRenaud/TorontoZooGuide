from __future__ import annotations

from dataclasses import dataclass

from ...types import Coordinate, SeasonalMultiplier


@dataclass( frozen=True )
class AttractionRecord:
   name: str
   free_with_admission: bool
   description: str
   info_link: str
   hyperlink_text: str
   x_coord: Coordinate
   y_coord: Coordinate
   weekday_multiplier: SeasonalMultiplier
   weekend_holiday_multiplier: SeasonalMultiplier
