from dataclasses import dataclass
from typing import Any
from typing import Tuple


@dataclass( frozen=True )
class ZoomobileRoute:
   route: str
   route_source: str
   zoomobile_stations: Tuple[ Any, ... ]


   def to_dict( self ):
      return {
         'route': self.route,
         'route_source': self.route_source,
         'zoomobile_stations': [
            station.to_dict() for station in self.zoomobile_stations
         ],
      }
