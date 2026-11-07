from __future__ import annotations

from datetime import date
from html import unescape
import re
import subprocess
from urllib.parse import unquote

from api.app_string_provider import AppStringProvider
from .constants import Constants
from .date_patterns import DatePatterns


class WebsitePage():
   BASE_URL = 'https://www.torontozoo.com'
   USER_AGENT = 'Mozilla/5.0'
   ALERTS = 'alerts'
   ATTRACTIONS = 'attractions'
   GIFT_SHOPS = 'tz/giftshops'
   RESTAURANTS = 'tz/restaurants'
   COL3_TITLE_RE = re.compile( r'(?is)<div class="col3title">(.*?)</div>' )
   COL3_OPENING_RE = re.compile( r'(?is)<(a|div) class="col3"[^>]*>' )
   OPENING_STATUS_RE = re.compile( r'(?is)<span class="opentxt">(?P<status>.*?)</span>' )


   @classmethod
   def url( cls, page: str ) -> str:
      return f'{ cls.BASE_URL }/{ page }'


   @classmethod
   def fetch_text( cls, url: str ) -> str:
      result = subprocess.run(
         [ 'curl', '-fsS', '--max-time', '30', '-A', cls.USER_AGENT, url ],
         check=False,
         capture_output=True,
      )

      if result.returncode != 0:
         detail = result.stderr.decode( errors='replace' ).strip()
         raise RuntimeError( detail or AppStringProvider.format(
            'checks.curlExited',
            returncode=result.returncode,
         ) )

      return result.stdout.decode()


   @classmethod
   def clean_html( cls, value: str ) -> str:
      text = re.sub( r'(?is)<[^>]+>', ' ', value )
      return re.sub( r'\s+', ' ', unescape( text ) ).strip()


   @classmethod
   def is_closed_for_season_status( cls, status: str | None, today: date ) -> bool:
      if status == None:
         return False

      cleaned = cls.clean_html( status ).casefold()

      if AppStringProvider.format( 'checks.closedForSeason' ) in cleaned:
         return True

      ended = DatePatterns.through_date( cleaned, today )
      return ended != None and ended < today


   @classmethod
   def opening_status( cls, body: str ) -> str | None:
      status_match = cls.OPENING_STATUS_RE.search( body )

      if status_match == None:
         return None

      return status_match.group( 'status' )


   @classmethod
   def is_seasonally_closed( cls, body: str, today: date ) -> bool:
      return cls.is_closed_for_season_status( cls.opening_status( body ), today )


   @classmethod
   def col3_openings( cls, page_html: str ) -> list[ re.Match[ str ] ]:
      return list( cls.COL3_OPENING_RE.finditer( page_html ) )


   @classmethod
   def col3_title( cls, html: str ) -> str:
      match = cls.COL3_TITLE_RE.search( html )
      return cls.clean_html( match.group( 1 ) )


   @classmethod
   def clean_website_name( cls, href: str ) -> str:
      return unescape( unquote( href ) ).replace( '+', ' ' ).strip()


   @classmethod
   def normalize_name( cls, name: str ) -> str:
      text = (
         name
         .replace( '\u2018', "'" )
         .replace( '\u2019', "'" )
         .replace( '\u201b', "'" )
      )
      text = re.sub( r'\s*\([^)]*\)', '', text )
      text = re.sub( f'[{ Constants.DASHES }]', ' ', text )
      text = text.casefold()
      return re.sub( r'\s+', ' ', text ).strip()


   @classmethod
   def normalize_path( cls, url: str ) -> str:
      trimmed = url.split( '?', 1 )[ 0 ].strip()

      if '://' in trimmed:
         trimmed = trimmed.split( '://', 1 )[ 1 ]
         trimmed = trimmed.split( '/', 1 )[ 1 ] if '/' in trimmed else ''

      return trimmed.strip( '/' ).casefold()
