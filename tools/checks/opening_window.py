from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from api.shared.date_values import DateValues
from api.shared.peak_months import PeakMonths
from .check_report import CheckReport
from .weekday_window import WeekdayWindow
from .window_change import WindowChange


@dataclass( frozen=True )
class OpeningWindow():
   start: date
   end: date | None
   pattern: WeekdayWindow
   change: WindowChange = WindowChange.SET


   @classmethod
   def covering(
         cls,
         records: list[ Any ],
         name: str,
         today: date,
         owner: str ) -> OpeningWindow | None:
      record = next(
         (
            candidate
            for candidate in records
            if getattr( candidate, owner ) == name
            and DateValues.is_date_in_range(
               today,
               candidate.schedule_start_date,
               candidate.schedule_end_date,
            )
         ),
         None,
      )

      if record == None:
         return None

      end = record.schedule_end_date
      return cls(
         start=DateValues.parse_date_value( record.schedule_start_date ),
         end=None if end == None else DateValues.parse_date_value( end ),
         pattern=WeekdayWindow.from_record( record ),
      )


   def stored_end( self ) -> str | None:
      if self.end == None:
         return None

      return self.end.isoformat()


   @classmethod
   def replacement(
         cls,
         website: WeekdayWindow,
         active: OpeningWindow | None,
         today: date,
         months: PeakMonths ) -> OpeningWindow | None:
      target = months.schedule_end( website.weekend_only(), today )

      if active != None and website.matches( active.pattern ):
         if active.end == target:
            return None

         start = today if active.start == None or active.start < today else active.start
         return cls( start, target, website, cls.end_change( active.end, target ) )

      return cls( today, target, website )


   @classmethod
   def end_change( cls, current: date | None, target: date | None ) -> WindowChange:
      if target == None:
         return WindowChange.SET

      if current != None and current > target:
         return WindowChange.TRIMMED

      return WindowChange.EXTENDED


   @classmethod
   def schedule_line( cls, window: OpeningWindow ) -> str:
      if window.change != WindowChange.SET and window.end != None:
         key = (
            'checks.extendedScheduleThrough'
            if window.change == WindowChange.EXTENDED
            else 'checks.trimmedScheduleThrough'
         )
         return (
            CheckReport.text( key )
            + DateValues.format_display_date_value( window.end )
            + CheckReport.text( 'checks.period' )
         )

      return CheckReport.set_schedule( window.start, window.end )


   @classmethod
   def unfixed( cls, line: str ) -> bool:
      phrases = (
         CheckReport.text( 'checks.setScheduleFrom' ),
         CheckReport.text( 'checks.setScheduleFor' ),
         CheckReport.text( 'checks.extendedScheduleThrough' ),
         CheckReport.text( 'checks.trimmedScheduleThrough' ),
      )
      return all( phrase not in line for phrase in phrases )


   @classmethod
   def detail( cls, window: OpeningWindow, clock: str | None = None ) -> str:
      days = window.pattern.description()

      if clock != None:
         days += CheckReport.text( 'checks.attractionHoursResumeFrom' ) + clock

      return CheckReport.join_lines( [
         CheckReport.detail_item( cls.schedule_line( window ) ),
         CheckReport.detail_item( CheckReport.text( 'format.bulletItem' ) + days ),
      ] )


   @classmethod
   def compared_note( cls, today: date ) -> str:
      return (
         CheckReport.text( 'checks.websiteDatesCompared' )
         + DateValues.format_display_date_value( today )
      )
