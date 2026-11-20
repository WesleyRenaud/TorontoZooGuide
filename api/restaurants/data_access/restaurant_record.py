from __future__ import annotations

from dataclasses import dataclass, field

from ...shared.peak_months import PeakMonths
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
   peak_months: PeakMonths = field( default_factory=PeakMonths )
