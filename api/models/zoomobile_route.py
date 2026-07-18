from __future__ import annotations

from dataclasses import dataclass

from .zoomobile_station import ZoomobileStation


@dataclass( frozen=True )
class ZoomobileRoute:
   route: str
   route_source: str
   zoomobile_stations: list[ ZoomobileStation ]


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'route': self.route,
         'route_source': self.route_source,
         'zoomobile_stations': [
            station.to_dict() for station in self.zoomobile_stations
         ],
      }
