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
from .booking_calendar import BookingCalendar
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .encounter_schedule_slots import EncounterScheduleSlots
from .encounter_schedule_table import EncounterScheduleTable
from .schedule_check import ScheduleCheck
from .schedule_slot import ScheduleSlot
from .schedule_slot_group import ScheduleSlotGroup
from .website_page import WebsitePage


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
         AppStringProvider.format( 'checks.categoryItem', item=name )
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
            AppStringProvider.format( 'checks.categoryItem', item=name ),
            CheckReport.detail_item( AppStringProvider.format(
               'checks.websiteSchedule',
               schedule=ScheduleSlotGroup.describe( website_slots.for_name( name ) ),
            ) ),
            CheckReport.detail_item( AppStringProvider.format(
               'checks.appSchedule',
               schedule=ScheduleSlotGroup.describe( app_slots.for_name( name ) ),
            ) ),
         ] ) )

      return lines


   @classmethod
   def window_lines(
         cls,
         names: list[ str ],
         encounters: list[ WildEncounterLink ],
         schedules: list[ WildEncounterSchedule ],
         first: date,
         last: date ) -> list[ str ]:
      lines = []

      for name in names:
         detail = cls.read_window_difference(
            WildEncounterLink.booking_link( name, encounters ),
            WildEncounterSchedule.dates( schedules, name, first, last ),
            first,
            last,
         )

         if detail == None:
            continue

         lines.append( cls.window_line( name, detail ) )

      return lines


   @classmethod
   def window_line( cls, name: str, detail: str ) -> str:
      return CheckReport.join_lines( [
         AppStringProvider.format( 'checks.categoryItem', item=name ),
         detail,
      ] )


   @classmethod
   def detail_line( cls, key: str, **params: object ) -> str:
      return CheckReport.detail_item( AppStringProvider.format( key, **params ) )


   @classmethod
   def date_line( cls, key: str, dates: list[ date ] ) -> str | None:
      if not dates:
         return None

      return cls.detail_line( key, dates=CheckReport.format_date_list( dates ) )


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
   def read_window_difference(
         cls,
         link: str,
         app_dates: list[ date ],
         first: date,
         last: date ) -> str | None:
      if link == '':
         return cls.detail_line( 'checks.noBookingLink' )

      try:
         booking_type = BookingCalendar.tour_id( WebsitePage.fetch_text( link ) )
      except RuntimeError as error:
         return cls.detail_line( 'checks.couldNotReadBookingPage', error=error )

      if booking_type == None:
         return cls.detail_line( 'checks.noTourId' )

      try:
         bookable = BookingCalendar.enabled_dates( booking_type, first, last )
      except ( RuntimeError, ValueError, KeyError, TypeError ) as error:
         return cls.detail_line( 'checks.couldNotReadBookingCalendar', error=error )

      return cls.date_mismatch( app_dates, bookable )


   @classmethod
   def comparison_note( cls, first: date, last: date ) -> str:
      return AppStringProvider.format(
         'checks.bookingDatesCompared',
         span=AppStringProvider.format(
            'format.dateRangeThrough',
            start=first.isoformat(),
            end=last.isoformat(),
         ),
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
      shared_names = website_names & app_names
      different_names = {
         name
         for name in shared_names
         if website_slots.for_name( name ) != current_app_slots.for_name( name )
      }
      first = today + timedelta( days=1 )
      last = today + timedelta( days=cls.BOOKING_HORIZON_DAYS )
      shared_name_list = sorted( shared_names, key=str.casefold )

      return ScheduleCheck(
         note=cls.comparison_note( first, last ),
         only_in_app=cls.names_only( app_names - website_names ),
         only_on_website=cls.names_only( website_names - app_names ),
         different_slots=cls.different_slot_lines(
            different_names,
            website_slots,
            current_app_slots,
         ),
         windows=cls.window_lines( shared_name_list, encounters, schedules, first, last ),
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      schedule = cls.schedule_check( database, today )
      CheckReport.report_schedule( 'wildEncounter', today, schedule )
      return CheckReport.count_schedule( schedule )


   @classmethod
   def main( cls ) -> int:
      args = cls.parse_args()

      if not args.database.exists():
         print(
            AppStringProvider.format(
               'checks.couldNotFindDatabase',
               database=args.database,
            ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      try:
         issues = cls.check_schedules( args.database, date.today() )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( WildEncounterScheduleChecker.main() )
