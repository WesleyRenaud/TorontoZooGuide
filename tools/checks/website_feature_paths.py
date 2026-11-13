from __future__ import annotations

import re

from .website_page import WebsitePage


class WebsiteFeaturePaths():
   SLIDE_RE = re.compile( r'(?is)<div class="mySlides\b[^>]*>.*?</div>' )
   CARD_RE = re.compile( r'(?is)<article class="card-slider-item">.*?</article>' )
   CUSTOM_RE = re.compile(
      r'(?is)<div class="[^"]*\bpgbut\b[^"]*\bcustom\b[^"]*"[^>]*>(?P<body>.*?)</div>'
   )
   HREF_RE = re.compile( r'(?is)href="([^"]+)"' )
   ZOO_RE = re.compile( r'(?i)^https?://(?:www\.)?torontozoo\.com/' )


   @classmethod
   def feature_paths( cls, home_html: str, animals_html: str ) -> list[ str ]:
      blocks = cls.SLIDE_RE.findall( home_html ) + cls.CARD_RE.findall( home_html )
      custom = cls.CUSTOM_RE.search( animals_html )

      if custom != None:
         blocks.append( custom.group( 'body' ) )

      paths = []
      seen: set[ str ] = set()

      for block in blocks:
         for href in cls.HREF_RE.findall( block ):
            path = cls.site_path( href )

            if path == None or path.casefold() in seen:
               continue

            seen.add( path.casefold() )
            paths.append( path )

      return paths


   @classmethod
   def site_path( cls, href: str ) -> str | None:
      text = WebsitePage.clean_website_name( href ).split( '#', 1 )[ 0 ].split( '?', 1 )[ 0 ].strip()
      zoo = cls.ZOO_RE.match( text )

      if '://' in text and zoo == None:
         return None

      if zoo != None:
         text = text[ zoo.end(): ]

      path = text.strip( '/' )

      if path == '' or path.casefold() == 'animals':
         return None

      return path
