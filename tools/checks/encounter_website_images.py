from __future__ import annotations

from .website_page import WebsitePage


class EncounterWebsiteImages():
   by_name: dict[ str, str ]


   def __init__( self ) -> None:
      self.by_name = {}


   def add( self, name: str, image: str ) -> None:
      self.by_name.setdefault( name, image )


   def for_name( self, name: str ) -> str:
      return self.by_name.get( WebsitePage.normalize_name( name ), '' )
