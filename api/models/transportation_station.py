from __future__ import annotations

from ..shared.text_values import TextValues
from ..types import Types


class TransportationStation:
   def __init__(
         self,
         name: str,
         description: str,
         x_coord: Types.Coordinate,
         y_coord: Types.Coordinate ) -> None:
      self.name = name
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord


   def name_key( self ) -> str:
      return TextValues.normalize_for_matching( self.name )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
      }
