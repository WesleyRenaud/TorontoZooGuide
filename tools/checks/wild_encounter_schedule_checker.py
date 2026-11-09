from __future__ import annotations

import argparse
from datetime import date
from datetime import timedelta
from pathlib import Path
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.domain.wild_encounter_link import WildEncounterLink
from api.wild_encounters.domain.wild_encounter_schedule import WildEncounterSchedule
from .bookable_dates import BookableDates
from .booking_calendar import BookingCalendar
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .encounter_schedule_slots import EncounterScheduleSlots
from .encounter_schedule_table import EncounterScheduleTable
from .paths import Paths
from .schedule_check import ScheduleCheck
from .schedule_slot import ScheduleSlot
from .schedule_slot_group import ScheduleSlotGroup
from tools.fix.encounter_schedule_correction import EncounterScheduleCorrection
from tools.fix.wild_encounter_window_fixer import WildEncounterWindowFixer
from .website_page import WebsitePage
from .wild_encounter_detail_image import WildEncounterDetailImage


class WildEncounterScheduleChecker():
   PAGE = 'wildencounters'
   BOOKING_HORIZON_DAYS = 400


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.wildEncounter.description' )
      )


   @classmethod
   def load_links( cls, database: Path ) -> list[ WildEncounterLink ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return WildEncounterCoordinator.get_wild_encounter_links()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def load_schedules( cls, database: Path ) -> list[ WildEncounterSchedule ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return WildEncounterCoordinator.get_wild_encounter_schedules()
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def active_slots(
         cls,
         schedules: list[ WildEncounterSchedule ],
         today: date ) -> EncounterScheduleSlots:
      slots = EncounterScheduleSlots()

      for schedule in schedules:
         if not schedule.covers( today ):
            continue

         encounter_time = DateValues.parse_time_value(
            EncounterScheduleTable.normalize_clock( schedule.encounter_time )
         )

         for weekday in schedule.weekday_indexes():
            slots.add( schedule.name, ScheduleSlot(
               weekday=weekday,
               time=encounter_time,
            ) )

      return slots


   @classmethod
   def names_only( cls, names: set[ str ] ) -> list[ str ]:
      return [
         CheckReport.text( 'checks.categoryItem' ) + name
         for name in sorted( names, key=str.casefold )
      ]


   @classmethod
   def different_slot_lines(
         cls,
         names: set[ str ],
         website_slots: EncounterScheduleSlots,
         app_slots: EncounterScheduleSlots ) -> list[ str ]:
      lines = []

      for name in sorted( names, key=str.casefold ):
         lines.append( CheckReport.join_lines( [
            CheckReport.text( 'checks.categoryItem' ) + name,
            CheckReport.detail_item(
               CheckReport.text( 'checks.websiteSchedule' )
               + ScheduleSlotGroup.describe( website_slots.for_name( name ) ),
            ),
            CheckReport.detail_item(
               CheckReport.text( 'checks.appSchedule' )
               + ScheduleSlotGroup.describe( app_slots.for_name( name ) ),
            ),
         ] ) )

      return lines


   @classmethod
   def window_names(
         cls,
         website_names: set[ str ],
         encounters: list[ WildEncounterLink ] ) -> list[ str ]:
      catalog = { encounter.name for encounter in encounters }
      return sorted( website_names & catalog, key=str.casefold )


   @classmethod
   def window_fix(
         cls,
         database: Path,
         correction: EncounterScheduleCorrection ) -> str:
      return WildEncounterWindowFixer.apply( database, correction )


   @classmethod
   def window_detail(
         cls,
         database: Path,
         name: str,
         encounters: list[ WildEncounterLink ],
         schedules: list[ WildEncounterSchedule ],
         website_slots: EncounterScheduleSlots,
         first: date,
         last: date ) -> str | None:
      booking = cls.read_bookable(
         WildEncounterLink.booking_link( name, encounters ),
         first,
         last,
      )

      if booking.failure != None:
         return booking.failure

      app_dates = WildEncounterSchedule.dates( schedules, name, first, last )
      mismatch = cls.date_mismatch( app_dates, booking.dates )

      if mismatch == None:
         return None

      return cls.window_fix(
         database,
         WildEncounterWindowFixer.correction(
            name,
            booking.dates,
            app_dates,
            schedules,
            website_slots,
            first,
         ),
      )


   @classmethod
   def window_lines(
         cls,
         database: Path,
         names: list[ str ],
         encounters: list[ WildEncounterLink ],
         schedules: list[ WildEncounterSchedule ],
         website_slots: EncounterScheduleSlots,
         first: date,
         last: date ) -> list[ str ]:
      lines = []

      for name in names:
         detail = cls.window_detail(
            database,
            name,
            encounters,
            schedules,
            website_slots,
            first,
            last,
         )

         if detail == None:
            continue

         lines.append( cls.window_line( name, detail ) )

      return lines


   @classmethod
   def window_line( cls, name: str, detail: str ) -> str:
      lines = [ CheckReport.text( 'checks.categoryItem' ) + name ]
      photo = WildEncounterDetailImage.source( name )

      if ( Paths.ROOT / photo ).is_file():
         lines.append( CheckReport.detail_item(
            CheckReport.text( 'checks.photo' ) + photo
         ) )

      lines.append( detail )
      return CheckReport.join_lines( lines )


   @classmethod
   def unfixed_windows( cls, lines: list[ str ] ) -> int:
      phrase = CheckReport.text( 'checks.setScheduleFrom' )
      return len( [
         line
         for line in lines
         if phrase not in line
      ] )


   @classmethod
   def detail_line( cls, key: str, value: str = '' ) -> str:
      return CheckReport.detail_item( CheckReport.text( key ) + value )


   @classmethod
   def date_line( cls, key: str, dates: list[ date ] ) -> str | None:
      if not dates:
         return None

      return cls.detail_line( key, CheckReport.format_date_list( dates ) )


   @classmethod
   def date_mismatch( cls, app_dates: list[ date ], bookable: list[ date ] ) -> str | None:
      lines = [
         line
         for line in (
            cls.date_line(
               'checks.appDatesNotBookable',
               sorted( set( app_dates ) - set( bookable ) ),
            ),
            cls.date_line(
               'checks.bookableDatesNotInApp',
               sorted( set( bookable ) - set( app_dates ) ),
            ),
         )
         if line != None
      ]

      if not lines:
         return None

      return CheckReport.join_lines( lines )


   @classmethod
   def read_bookable(
         cls,
         link: str,
         first: date,
         last: date ) -> BookableDates:
      if link == '':
         return BookableDates( dates=[], failure=cls.detail_line( 'checks.noBookingLink' ) )

      try:
         booking_type = BookingCalendar.tour_id( WebsitePage.fetch_text( link ) )
      except RuntimeError:
         return BookableDates( dates=[], failure=cls.detail_line( 'checks.couldNotReadBookingPage' ) )

      if booking_type == None:
         return BookableDates( dates=[], failure=cls.detail_line( 'checks.noTourId' ) )

      try:
         return BookableDates(
            dates=BookingCalendar.enabled_dates( booking_type, first, last ),
            failure=None,
         )
      except ( RuntimeError, ValueError, KeyError, TypeError ):
         return BookableDates( dates=[], failure=cls.detail_line( 'checks.couldNotReadBookingCalendar' ) )


   @classmethod
   def comparison_note( cls, first: date, last: date ) -> str:
      return (
         CheckReport.text( 'checks.bookingDatesCompared' )
         + CheckReport.format_date_span( first, last )
         + CheckReport.text( 'checks.period' )
      )


   @classmethod
   def schedule_check( cls, database: Path, today: date ) -> ScheduleCheck:
      encounters = cls.load_links( database )
      schedules = cls.load_schedules( database )
      website_slots = EncounterScheduleTable.resolve(
         EncounterScheduleTable.parse( WebsitePage.fetch_text( WebsitePage.url( cls.PAGE ) ) ),
         encounters,
      )
      current_app_slots = cls.active_slots( schedules, today )
      website_names = website_slots.names()
      app_names = current_app_slots.names()
      catalog = { encounter.name for encounter in encounters }
      shared_names = website_names & app_names
      different_names = {
         name
         for name in shared_names
         if website_slots.for_name( name ) != current_app_slots.for_name( name )
      }
      first = today + timedelta( days=1 )
      last = today + timedelta( days=cls.BOOKING_HORIZON_DAYS )

      return ScheduleCheck(
         note=cls.comparison_note( first, last ),
         only_in_app=cls.names_only( app_names - website_names ),
         only_on_website=cls.names_only( website_names - catalog ),
         different_slots=cls.different_slot_lines(
            different_names,
            website_slots,
            current_app_slots,
         ),
         windows=cls.window_lines(
            database,
            cls.window_names( website_names, encounters ),
            encounters,
            schedules,
            website_slots,
            first,
            last,
         ),
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      schedule = cls.schedule_check( database, today )
      CheckReport.report_schedule( 'wildEncounter', today, schedule )
      return (
         len( schedule.only_in_app )
         + len( schedule.only_on_website )
         + len( schedule.different_slots )
         + cls.unfixed_windows( schedule.windows )
      )


   @classmethod
   def main( cls ) -> int:
      args = cls.parse_args()

      if not args.database.exists():
         print(
            AppStringProvider.format( 'checks.couldNotFindDatabase' ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      try:
         issues = cls.check_schedules( args.database, DateValues.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( WildEncounterScheduleChecker.main() )
