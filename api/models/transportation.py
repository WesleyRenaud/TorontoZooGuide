from __future__ import annotations

from ..shared.value_conversion import ValueConversion
from ..types import Coordinate


class Transportation:
   def __init__(
         self,
         name: str,
         *,
         is_also_attraction: bool = False,
         free_with_admission: bool = False,
         description: str | None = None,
         info_link: str | None = None,
         hyperlink_text: str | None = None,
         x_coord: Coordinate | None = None,
         y_coord: Coordinate | None = None,
         region: str | None = None ) -> None:
      self.name = name
      self.is_also_attraction = is_also_attraction
      self.free_with_admission = free_with_admission
      self.description = description
      self.info_link = info_link
      self.hyperlink_text = hyperlink_text
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.region = region


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'is_also_attraction': ValueConversion.as_boolean(
            self.is_also_attraction ),
         'free_with_admission': ValueConversion.as_boolean(
            self.free_with_admission ),
         'description': self.description,
         'info_link': self.info_link,
         'hyperlink_text': self.hyperlink_text,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'region': self.region,
      }
