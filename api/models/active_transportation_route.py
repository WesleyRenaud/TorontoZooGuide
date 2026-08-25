from __future__ import annotations

from dataclasses import dataclass

from .transportation_station import TransportationStation


@dataclass( frozen=True )
class ActiveTransportationRoute:
   route: str
   route_source: str
   transportation_stations: list[ TransportationStation ]


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'route': self.route,
         'route_source': self.route_source,
         'transportation_stations': [
            station.to_dict() for station in self.transportation_stations
         ],
      }
