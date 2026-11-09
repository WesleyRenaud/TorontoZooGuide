from __future__ import annotations

import re

from .attraction_card import AttractionCard
from .encounter_website_images import EncounterWebsiteImages
from .website_page import WebsitePage


class EncounterWebsiteCard():
   IMAGE_RE = re.compile( r'(?is)<img\b[^>]*\bsrc="(?P<src>[^"]+)"' )


   @classmethod
   def image( cls, body: str ) -> str:
      match = cls.IMAGE_RE.search( body )

      if match == None:
         return ''

      return WebsitePage.absolute_url( match.group( 'src' ) )


   @classmethod
   def images( cls, page_html: str ) -> EncounterWebsiteImages:
      images = EncounterWebsiteImages()

      for card in AttractionCard.find( page_html ):
         title = WebsitePage.COL3_TITLE_RE.search( card.body )

         if title == None:
            continue

         image = cls.image( card.body )

         if image == '':
            continue

         images.add(
            WebsitePage.normalize_name( WebsitePage.clean_html( title.group( 'title' ) ) ),
            image,
         )

      return images
