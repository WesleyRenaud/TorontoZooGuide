from __future__ import annotations

from dataclasses import dataclass
import re
from typing import ClassVar

from .attraction_card import AttractionCard
from .website_page import WebsitePage


@dataclass
class GiftShopCard:
   TITLE_OPENING_RE: ClassVar[ re.Pattern[ str ] ] = re.compile( r'(?is)<strong>' )
   TITLE_CLOSING_RE: ClassVar[ re.Pattern[ str ] ] = re.compile( r'(?is)</strong>' )
   title: str
   status: str | None


   @classmethod
   def visible_page_html( cls, page_html: str ) -> str:
      return re.sub( r'(?is)<!--.*?-->', '', page_html )


   @classmethod
   def title_in( cls, body: str ) -> str:
      opening = cls.TITLE_OPENING_RE.search( body )
      closing = cls.TITLE_CLOSING_RE.search( body, opening.end() )
      return WebsitePage.clean_html( body[ opening.end():closing.start() ] )


   @classmethod
   def find( cls, page_html: str ) -> list[ GiftShopCard ]:
      page_html = cls.visible_page_html( page_html )

      return [
         cls(
            title=cls.title_in( card.body ),
            status=WebsitePage.opening_status( card.body ),
         )
         for card in AttractionCard.from_openings( page_html )
      ]
