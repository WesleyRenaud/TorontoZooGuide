from __future__ import annotations


class Pavilion:
   def __init__(
         self,
         name: str,
         region: str,
         description: str | None = None,
         x_coord: float | None = None,
         y_coord: float | None = None ) -> None:
      self.name = name
      self.region = region
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'region': self.region,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
