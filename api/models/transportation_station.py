from __future__ import annotations

from ..shared.name_matching_query import normalize_search_key
from ..types import Coordinate


class TransportationStation:
   def __init__(
         self,
         name: str,
         description: str,
         x_coord: Coordinate,
         y_coord: Coordinate ) -> None:
      self.name = name
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord


   def name_key( self ) -> str:
      return normalize_search_key( self.name )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
      }
