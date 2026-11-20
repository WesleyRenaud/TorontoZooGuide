from __future__ import annotations

from dataclasses import dataclass, field

from ...shared.peak_months import PeakMonths
from ...types import Types


@dataclass( frozen=True )
class GiftShopRecord:
   name: str
   location: str
   description: str
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   peak_months: PeakMonths = field( default_factory=PeakMonths )
