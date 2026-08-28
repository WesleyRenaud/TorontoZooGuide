from __future__ import annotations

from ..types import Types


class TransportationRouteMarker:
   def __init__( self, route_type: str, x_coord: Types.Coordinate, y_coord: Types.Coordinate ) -> None:
      self.route_type = route_type
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'route_type': self.route_type,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
