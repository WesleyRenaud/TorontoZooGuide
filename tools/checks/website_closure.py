from __future__ import annotations

import re

from api.app_string_provider import AppStringProvider
from .website_page import WebsitePage


class WebsiteClosure():
   NOTICES_HEADING_RE = re.compile( r'(?is)<h2[^>]*id="notices"[^>]*>.*?</h2>' )
   ANIMALS_HEADING_RE = re.compile( r'(?is)<h2[^>]*id="animals' )
   BOX_RE = re.compile(
      r'(?is)<div class="box[^"]*"[^>]*>.*?(?=<div class="box|\Z)',
   )
   STRONG_RE = re.compile( r'(?is)<strong>(.*?)</strong>' )
   SUMMARY_END_RE = re.compile( r'(?is)</summary>' )
   SEASON_RE = re.compile( r'for the (?:winter )?season' )
   CLOSURE_RE = re.compile( r'\b(?:close|closed|closing|closure)\b' )
   title: str
   description: str


   def __init__( self, title: str, description: str ) -> None:
      self.title = title
      self.description = description


   @classmethod
   def notices_section( cls, page_html: str ) -> str:
      heading = cls.NOTICES_HEADING_RE.search( page_html )
      following = None

      if heading != None:
         following = cls.ANIMALS_HEADING_RE.search( page_html, heading.end() )

      if heading == None or following == None:
         raise RuntimeError(
            AppStringProvider.format( 'checks.couldNotReadAlertsPage' )
         )

      return page_html[ heading.end():following.start() ]


   @classmethod
   def description( cls, box: str, title: str ) -> str:
      summary_end = cls.SUMMARY_END_RE.search( box )

      if summary_end != None:
         return WebsitePage.clean_html( box[ summary_end.end(): ] )

      text = WebsitePage.clean_html( box )

      if text.startswith( title ):
         return text[ len( title ): ].strip()

      return text


   @classmethod
   def notice( cls, box: str ) -> WebsiteClosure | None:
      strong = cls.STRONG_RE.search( box )

      if strong == None:
         return None

      title = WebsitePage.clean_html( strong.group( 1 ) )

      if title == '':
         return None

      return cls( title, cls.description( box, title ) )


   @classmethod
   def notices( cls, page_html: str ) -> list[ WebsiteClosure ]:
      notices = []

      for box in cls.BOX_RE.findall( cls.notices_section( page_html ) ):
         notice = cls.notice( box )

         if notice == None:
            continue

         notices.append( notice )

      return notices


   @classmethod
   def is_closure( cls, title: str, description: str ) -> bool:
      text = f'{ title } { description }'.casefold()

      if cls.SEASON_RE.search( text ) != None:
         return False

      return cls.CLOSURE_RE.search( text ) != None


   @classmethod
   def closures( cls, page_html: str ) -> list[ WebsiteClosure ]:
      return [
         notice
         for notice in cls.notices( page_html )
         if cls.is_closure( notice.title, notice.description )
      ]
