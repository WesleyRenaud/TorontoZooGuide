from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re

from .animal_detail_image import AnimalDetailImage
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.guardians.cancellations.guardians_talk_cancellation_input import GuardiansTalkCancellationInput
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from api.guardians.data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from api.guardians.data_access.guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from api.guardians.data_access.guardians_talk_occurrence_record import GuardiansTalkOccurrenceRecord
from api.guardians.data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from api.guardians.domain.guardians_talk_identity import GuardiansTalkIdentity
from api.guardians.scheduling.guardians_talk_occurrences_builder import GuardiansTalkOccurrencesBuilder
from api.models import GuardiansTalk, ScheduledOccurrence
from api.models.guardians_talk_linked_animal import GuardiansTalkLinkedAnimal
from api.request_connection_provider import RequestConnectionProvider
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from .check_report import CheckReport
from .date_patterns import DatePatterns
from .exhibit_name import ExhibitName
from .exhibit_region_colors import ExhibitRegionColors
from .guardians_talk_check import GuardiansTalkCheck
from .guardians_talk_detail_image import GuardiansTalkDetailImage
from .guardians_talk_listing import GuardiansTalkListing
from .guardians_talk_occurrences import GuardiansTalkOccurrences
from .loaded_guardians_talks import LoadedGuardiansTalks
from .paths import Paths
from .programme import Programme
from .programme_day import ProgrammeDay
from .programme_talk import ProgrammeTalk
from .schedule_slot import ScheduleSlot
from .website_page import WebsitePage
from .week_schedule import WeekSchedule


class GuardiansTalkComparison():
   PAGE = 'MeetTheGuardians'
   PROGRAMME_MARKER = '<div class="programme-schedule">'
   SECTION_SPLIT_RE = re.compile( r'(?is)<div class="cstrong">' )
   TALK_NAME_RE = re.compile( r'(?is)<div class="aname">(.*?)</div>' )
   TALK_LOCATION_RE = re.compile( r'(?is)<div class="talklocation">(.*?)</div>' )
   TALK_TIME_RE = re.compile( r'(?i)(\d{1,2}:\d{2}\s*[ap]m)' )


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
         first: date ) -> list[ ScheduledOccurrence ]:
      if schedule.schedule_end_date == None:
         return []

      end = date.fromisoformat( schedule.schedule_end_date )

      if end < first:
         return []

      return GuardiansTalkOccurrencesBuilder.build(
         [ schedule ],
         cls.cancellation_records( schedule, cancellations ),
         ( end - first ).days,
         start_date=first,
      )


   @classmethod
   def app_occurrences(
         cls,
         schedules: list[ GuardiansTalkScheduleRecord ],
         cancellations: list[ GuardiansTalkCancellationInput ],
         first: date ) -> GuardiansTalkOccurrences:
      occurrences = GuardiansTalkOccurrences()
      open_ended = {
         GuardiansTalkListing(
            name=schedule.name,
            location=schedule.location,
         )
         for schedule in schedules
         if schedule.schedule_end_date == None
      }

      for listing in open_ended:
         occurrences.add_listing( listing )

      for schedule in schedules:
         listing = GuardiansTalkListing(
            name=schedule.name,
            location=schedule.location,
         )

         if listing in open_ended:
            continue

         occurrences.add_scheduled(
            listing,
            cls.schedule_occurrences( schedule, cancellations, first ),
         )

      return occurrences


   @classmethod
   def load_animals( cls, database: Path ) -> list[ GuardiansTalkAnimalRecord ]:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         return GuardiansTalkAnimalProvider.fetch_records( connection )
      finally:
         RequestConnectionProvider.clear()
         connection.close()


   @classmethod
   def linked_animal(
         cls,
         identity: GuardiansTalkListing,
         animals: list[ GuardiansTalkAnimalRecord ] ) -> GuardiansTalkLinkedAnimal | None:
      return next(
         (
            GuardiansTalkLinkedAnimal( species=animal.species, exhibit=animal.exhibit )
            for animal in animals
            if animal.talk_name == identity.name and animal.location == identity.location
         ),
         None,
      )


   @classmethod
   def color_location( cls, location: str ) -> str:
      for name in cls.exhibit_names():
         if name.casefold() == location.casefold():
            return name

      return next(
         ExhibitRegionColors.exhibit_region( name )
         for name in cls.exhibit_names()
         if ExhibitName.key( name ).startswith( f'{ ExhibitName.key( location ) } ' )
      )


   @classmethod
   def label(
         cls,
         identity: GuardiansTalkListing,
         animal: GuardiansTalkLinkedAnimal | None = None ) -> str:
      location = animal.exhibit if animal != None else cls.color_location( identity.location )

      return AppStringProvider.format(
         'format.middleDotPair',
         first=identity.name,
         second=location,
      )


   @classmethod
   def talk_photo(
         cls,
         identity: GuardiansTalkListing,
         animal: GuardiansTalkLinkedAnimal | None = None ) -> str:
      if animal != None:
         photo = AnimalDetailImage.source( animal.exhibit, animal.species )

         if ( Paths.ROOT / photo ).is_file():
            return photo

      location = cls.color_location( identity.location )
      photo = GuardiansTalkDetailImage.source( location, identity.name )

      if ( Paths.ROOT / photo ).is_file():
         return photo

      return ''


   @classmethod
   def talk_line(
         cls,
         identity: GuardiansTalkListing,
         details: list[ str ] | None = None,
         animal: GuardiansTalkLinkedAnimal | None = None ) -> str:
      lines = [
         CheckReport.text( 'checks.categoryItem' ) + cls.label( identity, animal ),
      ]
      photo = cls.talk_photo( identity, animal )

      if photo != '':
         lines.append( CheckReport.detail_item(
            CheckReport.text( 'checks.photo' ) + photo
         ) )

      if details != None:
         lines.extend( details )

      return CheckReport.join_lines( lines )


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
   def week_schedule(
         cls,
         occurrences: set[ GuardiansTalkOccurrenceRecord ] ) -> WeekSchedule | None:
      return WeekSchedule.build(
         [
            date.fromisoformat( occurrence.occurrence_date )
            for occurrence in occurrences
         ],
         cls.slot_pairs( occurrences ),
      )


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
   def prepare( cls, database: Path, today: date ) -> GuardiansTalkCheck:
      loaded = cls.load_talks( database )
      programme = cls.parse_programme(
         WebsitePage.fetch_text( WebsitePage.url( cls.PAGE ) ),
         today,
      )
      compared_dates = [
         scheduled_date
         for scheduled_date in programme.dates
         if scheduled_date >= today
      ]
      upcoming_talks = [
         talk
         for talk in programme.talks
         if talk.scheduled_date >= today
      ]

      return GuardiansTalkCheck(
         note=cls.comparison_note( compared_dates, today ),
         website=cls.website_occurrences( upcoming_talks, loaded.talks ),
         app=cls.app_occurrences(
            loaded.schedules,
            loaded.cancellations,
            today,
         ),
         animals=cls.load_animals( database ),
         catalog={
            GuardiansTalkListing( name=talk.name, location=talk.location )
            for talk in loaded.talks
         },
      )
