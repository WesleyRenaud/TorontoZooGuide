from __future__ import annotations

from datetime import date
import re

from api.shared.calendar_dates import CalendarDates


class DatePatterns():
   MONTH_AND_DAY = r'(?P<month>[a-z]+)\s+(?P<day>\d{1,2})(?:st|nd|rd|th)?'
   MONTH_DAY_RE = re.compile( rf'(?i){ MONTH_AND_DAY }' )
   DATE_RE = re.compile( rf'(?i){ MONTH_AND_DAY },?\s+(?P<year>\d{{4}})' )
   THROUGH_DATE_RE = re.compile(
      rf'(?i)through\s+{ MONTH_AND_DAY }(?:\s*,?\s*(?P<year>\d{{4}}))?'
   )


   @classmethod
   def through_date( cls, status: str, today: date ) -> date | None:
      match = cls.THROUGH_DATE_RE.search( status.casefold() )

      if match == None:
         return None

      month = CalendarDates.month_index( match.group( 'month' ) )

      if month == None:
         return None

      year = today.year if match.group( 'year' ) == None else int( match.group( 'year' ) )

      try:
         return date( year, month, int( match.group( 'day' ) ) )
      except ValueError:
         return None
