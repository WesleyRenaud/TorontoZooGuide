from __future__ import annotations

from datetime import date
from pathlib import Path

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.data_access.wild_encounter_provider import WildEncounterProvider
from api.wild_encounters.data_access.wild_encounter_record import WildEncounterRecord
from api.wild_encounters.domain.wild_encounter_link import WildEncounterLink
from api.wild_encounters.domain.wild_encounter_schedule import WildEncounterSchedule
from .bookable_dates import BookableDates
from .booking_calendar import BookingCalendar
from .check_report import CheckReport
from .encounter_schedule_table import EncounterScheduleTable
from .encounter_website_card import EncounterWebsiteCard
from .paths import Paths
from .schedule_slot import ScheduleSlot
from .website_page import WebsitePage
from .week_schedule import WeekSchedule
from .wild_encounter_check import WildEncounterCheck
from .wild_encounter_detail_image import WildEncounterDetailImage


class WildEncounterComparison():
   PAGE = 'wildencounters'


   @classmethod
   def load_records( cls, database: Path ) -> list[ WildEncounterRecord ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return WildEncounterProvider.fetch_wild_encounter_records( connection )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def links( cls, records: list[ WildEncounterRecord ] ) -> list[ WildEncounterLink ]:
      return [
         WildEncounterLink( name=record.name, link=record.link or '' )
         for record in records
      ]


   @classmethod
   def region_for( cls, name: str, records: list[ WildEncounterRecord ] ) -> str:
      return next( record.region for record in records if record.name == name )


   @classmethod
   def encounter_line(
         cls,
         name: str,
         region: str,
         details: list[ str ] | None = None ) -> str:
      lines = [
         CheckReport.text( 'checks.categoryItem' ) + AppStringProvider.format(
            'format.middleDotPair',
            first=name,
            second=region,
         ),
      ]
      photo = WildEncounterDetailImage.source( name )

      if ( Paths.ROOT / photo ).is_file():
         lines.append( CheckReport.detail_item(
            CheckReport.text( 'checks.photo' ) + photo
         ) )

      if details != None:
         lines.extend( details )

      return CheckReport.join_lines( lines )


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
   def scheduled_names(
         cls,
         schedules: list[ WildEncounterSchedule ],
         first: date ) -> set[ str ]:
      open_ended = {
         schedule.name
         for schedule in schedules
         if schedule.start != None and schedule.end == None
      }
      names = set( open_ended )

      for name in { schedule.name for schedule in schedules } - open_ended:
         last = cls.last_scheduled_day( schedules, name )

         if last == None or last < first:
            continue

         if WildEncounterSchedule.dates( schedules, name, first, last ) != []:
            names.add( name )

      return names


   @classmethod
   def website_only_line( cls, name: str, image: str ) -> str:
      line = CheckReport.text( 'checks.categoryItem' ) + name

      if image == '':
         return line

      return CheckReport.join_lines( [
         line,
         CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + image ),
      ] )


   @classmethod
   def last_scheduled_day(
         cls,
         schedules: list[ WildEncounterSchedule ],
         name: str ) -> date | None:
      days = [
         schedule.last_day()
         for schedule in schedules
         if schedule.name == name and schedule.start != None
      ]

      if days == [] or None in days:
         return None

      return max( day for day in days if day != None )


   @classmethod
   def app_schedule(
         cls,
         schedules: list[ WildEncounterSchedule ],
         name: str,
         first: date ) -> WeekSchedule | None:
      last = cls.last_scheduled_day( schedules, name )

      if last == None or last < first:
         return None

      dates = WildEncounterSchedule.dates( schedules, name, first, last )
      return WeekSchedule.build( dates, cls.window_slots( schedules, name, dates ) )


   @classmethod
   def window_slots(
         cls,
         schedules: list[ WildEncounterSchedule ],
         name: str,
         days: list[ date ] ) -> set[ ScheduleSlot ]:
      slots: set[ ScheduleSlot ] = set()

      for day in days:
         for schedule in schedules:
            if schedule.name != name or not schedule.covers( day ):
               continue

            if day.weekday() not in schedule.weekday_indexes():
               continue

            parsed = DateValues.parse_time_value( schedule.encounter_time )

            if parsed == None:
               continue

            for index in schedule.weekday_indexes():
               slots.add( ScheduleSlot( weekday=index, time=parsed ) )

            break

      return slots


   @classmethod
   def detail_line( cls, key: str, value: str = '' ) -> str:
      return CheckReport.detail_item( CheckReport.text( key ) + value )


   @classmethod
   def website_schedule(
         cls,
         name: str,
         prepared: WildEncounterCheck ) -> BookableDates:
      booking = cls.read_bookable(
         WildEncounterLink.booking_link( name, prepared.encounters ),
         prepared.first,
      )

      if booking.failure != None:
         return booking

      return BookableDates(
         dates=booking.dates,
         failure=None,
         schedule=WeekSchedule.build(
            booking.dates,
            prepared.website_slots.for_name( name ),
         ),
      )


   @classmethod
   def read_bookable( cls, link: str, first: date ) -> BookableDates:
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
            dates=BookingCalendar.enabled_dates_from( booking_type, first ),
            failure=None,
         )
      except ( RuntimeError, ValueError, KeyError, TypeError ):
         return BookableDates( dates=[], failure=cls.detail_line( 'checks.couldNotReadBookingCalendar' ) )


   @classmethod
   def comparison_note( cls, first: date ) -> str:
      return (
         CheckReport.text( 'checks.bookingDatesCompared' )
         + first.isoformat()
         + CheckReport.text( 'checks.period' )
      )


   @classmethod
   def prepare( cls, database: Path, today: date ) -> WildEncounterCheck:
      records = cls.load_records( database )
      encounters = cls.links( records )
      schedules = cls.load_schedules( database )
      page_html = WebsitePage.fetch_text( WebsitePage.url( cls.PAGE ) )
      website_slots = EncounterScheduleTable.resolve(
         EncounterScheduleTable.parse( page_html ),
         encounters,
      )
      first = today

      return WildEncounterCheck(
         note=cls.comparison_note( first ),
         records=records,
         encounters=encounters,
         schedules=schedules,
         website_slots=website_slots,
         images=EncounterWebsiteCard.images( page_html ),
         app_names=cls.scheduled_names( schedules, first ),
         website_names=website_slots.names(),
         first=first,
      )
