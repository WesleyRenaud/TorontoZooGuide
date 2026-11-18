from __future__ import annotations

from dataclasses import replace
from datetime import date
import json
from pathlib import Path
import re
import subprocess

from api.app_string_provider import AppStringProvider
from api.attractions.data_access.attraction_hours_schedule_provider import AttractionHoursScheduleProvider
from api.attractions.data_access.attraction_hours_schedule_record import AttractionHoursScheduleRecord
from api.attractions.scheduling.attraction_hours_clock import AttractionHoursClock
from api.attractions.scheduling.attraction_hours_schedule_time_bounds_builder import AttractionHoursScheduleTimeBoundsBuilder
from api.attractions.scheduling.attraction_hours_span import AttractionHoursSpan
from api.database_connection_provider import DatabaseConnectionProvider
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from api.shared.peak_months import PeakMonths
from .attraction_hours import AttractionHours
from .check_report import CheckReport
from .opening_window import OpeningWindow
from tools.fix.attraction_hours_fixer import AttractionHoursFixer
from .website_page import WebsitePage
from .weekday_window import WeekdayWindow
from .window_change import WindowChange
from .zoo_hours_page import ZooHoursPage


class AttractionHoursReader():
   WEEKDAYS = 'weekdays'
   WEEKENDS = 'weekends'
   FRIDAYS = 'fridays'
   DAILY = 'daily'
   WEEKDAY = 'weekday'
   DURING_ZOO_HOURS = 'during zoo hours'
   OPEN = 'open'
   CLOSE = 'close'
   COMMENT_RE = re.compile( r'(?is)<!--.*?-->' )
   CLOCK = (
      r'(?P<{side}_hour>\d{{1,2}})(?::(?P<{side}_minute>\d{{2}}))?\s*'
      r'(?P<{side}_meridiem>am|pm)'
   )
   RANGE = (
      CLOCK.format( side=OPEN )
      + r'\s*(?:[-–—]|to)\s*'
      + CLOCK.format( side=CLOSE )
   )
   RANGE_RE = re.compile( '(?i)' + RANGE )
   LABELED_RE = re.compile(
      '(?i)'
      + r'\b(?P<label>'
      + WEEKDAYS
      + '|'
      + FRIDAYS
      + '|'
      + WEEKENDS
      + r'(?:\s*(?:/|&)\s*holidays)?)\s*:\s*'
      + RANGE
   )
   TOURS_URL = 'https://my.hornblower.com/graphql'
   PROPERTY_ID = 'tozoo'
   TOUR_ID_RE = re.compile( r'tour-id="(?P<id>\d+)"' )
   TOURS_QUERY = (
      'query tours( $propertyId: String!, $bookingType: String, $includeAvailability: Boolean ) '
      '{ searchTours( propertyId: $propertyId, bookingType: $bookingType, '
      'includeAvailability: $includeAvailability ) '
      '{ bookingTypeId localizedInfo { locale values { id value } } } }'
   )


   @classmethod
   def parse(
         cls,
         body: str,
         page_html: str,
         status: str | None = None ) -> AttractionHours | None:
      if status == None and cls.season_closed( body ):
         return None

      text = cls.plain_text( body )
      hours = cls.from_labels( text )

      if cls.has_hours( hours ):
         return hours

      if cls.DURING_ZOO_HOURS in text.casefold():
         return cls.header( page_html )

      if status == None:
         status = WebsitePage.opening_status( body )

      return cls.from_single( text, cls.weekend_only( status or '' ) )


   @classmethod
   def published( cls, body: str, page_html: str, href: str ) -> AttractionHours | None:
      hours = cls.parse( body, page_html )

      if hours != None or cls.season_closed( body ):
         return hours

      description = cls.tour_description( href )

      if description == None:
         return None

      return cls.parse( description, description, WebsitePage.opening_status( body ) )


   @classmethod
   def tour_description( cls, href: str ) -> str | None:
      page = WebsitePage.fetch_text( WebsitePage.absolute_url( href ) )
      match = cls.TOUR_ID_RE.search( page )

      if match == None:
         return None

      return cls.description( match.group( 'id' ) )


   @classmethod
   def description( cls, tour_id: str ) -> str | None:
      payload = json.dumps( {
         'query': cls.TOURS_QUERY,
         'variables': {
            'propertyId': cls.PROPERTY_ID,
            'bookingType': tour_id,
            'includeAvailability': False,
         },
      } )
      result = subprocess.run(
         [
            'curl',
            '-fsS',
            '--max-time',
            '30',
            '-A',
            WebsitePage.USER_AGENT,
            '-H',
            'Content-Type: application/json',
            '-H',
            'Accept: application/json',
            '--data',
            payload,
            cls.TOURS_URL,
         ],
         check=False,
         capture_output=True,
      )

      if result.returncode != 0:
         return None

      tours = json.loads( result.stdout ).get( 'data', {} ).get( 'searchTours' ) or []

      if tours == []:
         return None

      for info in tours[ 0 ][ 'localizedInfo' ]:
         if info[ 'locale' ] != 'en':
            continue

         for value in info[ 'values' ]:
            if value[ 'id' ] == 'description':
               return value[ 'value' ] or None

      return None


   @classmethod
   def has_hours( cls, hours: AttractionHours ) -> bool:
      return hours.weekday_opens != None or hours.weekend_opens != None


   @classmethod
   def matches( cls, left: AttractionHours, right: AttractionHours ) -> bool:
      return (
         cls.same_time( left.weekday_opens, right.weekday_opens )
         and cls.same_time( left.weekday_closes, right.weekday_closes )
         and cls.same_time( left.weekend_opens, right.weekend_opens )
         and cls.same_time( left.weekend_closes, right.weekend_closes )
      )


   @classmethod
   def complete(
         cls,
         published: AttractionHours,
         stored: AttractionHours | None ) -> AttractionHours | None:
      current = stored or AttractionHours()
      weekday_opens = cls.prefer(
         published.weekday_opens,
         current.weekday_opens,
      ) or cls.prefer( published.weekend_opens, current.weekend_opens )
      weekday_closes = cls.prefer(
         published.weekday_closes,
         current.weekday_closes,
      ) or cls.prefer( published.weekend_closes, current.weekend_closes )
      weekend_opens = cls.prefer(
         published.weekend_opens,
         current.weekend_opens,
      ) or cls.prefer( published.weekday_opens, current.weekday_opens )
      weekend_closes = cls.prefer(
         published.weekend_closes,
         current.weekend_closes,
      ) or cls.prefer( published.weekday_closes, current.weekday_closes )

      if None in ( weekday_opens, weekday_closes, weekend_opens, weekend_closes ):
         return None

      return AttractionHours(
         weekday_opens=weekday_opens,
         weekday_closes=weekday_closes,
         weekend_opens=weekend_opens,
         weekend_closes=weekend_closes,
      )


   @classmethod
   def prefer( cls, published: str | None, current: str | None ) -> str | None:
      if published == None:
         return current

      if current != None and cls.same_time( published, current ):
         return current

      return published


   @classmethod
   def same_time( cls, left: str | None, right: str | None ) -> bool:
      return DateValues.parse_time_value( left ) == DateValues.parse_time_value( right )


   @classmethod
   def season_closed( cls, body: str ) -> bool:
      status = WebsitePage.opening_status( body ) or ''
      phrase = AppStringProvider.format( 'checks.closedForSeason' ).casefold()
      return phrase in status.casefold()


   @classmethod
   def plain_text( cls, page_html: str ) -> str:
      return WebsitePage.clean_html( cls.COMMENT_RE.sub( ' ', page_html ) )


   @classmethod
   def from_labels( cls, text: str ) -> AttractionHours:
      hours = AttractionHours()

      for match in cls.LABELED_RE.finditer( text ):
         span = cls.hour_span( match )

         if span == None:
            continue

         opens, closes = span
         label = match.group( 'label' ).casefold()

         if label.startswith( cls.WEEKENDS ):
            hours = cls.with_weekend( hours, opens, closes )
         elif label == cls.WEEKDAYS:
            hours = cls.with_weekday( hours, opens, closes, overwrite=True )
         else:
            hours = cls.with_weekday( hours, opens, closes )

      return hours


   @classmethod
   def with_weekday(
         cls,
         hours: AttractionHours,
         opens: str,
         closes: str,
         overwrite: bool = False ) -> AttractionHours:
      if hours.weekday_opens != None and not overwrite:
         return hours

      return replace( hours, weekday_opens=opens, weekday_closes=closes )


   @classmethod
   def with_weekend(
         cls,
         hours: AttractionHours,
         opens: str,
         closes: str ) -> AttractionHours:
      if hours.weekend_opens != None:
         return hours

      return replace( hours, weekend_opens=opens, weekend_closes=closes )


   @classmethod
   def from_single( cls, text: str, weekend_only: bool ) -> AttractionHours | None:
      stripped = cls.LABELED_RE.sub( ' ', text )
      matches = list( cls.RANGE_RE.finditer( stripped ) )

      if len( matches ) != 1:
         return None

      span = cls.hour_span( matches[ 0 ] )

      if span == None:
         return None

      opens, closes = span

      if weekend_only:
         return AttractionHours( weekend_opens=opens, weekend_closes=closes )

      return AttractionHours(
         weekday_opens=opens,
         weekday_closes=closes,
         weekend_opens=opens,
         weekend_closes=closes,
      )


   @classmethod
   def weekend_only( cls, status: str ) -> bool:
      folded = status.casefold()
      return (
         cls.WEEKENDS in folded
         and cls.DAILY not in folded
         and cls.WEEKDAY not in folded
      )


   @classmethod
   def header( cls, page_html: str ) -> AttractionHours | None:
      openings = WebsitePage.col3_openings( page_html )
      head = page_html

      if openings != []:
         head = page_html[ :openings[ 0 ].start() ]

      text = cls.plain_text( head )
      hours = cls.from_labels( text )

      if cls.has_hours( hours ):
         return cls.complete( hours, None )

      return cls.from_single( text, False )


   @classmethod
   def hour_span( cls, match: re.Match[ str ] ) -> tuple[ str, str ] | None:
      opens = cls.display_time( match, cls.OPEN )
      closes = cls.display_time( match, cls.CLOSE )

      if opens == None or closes == None:
         return None

      return opens, closes


   @classmethod
   def display_time( cls, match: re.Match[ str ], side: str ) -> str | None:
      parsed = ZooHoursPage.parse_clock(
         match.group( f'{ side }_hour' ),
         match.group( f'{ side }_minute' ),
         match.group( f'{ side }_meridiem' ),
      )
      return DateValues.format_display_time_value( parsed )


   @classmethod
   def load( cls, database: Path ) -> list[ AttractionHoursScheduleRecord ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return AttractionHoursScheduleProvider.fetch_hours_schedule_records( connection )
      finally:
         connection.close()


   @classmethod
   def record(
         cls,
         records: list[ AttractionHoursScheduleRecord ],
         name: str,
         today: date ) -> AttractionHoursScheduleRecord | None:
      return next(
         (
            record
            for record in records
            if record.attraction == name
            and DateValues.is_date_in_range(
               today,
               record.schedule_start_date,
               record.schedule_end_date,
            )
         ),
         None,
      )


   @classmethod
   def from_record( cls, record: AttractionHoursScheduleRecord ) -> AttractionHours:
      return AttractionHours(
         weekday_opens=record.weekday_start_time,
         weekday_closes=record.weekday_end_time,
         weekend_opens=record.weekend_holiday_start_time,
         weekend_closes=record.weekend_holiday_end_time,
      )


   @classmethod
   def change(
         cls,
         chosen: AttractionHours,
         record: AttractionHoursScheduleRecord | None,
         end: date | None ) -> WindowChange | None:
      if record == None:
         return WindowChange.SET

      stored = cls.from_record( record )
      current = DateValues.parse_date_value( record.schedule_end_date )

      if cls.matches( stored, chosen ) and current == end:
         return None

      if not cls.matches( stored, chosen ):
         return WindowChange.SET

      return OpeningWindow.end_change( current, end )


   @classmethod
   def starting(
         cls,
         record: AttractionHoursScheduleRecord | None,
         today: date ) -> date:
      if record == None:
         return today

      start = DateValues.parse_date_value( record.schedule_start_date )

      if start != None and start >= today:
         return start

      return today


   @classmethod
   def span( cls, opens: str | None, closes: str | None ) -> str:
      return (
         ( opens or '' )
         + CheckReport.text( 'checks.hoursTo' )
         + ( closes or '' )
      )


   @classmethod
   def hours_text( cls, hours: AttractionHours ) -> str:
      weekday = cls.span( hours.weekday_opens, hours.weekday_closes )
      weekend = cls.span( hours.weekend_opens, hours.weekend_closes )

      if weekday == weekend:
         return weekday

      return (
         weekday
         + CheckReport.text( 'checks.attractionHoursWeekdayJoin' )
         + weekend
         + CheckReport.text( 'checks.attractionHoursWeekendSpan' )
      )


   @classmethod
   def sentence(
         cls,
         kind: WindowChange,
         hours: AttractionHours,
         end: date | None,
         resume: date | None = None ) -> str:
      if kind == WindowChange.SET:
         when = cls.hours_text( hours )
         resumed = DateValues.format_display_date_value( resume )
         shown = DateValues.format_display_date_value( end )

         if resumed != None:
            when = (
               when
               + CheckReport.text( 'checks.attractionHoursResumeFrom' )
               + resumed
            )

         if shown != None:
            when = when + CheckReport.text( 'checks.dateThrough' ) + shown

         return (
            CheckReport.text( 'checks.setAttractionHoursFrom' )
            + when
            + CheckReport.text( 'checks.period' )
         )

      key = (
         'checks.extendedAttractionHoursThrough'
         if kind == WindowChange.EXTENDED
         else 'checks.trimmedAttractionHoursThrough'
      )
      shown = DateValues.format_display_date_value( end )
      return (
         CheckReport.text( key )
         + ( shown or '' )
         + CheckReport.text( 'checks.period' )
      )


   @classmethod
   def fitting_spans(
         cls,
         database: Path,
         span: AttractionHoursSpan,
         hours: AttractionHours ) -> list[ AttractionHoursSpan ]:
      connection = DatabaseConnectionProvider.open( str( database ) )

      try:
         return AttractionHoursScheduleTimeBoundsBuilder.fitting_spans(
            connection,
            span,
            AttractionHoursClock(
               weekday_start_time=hours.weekday_opens,
               weekday_end_time=hours.weekday_closes,
               weekend_holiday_start_time=hours.weekend_opens,
               weekend_holiday_end_time=hours.weekend_closes,
            ),
         )
      finally:
         connection.close()


   @classmethod
   def span_change(
         cls,
         chosen: AttractionHours,
         records: list[ AttractionHoursScheduleRecord ],
         name: str,
         covering: AttractionHoursScheduleRecord | None,
         index: int,
         span_start: date,
         span_end: date | None ) -> WindowChange | None:
      if index > 0:
         covering = cls.record( records, name, span_start )
         christmas = CalendarDates.one_day_earlier( span_start )

         if covering != None and DateValues.is_date_in_range(
               christmas,
               covering.schedule_start_date,
               covering.schedule_end_date ):
            return WindowChange.SET

      return cls.change( chosen, covering, span_end )


   @classmethod
   def report_lines(
         cls,
         database: Path,
         name: str,
         status: str | None,
         hours: AttractionHours,
         records: list[ AttractionHoursScheduleRecord ],
         today: date,
         months: PeakMonths,
         schedule_end: date | None = None ) -> tuple[ list[ str ], str | None ]:
      record = cls.record( records, name, today )
      stored = None if record == None else cls.from_record( record )
      chosen = cls.complete( hours, stored )

      if chosen == None:
         return [], None

      pattern = WeekdayWindow.parse( status )
      season_end = months.schedule_end(
         pattern != None and pattern.weekend_only(),
         today,
      )
      spans = cls.fitting_spans(
         database,
         AttractionHoursSpan(
            start=cls.starting( record, today ),
            end=season_end,
         ),
         chosen,
      )
      lines: list[ str ] = []
      saved = 0

      for index, span in enumerate( spans ):
         kind = cls.span_change(
            chosen,
            records,
            name,
            record,
            index,
            span.start,
            span.end,
         )

         if kind == None:
            continue

         if AttractionHoursFixer.apply(
               database,
               name,
               span.start,
               span.end,
               chosen,
         ):
            saved += 1

         lines.append( CheckReport.detail_item(
            cls.sentence(
               kind,
               chosen,
               span.end,
               span.start if index > 0 else None,
            ),
         ) )

      if schedule_end != None and len( lines ) == 1 and span.end == schedule_end:
         return [], cls.hours_text( chosen )

      if saved > 0:
         CheckReport.note_fixed( saved )

      opening = (
         CheckReport.text( 'checks.setAttractionHoursFrom' )
         + cls.hours_text( chosen )
      )
      return CheckReport.shared_lines( opening, lines ), None


   @classmethod
   def unfixed( cls, line: str ) -> bool:
      phrases = (
         CheckReport.text( 'checks.setAttractionHoursFrom' ),
         CheckReport.text( 'checks.extendedAttractionHoursThrough' ),
         CheckReport.text( 'checks.trimmedAttractionHoursThrough' ),
      )
      return all( phrase not in line for phrase in phrases )
