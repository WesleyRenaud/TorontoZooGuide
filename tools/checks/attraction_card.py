from __future__ import annotations

from dataclasses import dataclass
import re
from typing import ClassVar

from .website_page import WebsitePage


@dataclass( frozen=True )
class AttractionCard:
   CARD_RE: ClassVar[ re.Pattern[ str ] ] = re.compile(
      r'(?is)<a class="col3"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
   )
   HREF_RE: ClassVar[ re.Pattern[ str ] ] = re.compile( r'href="([^"]*)"' )
   href: str
   body: str


   @classmethod
   def href_from_tag( cls, tag: str ) -> str:
      match = cls.HREF_RE.search( tag )

      if match == None:
         return ''

      return match.group( 1 )


   @classmethod
   def from_openings( cls, page_html: str ) -> list[ AttractionCard ]:
      openings = WebsitePage.col3_openings( page_html )
      cards = []

      for index, opening in enumerate( openings ):
         end = len( page_html )

         if index + 1 < len( openings ):
            end = openings[ index + 1 ].start()

         cards.append( cls(
            href=cls.href_from_tag( opening.group( 0 ) ),
            body=page_html[ opening.end():end ],
         ) )

      return cards


   @classmethod
   def find( cls, page_html: str ) -> list[ AttractionCard ]:
      return [
         cls( href=href, body=body )
         for href, body in cls.CARD_RE.findall( page_html )
      ]
