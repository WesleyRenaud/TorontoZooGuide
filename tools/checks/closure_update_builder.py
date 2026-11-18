from __future__ import annotations

import calendar
from datetime import date
import re

from api.models import Update
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from api.shared.text_values import TextValues
from api.updates.domain.update_type import UpdateType
from .closure_update import ClosureUpdate
from .closure_update_plan import ClosureUpdatePlan
from .website_closure import WebsiteClosure


class ClosureUpdateBuilder():
   MONTH = (
      r'jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|'
      r'aug(?:ust)?|sept(?:ember)?|sep(?:tember)?|oct(?:ober)?|'
      r'nov(?:ember)?|dec(?:ember)?'
   )
   SUFFIX = r'(?:st|nd|rd|th)?'
   DATE_RE = re.compile(
      rf'(?i)\b(?P<month>{ MONTH })\.?\s+(?P<day>\d{{1,2}}){ SUFFIX }'
      rf'(?:\s*,?\s*(?P<year>\d{{4}}))?'
      rf'(?:\s*(?:–|-|—|\+|to|through)\s*'
      rf'(?:(?P<end_month>{ MONTH })\.?\s+)?'
      rf'(?P<end_day>\d{{1,2}}){ SUFFIX }'
      rf'(?:\s*,?\s*(?P<end_year>\d{{4}}))?)?'
   )
   TODAY_RE = re.compile( r'(?i)\btoday\b' )
   TOMORROW_RE = re.compile( r'(?i)\btomorrow\b' )


   @classmethod
   def horizon( cls, today: date ) -> date:
      return CalendarDates.one_month_later( today )


   @classmethod
   def kept_end( cls, end: date | None, today: date ) -> date | None:
      horizon = cls.horizon( today )

      if end == None or end >= horizon:
         return end

      return horizon


   @classmethod
   def update_start( cls, update: Update ) -> date | None:
      return DateValues.parse_date_value( update.start_date )


   @classmethod
   def update_end( cls, update: Update ) -> date | None:
      if update.end_date in ( None, '' ):
         return None

      return DateValues.parse_date_value( update.end_date )


   @classmethod
   def app_closures( cls, updates: list[ Update ] ) -> list[ Update ]:
      return [
         update
         for update in updates
         if update.update_type == UpdateType.CLOSURE.value
      ]


   @classmethod
   def same( cls, notice: WebsiteClosure, update: Update ) -> bool:
      return update.title == notice.title and update.description == notice.description


   @classmethod
   def matched( cls, notice: WebsiteClosure, updates: list[ Update ] ) -> Update | None:
      for update in updates:
         if cls.same( notice, update ):
            return update

      return None


   @classmethod
   def on_website( cls, update: Update, notices: list[ WebsiteClosure ] ) -> bool:
      return cls.notice_for( update, notices ) != None


   @classmethod
   def notice_for(
         cls,
         update: Update,
         notices: list[ WebsiteClosure ] ) -> WebsiteClosure | None:
      for notice in notices:
         if cls.same( notice, update ):
            return notice

      return None


   @classmethod
   def month_number( cls, name: str ) -> int | None:
      folded = name.casefold().rstrip( '.' )

      if folded in ( 'sep', 'sept' ):
         folded = 'september'

      number = CalendarDates.month_index( folded )

      if number != None:
         return number

      for index, abbr in enumerate( calendar.month_abbr ):
         if abbr != '' and abbr.casefold() == folded:
            return index

      return None


   @classmethod
   def on_day(
         cls,
         month_name: str,
         day_text: str,
         year_text: str | None,
         today: date ) -> date | None:
      month = cls.month_number( month_name )

      if month == None:
         return None

      year = today.year if year_text == None else int( year_text )
      day = int( day_text )

      try:
         return date( year, month, day )
      except ValueError:
         return None


   @classmethod
   def dates_named( cls, text: str, today: date ) -> list[ date ]:
      found = []

      for match in cls.DATE_RE.finditer( text ):
         start = cls.on_day(
            match.group( 'month' ),
            match.group( 'day' ),
            match.group( 'year' ),
            today,
         )

         if start != None:
            found.append( start )

         if match.group( 'end_day' ) == None:
            continue

         end_month = match.group( 'end_month' ) or match.group( 'month' )
         end = cls.on_day(
            end_month,
            match.group( 'end_day' ),
            match.group( 'end_year' ) or match.group( 'year' ),
            today,
         )

         if end == None:
            continue

         if start != None and end < start:
            end = end.replace( year=end.year + 1 )

         found.append( end )

      if found != []:
         return found

      if cls.TODAY_RE.search( text ) != None:
         return [ today ]

      if cls.TOMORROW_RE.search( text ) != None:
         return [ CalendarDates.one_day_later( today ) ]

      return []


   @classmethod
   def named_end( cls, notice: WebsiteClosure, today: date ) -> date | None:
      days = cls.dates_named(
         TextValues.beside( notice.title, notice.description ),
         today,
      )

      if days == []:
         return None

      return max( days )


   @classmethod
   def addition(
         cls,
         notice: WebsiteClosure,
         today: date ) -> ClosureUpdate:
      named = cls.named_end( notice, today )

      if named == None:
         return ClosureUpdate(
            notice.title,
            notice.description,
            today,
            cls.horizon( today ),
         )

      return ClosureUpdate(
         notice.title,
         notice.description,
         today,
         named,
      )


   @classmethod
   def ending( cls, update: Update, today: date ) -> ClosureUpdate | None:
      start = cls.update_start( update )

      if start == None:
         return None

      return ClosureUpdate(
         update.title,
         update.description,
         start,
         CalendarDates.one_day_earlier( today ),
      )


   @classmethod
   def extension( cls, update: Update, today: date ) -> ClosureUpdate | None:
      start = cls.update_start( update )
      end = cls.update_end( update )
      kept = cls.kept_end( end, today )

      if start == None or kept == None or kept == end:
         return None

      return ClosureUpdate(
         update.title,
         update.description,
         start,
         kept,
      )


   @classmethod
   def added(
         cls,
         notices: list[ WebsiteClosure ],
         closures: list[ Update ],
         today: date ) -> list[ ClosureUpdate ]:
      return [
         cls.addition( notice, today )
         for notice in notices
         if cls.matched( notice, closures ) == None
      ]


   @classmethod
   def ended(
         cls,
         notices: list[ WebsiteClosure ],
         closures: list[ Update ],
         today: date ) -> list[ ClosureUpdate ]:
      endings = []

      for update in closures:
         if cls.on_website( update, notices ):
            continue

         ending = cls.ending( update, today )

         if ending == None:
            continue

         endings.append( ending )

      return endings


   @classmethod
   def dated(
         cls,
         update: Update,
         end: date ) -> ClosureUpdate | None:
      start = cls.update_start( update )
      current = cls.update_end( update )

      if start == None or current == end:
         return None

      return ClosureUpdate(
         update.title,
         update.description,
         start,
         end,
      )


   @classmethod
   def realigned(
         cls,
         notices: list[ WebsiteClosure ],
         closures: list[ Update ],
         today: date ) -> tuple[ list[ ClosureUpdate ], list[ ClosureUpdate ] ]:
      extended = []
      trimmed = []

      for update in closures:
         notice = cls.notice_for( update, notices )

         if notice == None:
            continue

         named = cls.named_end( notice, today )

         if named != None:
            change = cls.dated( update, named )

            if change == None:
               continue

            current = cls.update_end( update )

            if current == None or named < current:
               trimmed.append( change )
            else:
               extended.append( change )

            continue

         extension = cls.extension( update, today )

         if extension != None:
            extended.append( extension )

      return extended, trimmed


   @classmethod
   def build(
         cls,
         notices: list[ WebsiteClosure ],
         updates: list[ Update ],
         today: date ) -> ClosureUpdatePlan:
      closures = cls.app_closures( updates )
      extended, trimmed = cls.realigned( notices, closures, today )
      return ClosureUpdatePlan(
         cls.added( notices, closures, today ),
         cls.ended( notices, closures, today ),
         extended,
         trimmed,
      )
