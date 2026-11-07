from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .website_page import WebsitePage


@dataclass( frozen=True )
class GiftShopListing:
   name: str


   def __eq__( self, other: Any ) -> bool:
      if not isinstance( other, type( self ) ):
         return NotImplemented

      return WebsitePage.normalize_name( self.name ) == WebsitePage.normalize_name( other.name )


   def __hash__( self ) -> int:
      return hash( WebsitePage.normalize_name( self.name ) )
