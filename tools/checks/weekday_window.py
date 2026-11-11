from __future__ import annotations

import calendar
from dataclasses import dataclass
import re
from typing import Any

from api.app_string_provider import AppStringProvider
from api.shared.calendar_dates import CalendarDates
from api.shared.schedule_row_input import SCHEDULE_ROW_WEEKDAY_KEYS
from .website_page import WebsitePage


@dataclass( frozen=True )
class WeekdayWindow():
   DAY_NAMES = tuple( name.casefold() for name in calendar.day_name )
   DAILY = frozenset( { 'daily', 'open daily' } )
   WEEKENDS = frozenset( { 'open weekends', 'weekends' } )
   RANGE_RE = re.compile(
      r'(?i)^(?:open\s+)?(?P<start>monday|tuesday|wednesday|thursday|friday|saturday|sunday)'
      r'\s+to\s+'
      r'(?P<end>monday|tuesday|wednesday|thursday|friday|saturday|sunday)$'
   )
   weekdays: frozenset[ int ]
   holidays_only: bool


   def matches( self, other: WeekdayWindow | None ) -> bool:
      return other != None and self == other


   def weekend_only( self ) -> bool:
      return self.weekdays == frozenset( { 5, 6 } )


   def description( self ) -> str:
      labels = [ CalendarDates.format_weekdays( set( self.weekdays ) ) ]

      if self.holidays_only:
         labels.append( AppStringProvider.format( 'schedule.dayLabels.holidays' ) )

      return ', '.join( label for label in labels if label != '' )


   def weekday_values( self ) -> tuple[ bool, bool, bool, bool, bool, bool, bool ]:
      return (
         0 in self.weekdays,
         1 in self.weekdays,
         2 in self.weekdays,
         3 in self.weekdays,
         4 in self.weekdays,
         5 in self.weekdays,
         6 in self.weekdays,
      )


   @classmethod
   def from_record( cls, record: Any ) -> WeekdayWindow:
      return cls(
         frozenset(
            index
            for index, day in enumerate( SCHEDULE_ROW_WEEKDAY_KEYS )
            if getattr( record, day )
         ),
         bool( record.holidays_only ),
      )


   @classmethod
   def parse( cls, status: str | None ) -> WeekdayWindow | None:
      return next( iter( cls.windows( cls.normalized( status ) ) ), None )


   @classmethod
   def normalized( cls, status: str | None ) -> str:
      if status == None:
         return ''

      text = WebsitePage.clean_html( status ).strip().casefold()

      if 'closed for the season' in text:
         return ''

      return text


   @classmethod
   def windows( cls, text: str ) -> list[ WeekdayWindow ]:
      if text in cls.DAILY:
         return [ cls( frozenset( range( 7 ) ), False ) ]

      if 'weekend' in text and 'holiday' in text:
         return [ cls( frozenset( { 5, 6 } ), True ) ]

      if text in cls.WEEKENDS:
         return [ cls( frozenset( { 5, 6 } ), False ) ]

      return [
         cls( cls.range_days( match.group( 'start' ), match.group( 'end' ) ), False )
         for match in cls.RANGE_RE.finditer( text )
      ]


   @classmethod
   def range_days( cls, start_name: str, end_name: str ) -> frozenset[ int ]:
      start = cls.DAY_NAMES.index( start_name.casefold() )
      end = cls.DAY_NAMES.index( end_name.casefold() )
      length = ( end - start ) % 7 + 1
      return frozenset( ( start + offset ) % 7 for offset in range( length ) )
