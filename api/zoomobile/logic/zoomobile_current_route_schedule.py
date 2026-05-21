from dataclasses import dataclass

from ...shared.enums.zoomobile_route import ZoomobileRouteId


@dataclass( frozen=True )
class ZoomobileCurrentRouteSchedule:
   route: ZoomobileRouteId
   start_date: str
   end_date: object
