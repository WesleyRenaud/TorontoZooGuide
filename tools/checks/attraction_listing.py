from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .website_page import WebsitePage


@dataclass( frozen=True )
class AttractionListing:
   WEBSITE_ONLY_NAMES = {
      'Kids Zoo',
      "Nature's Night Shift",
      'Serengeti Bush Camp',
   }
   name: str
   link: str = ''


   @classmethod
   def website_only( cls ) -> set[ AttractionListing ]:
      return {
         cls( name=name )
         for name in cls.WEBSITE_ONLY_NAMES
      }


   def is_website_only( self ) -> bool:
      return self in AttractionListing.website_only()


   def matches( self, other: AttractionListing ) -> bool:
      if WebsitePage.normalize_name( self.name ) == WebsitePage.normalize_name( other.name ):
         return True

      path = WebsitePage.normalize_path( self.link )
      return path != '' and path == WebsitePage.normalize_path( other.link )


   def __eq__( self, other: Any ) -> bool:
      if not isinstance( other, type( self ) ):
         return NotImplemented

      return WebsitePage.normalize_name( self.name ) == WebsitePage.normalize_name( other.name )


   def __hash__( self ) -> int:
      return hash( WebsitePage.normalize_name( self.name ) )
