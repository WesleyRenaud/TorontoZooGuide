from dataclasses import dataclass


@dataclass( frozen=True )
class ZoomobileStationStatusRecord:
   zoomobile_station: object
   closed_start: object
   closed_end: object
   is_closed: object
   closed_message: object
