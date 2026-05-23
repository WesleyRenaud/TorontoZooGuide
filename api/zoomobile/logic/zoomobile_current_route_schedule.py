from __future__ import annotations

from dataclasses import dataclass

from ...shared.enums.zoomobile_route import ZoomobileRouteId
from ...types import DateKey


@dataclass( frozen=True )
class ZoomobileCurrentRouteSchedule:
   route: ZoomobileRouteId
   start_date: str
   end_date: DateKey | None
