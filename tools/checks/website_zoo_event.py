from __future__ import annotations

import calendar
from datetime import date
import re

from api.shared.calendar_dates import CalendarDates
from api.shared.enums.position import Position
from .date_span import DateSpan
from .website_feature_paths import WebsiteFeaturePaths
from .website_page import WebsitePage


class WebsiteZooEvent():
   CARD_RE = re.compile( r'(?is)<article class="card-slider-item">.*?</article>' )
   HREF_RE = re.compile( r'(?is)<a\b[^>]*href="([^"]*)"' )
   H2_RE = re.compile( r'(?is)<h2>(.*?)</h2>' )
   IMG_RE = re.compile( r'(?is)<img\b[^>]*\bsrc="([^"]*)"' )
   DATE_RE = re.compile( r'(?is)<p class="card-date">(.*?)</p>' )
   PARAGRAPH_RE = re.compile( r'(?is)<p(?![^>]*card-date)[^>]*>(.*?)</p>' )
   SENTENCE_RE = re.compile( r'[^.!?]*[.!?]' )
   DESCRIPTION_LIMIT = 160

   name: str
   description: str
   link: str
   image: str
   start: date | None
   end: date | None


   def __init__(
         self,
         name: str,
         description: str,
         link: str,
         image: str,
         start: date | None,
         end: date | None ) -> None:
      self.name = name
      self.description = description
      self.link = link
      self.image = image
      self.start = start
      self.end = end


   @classmethod
   def month_re( cls ) -> re.Pattern[ str ]:
      return re.compile( rf'(?i)\b(?P<month>{ "|".join( calendar.month_name[ 1: ] ) })\b' )


   @classmethod
   def range_re( cls ) -> re.Pattern[ str ]:
      months = '|'.join( calendar.month_name[ 1: ] )
      day = rf'(?:{ months })\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,?\s+20\d{{2}})?'
      return re.compile(
         rf'(?i)(?:from\s+)?(?P<a>{ day })\s*(?:to|through|–|—|-)\s*'
         rf'(?:[A-Za-z]+,\s*)?(?P<b>{ day })'
      )


   @classmethod
   def limited( cls, description: str ) -> str:
      if len( description ) <= cls.DESCRIPTION_LIMIT:
         return description

      sentences = cls.SENTENCE_RE.findall( description )

      if len( sentences ) == 0:
         return description

      kept = sentences[ 0 ]

      for sentence in sentences[ 1: ]:
         if len( kept + sentence ) > cls.DESCRIPTION_LIMIT:
            break

         kept += sentence

      return kept.rstrip()


   @classmethod
   def plain( cls, html: str ) -> str:
      without = re.sub( r'(?is)<(script|style)\b.*?</\1>', ' ', html )
      return WebsitePage.clean_html( without )


   @classmethod
   def dates_in( cls, text: str, today: date ) -> list[ date ]:
      found = []
      matches = list( cls.month_re().finditer( text ) )

      for index, match in enumerate( matches ):
         month = CalendarDates.month_index( match.group( 'month' ) )

         if month == None:
            continue

         rest_end = matches[ index + 1 ].start() if index + 1 < len( matches ) else len( text )
         rest = text[ match.end():rest_end ]
         year_match = re.search( r'\b(20\d{2})\b', rest )
         year = today.year if year_match == None else int( year_match.group( 1 ) )

         for day_text in re.findall( r'\b(\d{1,2})\b', rest ):
            day = int( day_text )

            try:
               found.append( date( year, month, day ) )
            except ValueError:
               continue

      return found


   @classmethod
   def span( cls, dates: list[ date ] ) -> DateSpan:
      start = dates[ Position.FIRST ]
      end = dates[ Position.LAST ]

      if end < start:
         end = date( end.year + 1, end.month, end.day )

      return DateSpan( start=start, end=end )


   @classmethod
   def pair( cls, start_text: str, end_text: str, today: date ) -> DateSpan | None:
      starts = cls.dates_in( start_text, today )
      ends = cls.dates_in( end_text, today )

      if len( starts ) == 0 or len( ends ) == 0:
         return None

      return cls.span( [ starts[ Position.FIRST ], ends[ Position.LAST ] ] )


   @classmethod
   def choose_range( cls, text: str, today: date ) -> DateSpan | None:
      ranges = []

      for match in cls.range_re().finditer( text ):
         found = cls.pair( match.group( 'a' ), match.group( 'b' ), today )

         if found != None:
            ranges.append( found )

      covering = [
         found
         for found in ranges
         if found.start <= today <= found.end
      ]
      dates = cls.dates_in( text, today )
      loose = [] if len( dates ) == 0 else [ cls.span( dates ) ]
      chosen = covering or ranges or loose
      return None if len( chosen ) == 0 else chosen[ Position.FIRST ]


   @classmethod
   def window(
         cls,
         title: str,
         card_date: str,
         page: str,
         today: date ) -> DateSpan | None:
      title_dates = cls.dates_in( title, today )
      card_dates = cls.dates_in( card_date, today )
      title_span = None if len( title_dates ) < 2 else cls.span( title_dates )
      card_span = None if len( card_dates ) == 0 else cls.span( card_dates )
      single_title = None if len( title_dates ) != 1 else cls.span( title_dates )
      return title_span or card_span or cls.choose_range( page, today ) or single_title


   @classmethod
   def page_text( cls, link: str, pages: dict[ str, str ] | None ) -> str:
      url = link.split( '#', 1 )[ Position.FIRST ]

      if pages != None:
         return pages.get( url, '' )

      return cls.plain( WebsitePage.fetch_text( url ) )


   @classmethod
   def from_card(
         cls,
         card: str,
         today: date,
         pages: dict[ str, str ] | None ) -> WebsiteZooEvent | None:
      hrefs = cls.HREF_RE.findall( card )
      heading = cls.H2_RE.search( card )

      if len( hrefs ) == 0 or heading == None:
         return None

      path = WebsiteFeaturePaths.site_path( hrefs[ Position.FIRST ] )

      if path == None or path.casefold() == 'events':
         return None

      name = WebsitePage.clean_html( heading.group( 1 ) )
      date_html = cls.DATE_RE.search( card )
      card_date = '' if date_html == None else cls.plain( date_html.group( 1 ) )
      description = ' '.join(
         WebsitePage.clean_html( piece )
         for piece in cls.PARAGRAPH_RE.findall( card )
      )
      images = cls.IMG_RE.findall( card )
      image = '' if len( images ) == 0 else WebsitePage.absolute_url( images[ Position.FIRST ] )
      link = WebsitePage.absolute_url( hrefs[ Position.FIRST ] )
      page = ''
      found = cls.window( name, card_date, '', today )

      if found == None:
         page = cls.page_text( link, pages )
         found = cls.window( name, card_date, page, today )

      start = None if found == None else found.start
      end = None if found == None else found.end
      return cls( name, description, link, image, start, end )


   @classmethod
   def read(
         cls,
         home_html: str,
         today: date,
         pages: dict[ str, str ] | None = None ) -> list[ WebsiteZooEvent ]:
      events_at = home_html.find( 'id="events"' )
      section = home_html if events_at < 0 else home_html[ events_at: ]
      events = []

      for card in cls.CARD_RE.findall( section ):
         event = cls.from_card( card, today, pages )

         if event != None:
            events.append( event )

      return events
