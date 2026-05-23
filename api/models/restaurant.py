from __future__ import annotations

from ..shared.value_conversion import ValueConversion


class Restaurant:
   def __init__(
         self,
         name: str,
         location: str,
         sub_location: str,
         description: str | None = None,
         menu_link: str | None = None,
         x_coord: float | None = None,
         y_coord: float | None = None,
         is_closed: bool | None = None,
         closed_message: str | None = None,
         likelihood: int | None = None ) -> None:
      self.name = name
      self.location = location
      self.sub_location = sub_location
      self.description = description
      self.menu_link = menu_link
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.likelihood = likelihood


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'location': self.location,
         'sub_location': self.sub_location,
         'description': self.description,
         'menu_link': self.menu_link,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ValueConversion.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'likelihood': self.likelihood
      }
