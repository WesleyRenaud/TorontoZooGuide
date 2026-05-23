from __future__ import annotations

from ..shared.value_conversion import ValueConversion
from ..types import Coordinate


class DrinkingFountain:
   def __init__(
         self,
         x_coord: Coordinate,
         y_coord: Coordinate,
         is_closed: bool = False,
         closed_message: str | None = None,
         likelihood: int | None = None ) -> None:
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = ValueConversion.as_boolean( is_closed )
      self.closed_message = closed_message
      self.likelihood = likelihood


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': self.is_closed,
         'closed_message': self.closed_message,
         'likelihood': self.likelihood
      }
