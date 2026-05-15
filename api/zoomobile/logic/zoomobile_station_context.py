from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class ZoomobileStationContext:
   route: object
   target_date: date
   zoomobile_stations_to_include: list
