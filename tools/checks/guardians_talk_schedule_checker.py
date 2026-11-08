from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.guardians.cancellations.guardians_talk_cancellation_input import GuardiansTalkCancellationInput
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.data_access.guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from api.guardians.data_access.guardians_talk_occurrence_record import GuardiansTalkOccurrenceRecord
from api.guardians.data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from api.guardians.domain.guardians_talk_identity import GuardiansTalkIdentity
from api.guardians.scheduling.guardians_talk_occurrences_builder import GuardiansTalkOccurrencesBuilder
from api.models import GuardiansTalk, ScheduledOccurrence
from api.request_connection_provider import RequestConnectionProvider
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .date_patterns import DatePatterns
from .exhibit_name import ExhibitName
from .guardians_talk_listing import GuardiansTalkListing
from .guardians_talk_occurrences import GuardiansTalkOccurrences
from .loaded_guardians_talks import LoadedGuardiansTalks
from .paths import Paths
from .programme import Programme
from .programme_day import ProgrammeDay
from .programme_talk import ProgrammeTalk
from .schedule_check import ScheduleCheck
from .schedule_slot import ScheduleSlot
from .schedule_slot_group import ScheduleSlotGroup
from .website_page import WebsitePage


class GuardiansTalkScheduleChecker():
   PAGE = 'MeetTheGuardians'
   PROGRAMME_MARKER = '<div class="programme-schedule">'
   SECTION_SPLIT_RE = re.compile( r'(?is)<div class="cstrong">' )
   TALK_NAME_RE = re.compile( r'(?is)<div class="aname">(.*?)</div>' )
   TALK_LOCATION_RE = re.compile( r'(?is)<div class="talklocation">(.*?)</div>' )
   TALK_TIME_RE = re.compile( r'(?i)(\d{1,2}:\d{2}\s*[ap]m)' )


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse(
         AppStringProvider.format( 'reports.guardiansTalk.description' )
      )


   @classmethod
   def parse_heading( cls, heading: str, today: date ) -> date:
      match = DatePatterns.MONTH_DAY_RE.search( heading )
      month = CalendarDates.month_index( match.group( 'month' ) )

      return CalendarDates.resolve_month_day(
         month,
         int( match.group( 'day' ) ),
         today,
      )


   @classmethod
   def programme_sections( cls, page_html: str ) -> list[ str ]:
      schedule = page_html[ page_html.find( cls.PROGRAMME_MARKER ): ]
      return cls.SECTION_SPLIT_RE.split( schedule )[ 1: ]


   @classmethod
   def parse_day( cls, section: str, today: date ) -> ProgrammeDay:
      heading, _, rest = section.partition( '</div>' )
      scheduled_date = cls.parse_heading( WebsitePage.clean_html( heading ), today )
      names = [
         WebsitePage.clean_html( name )
         for name in cls.TALK_NAME_RE.findall( rest )
      ]
      locations = [
         WebsitePage.clean_html( location )
         for location in cls.TALK_LOCATION_RE.findall( rest )
      ]
      times = [
         DateValues.normalize_schedule_time( talk_time )
         for talk_time in cls.TALK_TIME_RE.findall( rest )
      ]

      return ProgrammeDay(
         scheduled_date=scheduled_date,
         talks=[
            ProgrammeTalk(
               scheduled_date=scheduled_date,
               talk_time=talk_time,
               name=name,
               location=location,
            )
            for name, location, talk_time in zip( names, locations, times )
         ],
      )


   @classmethod
   def parse_programme( cls, page_html: str, today: date ) -> Programme:
      return Programme.from_days( [
         cls.parse_day( section, today )
         for section in cls.programme_sections( page_html )
      ] )


   @classmethod
   def load_talks( cls, database: Path ) -> LoadedGuardiansTalks:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return LoadedGuardiansTalks(
            talks=GuardiansCoordinator.get_guardians_talk_details(),
            schedules=GuardiansCoordinator.get_guardians_talk_schedule_records(),
            cancellations=GuardiansCoordinator.get_guardians_talk_cancellations(),
         )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def exhibit_names( cls ) -> list[ str ]:
      return [
         row[ 'name' ]
         for row in json.loads( Paths.EXHIBIT_DATA.read_text() )
      ]


   @classmethod
   def resolve_talk(
         cls,
         name: str,
         location: str,
         catalog: list[ GuardiansTalk ] ) -> GuardiansTalkListing:
      candidates = [
         talk
         for talk in catalog
         if WebsitePage.normalize_name( talk.name ) == WebsitePage.normalize_name( name )
      ]
      exhibit_keys = {
         ExhibitName.key( exhibit )
         for exhibit in ExhibitName.matching( location, cls.exhibit_names() )
      }

      if not exhibit_keys:
         exhibit_keys = { ExhibitName.key( location ) }

      located = [
         talk
         for talk in candidates
         if ExhibitName.key( talk.location ) in exhibit_keys
      ]

      if located:
         talk = min(
            located,
            key=lambda item: (
               item.name.casefold(),
               item.location.casefold(),
               item.name,
               item.location,
            ),
         )
         return GuardiansTalkListing(
            name=talk.name,
            location=talk.location,
         )

      return GuardiansTalkListing( name=name, location=location )


   @classmethod
   def website_occurrences(
         cls,
         talks: list[ ProgrammeTalk ],
         catalog: list[ GuardiansTalk ],
         ) -> GuardiansTalkOccurrences:
      occurrences = GuardiansTalkOccurrences()

      for talk in talks:
         occurrences.add(
            cls.resolve_talk( talk.name, talk.location, catalog ),
            talk.scheduled_date,
            talk.talk_time,
         )

      return occurrences


   @classmethod
   def cancellation_records(
         cls,
         schedule: GuardiansTalkScheduleRecord,
         cancellations: list[ GuardiansTalkCancellationInput ],
         ) -> list[ GuardiansTalkCancellationRecord ]:
      return [
         GuardiansTalkCancellationRecord(
            cancellation_date=cancellation.cancellation_date,
            talk_time=cancellation.talk_time,
         )
         for cancellation in cancellations
         if GuardiansTalkIdentity.matches(
            cancellation.talk_name,
            cancellation.location,
            cancellation.enclosure_name,
            other_talk_name=schedule.name,
            other_location=schedule.location,
            other_enclosure_name=schedule.enclosure_name,
         )
      ]


   @classmethod
   def schedule_occurrences(
         cls,
         schedule: GuardiansTalkScheduleRecord,
         cancellations: list[ GuardiansTalkCancellationInput ],
         window: set[ date ] ) -> list[ ScheduledOccurrence ]:
      if len( window ) == 0:
         return []

      start = min( window )
      built = GuardiansTalkOccurrencesBuilder.build(
         [ schedule ],
         cls.cancellation_records( schedule, cancellations ),
         ( max( window ) - start ).days,
         start_date=start,
      )

      return [
         occurrence
         for occurrence in built
         if date.fromisoformat( occurrence.date ) in window
      ]


   @classmethod
   def app_occurrences(
         cls,
         schedules: list[ GuardiansTalkScheduleRecord ],
         cancellations: list[ GuardiansTalkCancellationInput ],
         window: set[ date ],
         ) -> GuardiansTalkOccurrences:
      occurrences = GuardiansTalkOccurrences()

      for schedule in schedules:
         occurrences.add_scheduled(
            GuardiansTalkListing(
               name=schedule.name,
               location=schedule.location,
            ),
            cls.schedule_occurrences( schedule, cancellations, window ),
         )

      return occurrences


   @classmethod
   def label( cls, identity: GuardiansTalkListing ) -> str:
      return AppStringProvider.values()[ 'format.listJoin' ].join( [
         identity.name,
         identity.location,
      ] )


   @classmethod
   def names_only( cls, identities: set[ GuardiansTalkListing ] ) -> list[ str ]:
      return [
         CheckReport.text( 'checks.categoryItem' ) + cls.label( identity )
         for identity in sorted( identities, key=cls.label )
      ]


   @classmethod
   def slot_pairs(
         cls,
         occurrences: set[ GuardiansTalkOccurrenceRecord ] ) -> set[ ScheduleSlot ]:
      return {
         ScheduleSlot(
            weekday=date.fromisoformat( occurrence.occurrence_date ).weekday(),
            time=DateValues.parse_time_value( occurrence.talk_time ),
         )
         for occurrence in occurrences
      }


   @classmethod
   def different_slot_lines(
         cls,
         identities: set[ GuardiansTalkListing ],
         website: GuardiansTalkOccurrences,
         app: GuardiansTalkOccurrences ) -> list[ str ]:
      lines = []

      for identity in sorted( identities, key=cls.label ):
         lines.append( CheckReport.join_lines( [
            CheckReport.text( 'checks.categoryItem' ) + cls.label( identity ),
            CheckReport.detail_item(
               CheckReport.text( 'checks.websiteSchedule' )
               + ScheduleSlotGroup.describe(
                  cls.slot_pairs( website.for_listing( identity ) ),
               ),
            ),
            CheckReport.detail_item(
               CheckReport.text( 'checks.appSchedule' )
               + ScheduleSlotGroup.describe(
                  cls.slot_pairs( app.for_listing( identity ) ),
               ),
            ),
         ] ) )

      return lines


   @classmethod
   def window_lines(
         cls,
         identities: set[ GuardiansTalkListing ],
         website: GuardiansTalkOccurrences,
         app: GuardiansTalkOccurrences ) -> list[ str ]:
      lines = []

      for identity in sorted( identities, key=cls.label ):
         website_dates = {
            date.fromisoformat( occurrence.occurrence_date )
            for occurrence in website.for_listing( identity )
         }
         app_dates = {
            date.fromisoformat( occurrence.occurrence_date )
            for occurrence in app.for_listing( identity )
         }
         parts = [ CheckReport.text( 'checks.categoryItem' ) + cls.label( identity ) ]
         app_only = sorted( app_dates - website_dates )
         website_only = sorted( website_dates - app_dates )

         if app_only:
            parts.append( CheckReport.detail_item(
               CheckReport.text( 'checks.appDatesNotOnWebsite' )
               + CheckReport.format_date_list( app_only ),
            ) )

         if website_only:
            parts.append( CheckReport.detail_item(
               CheckReport.text( 'checks.websiteDatesNotInApp' )
               + CheckReport.format_date_list( website_only ),
            ) )

         if len( parts ) > 1:
            lines.append( CheckReport.join_lines( parts ) )

      return lines


   @classmethod
   def comparison_note( cls, compared_dates: list[ date ], today: date ) -> str:
      if compared_dates:
         return (
            CheckReport.text( 'checks.websiteDatesCompared' )
            + CheckReport.format_date_span( min( compared_dates ), max( compared_dates ) )
            + CheckReport.text( 'checks.period' )
         )

      return (
         CheckReport.text( 'checks.noWebsiteDatesAfter' )
         + today.isoformat()
         + CheckReport.text( 'checks.period' )
      )


   @classmethod
   def schedule_check( cls, database: Path, today: date ) -> ScheduleCheck:
      loaded = cls.load_talks( database )
      programme = cls.parse_programme( WebsitePage.fetch_text( WebsitePage.url( cls.PAGE ) ), today )
      compared_dates = [
         scheduled_date
         for scheduled_date in programme.dates
         if scheduled_date > today
      ]
      upcoming_talks = [
         talk
         for talk in programme.talks
         if talk.scheduled_date > today
      ]
      website = cls.website_occurrences( upcoming_talks, loaded.talks )
      app = cls.app_occurrences(
         loaded.schedules,
         loaded.cancellations,
         set( compared_dates ),
      )
      website_names = website.listings()
      app_names = app.listings()
      shared_names = website_names & app_names
      different_names = {
         identity
         for identity in shared_names
         if cls.slot_pairs( website.for_listing( identity ) ) != cls.slot_pairs( app.for_listing( identity ) )
      }

      return ScheduleCheck(
         note=cls.comparison_note( compared_dates, today ),
         only_in_app=cls.names_only( app_names - website_names ),
         only_on_website=cls.names_only( website_names - app_names ),
         different_slots=cls.different_slot_lines( different_names, website, app ),
         windows=cls.window_lines( shared_names, website, app ),
      )


   @classmethod
   def check_schedules( cls, database: Path, today: date ) -> int:
      schedule = cls.schedule_check( database, today )
      CheckReport.report_schedule( 'guardiansTalk', today, schedule )
      return CheckReport.count_schedule( schedule )


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
   raise SystemExit( GuardiansTalkScheduleChecker.main() )
