from dataclasses import dataclass


@dataclass( frozen=True )
class ZoomobileStationClosedStatus:
   zoomobile_station: str
   start_date: str
   end_date: object
   message: str
