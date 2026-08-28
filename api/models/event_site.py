from __future__ import annotations

from ..types import Types


class EventSite:
   def __init__( self, name: str, x_coord: Types.Coordinate, y_coord: Types.Coordinate ) -> None:
      self.name = name
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
