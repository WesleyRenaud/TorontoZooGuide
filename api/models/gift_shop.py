from __future__ import annotations

from ..shared.text_values import TextValues
from ..shared.value_conversion import ValueConversion


class GiftShop:
   name: str
   location: str
   description: str | None
   x_coord: float | None
   y_coord: float | None
   is_closed: bool | None
   closed_message: str | None
   likelihood: int | None
   is_closed_for_season: bool


   def __init__(
         self,
         name: str,
         location: str,
         description: str | None = None,
         x_coord: float | None = None,
         y_coord: float | None = None,
         is_closed: bool | None = None,
         closed_message: str | None = None,
         likelihood: int | None = None,
         is_closed_for_season: bool = False ) -> None:
      self.name = name
      self.location = location
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.likelihood = likelihood
      self.is_closed_for_season = is_closed_for_season


   def name_key( self ) -> str:
      return TextValues.normalize_for_matching( self.name )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'location': self.location,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ValueConversion.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'likelihood': self.likelihood,
         'is_closed_for_season': ValueConversion.as_boolean( self.is_closed_for_season ),
      }
