from __future__ import annotations

from ..types import Types


class GuestService:
   def __init__( self, service_type: str, x_coord: Types.Coordinate, y_coord: Types.Coordinate ) -> None:
      self.service_type = service_type
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'service_type': self.service_type,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
