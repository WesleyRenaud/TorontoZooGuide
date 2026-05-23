from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from ...shared.enums.zoomobile_route import ZoomobileRouteId


@dataclass( frozen=True )
class ZoomobileStationContext:
   route: ZoomobileRouteId
   target_date: date
   zoomobile_stations_to_include: list[ str ]
