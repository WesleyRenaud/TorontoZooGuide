from __future__ import annotations

from ..types import Coordinate


class EmergencyIntercom:
   def __init__( self, x_coord: Coordinate, y_coord: Coordinate ) -> None:
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
