from __future__ import annotations

from ..shared.value_conversion import ValueConversion
from ..types import Types


class DrinkingFountain:
   x_coord: Types.Coordinate
   y_coord: Types.Coordinate
   is_closed: bool
   closed_message: str | None
   likelihood: int | None
   is_closed_for_season: bool


   def __init__(
         self,
         x_coord: Types.Coordinate,
         y_coord: Types.Coordinate,
         is_closed: bool = False,
         closed_message: str | None = None,
         likelihood: int | None = None,
         is_closed_for_season: bool = False ) -> None:
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = ValueConversion.as_boolean( is_closed )
      self.closed_message = closed_message
      self.likelihood = likelihood
      self.is_closed_for_season = ValueConversion.as_boolean( is_closed_for_season )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': self.is_closed,
         'closed_message': self.closed_message,
         'likelihood': self.likelihood,
         'is_closed_for_season': ValueConversion.as_boolean( self.is_closed_for_season ),
      }
