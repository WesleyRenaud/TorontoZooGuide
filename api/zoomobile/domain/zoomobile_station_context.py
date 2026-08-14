from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class ZoomobileStationContext:
   route: str
   stations_on_route: list[ str ]
   target_date: date
   zoomobile_stations_to_include: list[ str ]
