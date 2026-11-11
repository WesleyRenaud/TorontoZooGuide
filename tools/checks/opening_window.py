from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from api.shared.date_values import DateValues
from api.shared.peak_months import PeakMonths
from .check_report import CheckReport
from .weekday_window import WeekdayWindow


@dataclass( frozen=True )
class OpeningWindow():
   start: date
   end: date | None
   pattern: WeekdayWindow


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

         return cls( active.start, target, website )

      return cls( today, target, website )


   @classmethod
   def detail( cls, window: OpeningWindow ) -> str:
      when = DateValues.format_display_date_value( window.start )
      end = DateValues.format_display_date_value( window.end )

      if end != None:
         when = when + CheckReport.text( 'checks.dateThrough' ) + end

      return CheckReport.join_lines( [
         CheckReport.detail_item(
            CheckReport.text( 'checks.setScheduleFrom' )
            + when
            + CheckReport.text( 'checks.period' )
         ),
         CheckReport.detail_item(
            CheckReport.text( 'format.bulletItem' )
            + window.pattern.description()
         ),
      ] )


   @classmethod
   def compared_note( cls, today: date ) -> str:
      return (
         CheckReport.text( 'checks.websiteDatesCompared' )
         + DateValues.format_display_date_value( today )
      )
