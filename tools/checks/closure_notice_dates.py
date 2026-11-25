from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import re

from api.shared.calendar_dates import CalendarDates


@dataclass( frozen=True )
class ClosureNoticeDates():
   end: date | None = None
   start: date | None = None

   MONTH = (
      r'jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|'
      r'aug(?:ust)?|sept(?:ember)?|sep(?:tember)?|oct(?:ober)?|'
      r'nov(?:ember)?|dec(?:ember)?'
   )
   SUFFIX = r'(?:st|nd|rd|th)?'
   DATE_RE = re.compile(
      rf'(?i)\b(?P<month>{ MONTH })\.?\s+(?P<day>\d{{1,2}}){ SUFFIX }\b'
      rf'(?:\s*,?\s*(?P<year>\d{{4}}))?'
      rf'(?:\s*(?:–|-|—|\+|to|through)\s*'
      rf'(?:(?P<end_month>{ MONTH })\.?\s+)?'
      rf'(?P<end_day>\d{{1,2}}){ SUFFIX }\b'
      rf'(?:\s*,?\s*(?P<end_year>\d{{4}}))?)?'
   )
   MID_MONTH_RE = re.compile(
      rf'(?i)(?:^|\b(?:until|through|to)\s+|[–—-]\s*)'
      rf'mid[-‑–—\s]+(?P<month>{ MONTH })\b\.?'
      rf'(?:\s*,?\s*(?P<year>\d{{4}})\b)?',
   )
   EXACT_END_PREFIX_RE = re.compile(
      r'(?i)\b(?:until|through|to|reopen(?:s|ing)?(?:\s+on)?)'
      r'\s+(?:(?:mon|tues|wednes|thurs|fri|satur|sun)day,?\s+)?$',
   )
   TODAY_RE = re.compile( r'(?i)\btoday\b' )
   TOMORROW_RE = re.compile( r'(?i)\btomorrow\b' )


   @classmethod
   def parse( cls, text: str, today: date ) -> ClosureNoticeDates:
      matches = list( cls.DATE_RE.finditer( text ) )
      estimate = cls.estimated_range( text, matches, today )
      if estimate != None:
         return estimate

      dates = [ day for match in matches for day in cls.exact_days( match, today.year ) ]
      if dates:
         return cls( start=min( dates ), end=max( dates ) )
      if cls.TODAY_RE.search( text ) != None:
         return cls( today, today )
      if cls.TOMORROW_RE.search( text ) != None:
         tomorrow = CalendarDates.one_day_later( today )
         return cls( tomorrow, tomorrow )
      return cls()


   @staticmethod
   def parse_day( month_name: str, day: str, year: int ) -> date | None:
      month = CalendarDates.normalize_month( month_name.title() )
      if month == None:
         return None

      try:
         return date( year, month, int( day ) )
      except ValueError:
         return None


   @classmethod
   def exact_days(
         cls,
         match: re.Match[ str ],
         year: int ) -> list[ date ]:
      start = cls.parse_day( match[ 'month' ], match[ 'day' ], int( match[ 'year' ] or year ) )
      if match[ 'end_day' ] == None:
         return [ start ] if start != None else []

      month = match[ 'end_month' ] or match[ 'month' ]
      end_year = int( match[ 'end_year' ] or match[ 'year' ] or year )
      end = cls.parse_day( month, match[ 'end_day' ], end_year )
      if start != None and end != None and end < start:
         end = end.replace( year=end.year + 1 )
      return [ day for day in ( start, end ) if day != None ]


   @classmethod
   def estimated_range(
         cls,
         text: str,
         matches: list[ re.Match[ str ] ],
         today: date ) -> ClosureNoticeDates | None:
      estimate = cls.MID_MONTH_RE.search( text )
      if estimate == None or len( matches ) > 1:
         return None

      named = next( iter( matches ), None )
      if named != None and (
         named.start() >= estimate.start()
         or cls.EXACT_END_PREFIX_RE.search( text, 0, named.start() ) != None
      ):
         return None

      exact = cls.exact_days( named, today.year ) if named != None else []
      if len( exact ) > 1:
         return None

      start = next( iter( exact ), None )
      start_has_year = named != None and named[ 'year' ] != None
      midpoint = cls.midpoint( estimate, today, start if start_has_year else None )
      if midpoint == None:
         return None

      if start != None and named != None and not start_has_year:
         year = midpoint.year - ( start.month > midpoint.month )
         start = cls.parse_day( named[ 'month' ], named[ 'day' ], year ) or start
      return cls(
         start=start,
         end=max( start or today, midpoint, CalendarDates.one_week_later( today ) ),
      )


   @staticmethod
   def midpoint(
         estimate: re.Match[ str ],
         today: date,
         dated_start: date | None ) -> date | None:
      month = CalendarDates.normalize_month( estimate[ 'month' ].title() )
      if month == None:
         return None

      if estimate[ 'year' ] != None:
         years = ( int( estimate[ 'year' ] ), )
      elif dated_start != None:
         years = ( dated_start.year + ( month < dated_start.month ), )
      else:
         years = ( today.year, today.year - 1, today.year + 1 )

      return min(
         (
            CalendarDates.month_midpoint( year, month )
            for year in years
            if date.min.year <= year <= date.max.year
         ),
         key=lambda midpoint: abs( midpoint - today ),
         default=None,
      )
