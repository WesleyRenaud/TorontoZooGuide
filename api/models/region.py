from __future__ import annotations


class Region:
   name: str
   has_exhibits: bool


   def __init__( self, name: str, has_exhibits: bool ) -> None:
      self.name = name
      self.has_exhibits = has_exhibits


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'hasExhibits': self.has_exhibits,
      }
