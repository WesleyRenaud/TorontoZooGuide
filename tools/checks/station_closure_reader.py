from __future__ import annotations

from datetime import date
import re

from api.shared.calendar_dates import CalendarDates
from api.shared.text_values import TextValues
from .date_span import DateSpan
from .station_closure import StationClosure
from .viewing_alert_sentence_builder import ViewingAlertSentenceBuilder
from .website_closure import WebsiteClosure


class StationClosureReader():
   PLACES = (
      ( 'Canadian Domain Zoomobile Station', ( 'canadian domain zoomobile', ) ),
      ( 'Indo-Malaya Zoomobile Station', ( 'indo-malaya zoomobile', 'indomalaya zoomobile' ) ),
      ( 'Tundra Zoomobile Station', ( 'tundra zoomobile', ) ),
      ( 'Eurasia Zoomobile Station', ( 'eurasia zoomobile', ) ),
      ( 'Africa Zoomobile Station', ( 'african zoomobile', 'africa zoomobile' ) ),
      ( 'Main Zoomobile Station', ( 'zoomobile main station', 'main zoomobile station' ) ),
   )
   SKIP_RE = re.compile(
      r'wheelchair|relocat|remain open|now open|\bis open\b|\bare open\b',
      re.I,
   )
   CLOSED_RE = re.compile( r'\b(?:close|closed|closing|closure)\b', re.I )
   WEEKDAY = r'(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday),?\s+'
   MONTH = (
      r'(?:january|february|march|april|may|june|july|august|september|'
      r'october|november|december)'
   )
   DAY = r'\d{1,2}(?:st|nd|rd|th)?'
   DATE_RE = re.compile(
      rf'(?i)(?:{ WEEKDAY })?(?P<month>{ MONTH })\s+(?P<day>{ DAY })'
      rf'(?:\s*,?\s*(?P<year>\d{{4}}))?'
      rf'(?:\s*(?:–|-|—|through|to)\s+'
      rf'(?:{ WEEKDAY })?(?P<end_month>{ MONTH })\s+(?P<end_day>{ DAY })'
      rf'(?:\s*,?\s*(?P<end_year>\d{{4}}))?)?'
   )


   @classmethod
   def text( cls, notice: WebsiteClosure ) -> str:
      title = notice.title.strip()

      if title != '' and title[ -1 ] not in '.!?':
         title = f'{ title }.'

      return TextValues.beside( title, notice.description )


   @classmethod
   def closure( cls, sentence: str ) -> bool:
      folded = sentence.casefold()
      return cls.SKIP_RE.search( folded ) == None and cls.CLOSED_RE.search( folded ) != None


   @classmethod
   def places( cls, sentence: str ) -> list[ str ]:
      folded = sentence.casefold()
      found = []

      for title, phrases in cls.PLACES:
         phrase = next( ( candidate for candidate in phrases if candidate in folded ), None )

         if phrase == None:
            continue

         found.append( title )
         folded = folded.replace( phrase, ' ', 1 )

      return found


   @classmethod
   def on_day(
         cls,
         month_name: str,
         day_text: str,
         year_text: str | None,
         today: date ) -> date | None:
      month = CalendarDates.month_index( month_name )
      year = today.year if year_text == None else int( year_text )
      day = int( re.match( r'\d+', day_text ).group() )

      if month == None:
         return None

      try:
         return date( year, month, day )
      except ValueError:
         return None


   @classmethod
   def span( cls, text: str, today: date ) -> DateSpan | None:
      match = cls.DATE_RE.search( text )

      if match == None:
         return None

      start = cls.on_day( match.group( 'month' ), match.group( 'day' ), match.group( 'year' ), today )
      end = start

      if match.group( 'end_month' ) != None:
         end = cls.on_day(
            match.group( 'end_month' ),
            match.group( 'end_day' ),
            match.group( 'end_year' ),
            today,
         )

      if start == None or end == None:
         return None

      if end < start:
         end = end.replace( year=end.year + 1 )

      return DateSpan( start=start, end=end )


   @classmethod
   def read( cls, page_html: str, today: date ) -> list[ StationClosure ]:
      found = {}

      for notice in WebsiteClosure.notices( page_html ):
         pending = None

         for sentence in ViewingAlertSentenceBuilder.notice_parts( cls.text( notice ) ):
            current = cls.span( sentence, today )
            stations = cls.places( sentence ) if cls.closure( sentence ) else []

            if stations == []:
               pending = current
               continue

            chosen = current or pending
            start = None if chosen == None else chosen.start
            end = None if chosen == None else chosen.end

            for station in stations:
               found.setdefault( station, StationClosure( station, sentence, start, end ) )

            pending = None

      return list( found.values() )
