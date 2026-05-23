from __future__ import annotations


class RegionWithExhibits:
   def __init__( self, name: str, exhibits: list[ str ] | None ) -> None:
      self.name = name
      self.exhibits = exhibits or []


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'exhibits': self.exhibits,
      }
