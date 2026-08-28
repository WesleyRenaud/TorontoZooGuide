from __future__ import annotations

from collections.abc import Callable
from datetime import date
from datetime import timedelta

from ..cancellations.guardians_talk_cancellation_builder import GuardiansTalkCancellationBuilder
from ..data_access.guardians_talk_cancellation_provider import GuardiansTalkCancellationProvider
from ..data_access.guardians_talk_day_schedule_provider import GuardiansTalkDayScheduleProvider
from ..data_access.guardians_talk_occurrence_provider import GuardiansTalkOccurrenceProvider
from ..data_access.guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from ..data_access.meet_the_guardians_talk_provider import MeetTheGuardiansTalkProvider
from ..domain.guardians_talk_builder import GuardiansTalkBuilder
from ..domain.guardians_talk_linked_animals_builder import GuardiansTalkLinkedAnimalsBuilder
from ...itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from ..itinerary.itinerary_guardians_talks_builder import ItineraryGuardiansTalksBuilder
from ...models import GuardiansTalk
from ...models import ScheduledOccurrence
from ..occurrences.guardians_talk_occurrence_builder import GuardiansTalkOccurrenceBuilder
from ...request_connection import get_connection
from ..scheduling.guardians_talk_day_schedule_builder import GuardiansTalkDayScheduleBuilder
from ..scheduling.guardians_talk_day_schedule_finder import GuardiansTalkDayScheduleFinder
from ..scheduling.guardians_talk_occurrences_builder import GuardiansTalkOccurrencesBuilder
from ..scheduling.guardians_talk_schedule_builder import GuardiansTalkScheduleBuilder
from ..scheduling.guardians_talk_schedule_conflict_resolver import GuardiansTalkScheduleConflictResolver
from ..scheduling.guardians_talk_schedule_end_builder import GuardiansTalkScheduleEndBuilder
from ..scheduling.guardians_talk_schedule_input import GuardiansTalkScheduleInput
from ..scheduling.guardians_talk_schedule_row_input import GuardiansTalkScheduleRowInput
from ..search.guardians_talks_matching_query_builder import GuardiansTalksMatchingQueryBuilder
from ...shared.api_error_response import ApiOperationFailure
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...shared.constants import SCHEDULED_OCCURRENCE_DAYS_AHEAD
from ...shared.enums.api_error_type import ApiErrorType
from ...types import Connection, DateInput, DateKey, MonthInput, VisitDay, VisitYear


class GuardiansCoordinator():
   @classmethod
   def _build_guardians_talk_schedules(
         cls,
         talk: str,
         location: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str,
         *,
         schedule_rows: list[ dict[ str, object ] ] | None = None ) -> list[ GuardiansTalkScheduleInput ]:
      resolved_schedule_rows = GuardiansTalkScheduleRowInput.parse_rows( schedule_rows )

      return [
         GuardiansTalkScheduleBuilder.build(
            talk=talk,
            location=location,
            start_date=start_date,
            end_date=end_date,
            talk_time=schedule_row.talk_time,
            monday=schedule_row.monday,
            tuesday=schedule_row.tuesday,
            wednesday=schedule_row.wednesday,
            thursday=schedule_row.thursday,
            friday=schedule_row.friday,
            saturday=schedule_row.saturday,
            sunday=schedule_row.sunday,
            message=message )
         for schedule_row in resolved_schedule_rows
      ]


   @classmethod
   def _save_guardians_talk_schedules(
         cls,
         schedules: list[ GuardiansTalkScheduleInput ],
         *,
         save_schedule: Callable[ [ Connection, GuardiansTalkScheduleInput ], bool ] ) -> bool:
      if not schedules:
         return False

      conn = get_connection()

      for schedule in schedules:
         if not save_schedule( conn, schedule ):
            return False

      return True


   @classmethod
   def get_guardians_talk_locations( cls ) -> list[ str ]:
      return MeetTheGuardiansTalkProvider.fetch_guardians_talk_locations( get_connection() )


   @classmethod
   def get_guardians_talk_names( cls ) -> list[ str ]:
      return MeetTheGuardiansTalkProvider.fetch_guardians_talk_names( get_connection() )


   @classmethod
   def get_guardians_talk_names_at_location( cls, location: str ) -> list[ str ]:
      return MeetTheGuardiansTalkProvider.fetch_guardians_talk_names_at_location(
         get_connection(),
         location=location )


   @classmethod
   def get_guardians_talk_occurrences(
         cls,
         talk: str,
         location: str,
         days_ahead: int = SCHEDULED_OCCURRENCE_DAYS_AHEAD ) -> list[ ScheduledOccurrence ]:
      conn = get_connection()
      schedule_records = GuardiansTalkScheduleProvider.fetch_schedule_records_for_occurrences(
         conn,
         talk_name=talk,
         location=location )
      cancellation_records = GuardiansTalkCancellationProvider.fetch_cancellation_records(
         conn,
         talk_name=talk,
         location=location )
      today = DateValues.parse_date_value( DateValues.today_date_key() )
      occurrence_records = GuardiansTalkOccurrenceProvider.fetch_occurrence_records(
         conn,
         talk_name=talk,
         location=location,
         start_date=today.isoformat(),
         end_date=( today + timedelta( days=days_ahead ) ).isoformat() )

      return GuardiansTalkOccurrencesBuilder.build(
         schedule_records=schedule_records,
         cancellation_records=cancellation_records,
         days_ahead=days_ahead,
         occurrence_records=occurrence_records )


   @classmethod
   def get_guardians_talk_details(
         cls,
         guardians_talks_to_include: list[ str ] | None = None ) -> list[ GuardiansTalk ]:
      talk_records = MeetTheGuardiansTalkProvider.fetch_meet_the_guardians_talk_records( get_connection() )

      return GuardiansTalkBuilder.build_details(
         talk_records,
         guardians_talks_to_include=guardians_talks_to_include )


   @classmethod
   def set_guardians_talk_schedule(
         cls,
         talk: str,
         location: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str = '',
         *,
         schedule_rows: list[ dict[ str, object ] ] | None = None ) -> bool:
      schedules = cls._build_guardians_talk_schedules(
         talk,
         location,
         start_date,
         end_date,
         message,
         schedule_rows=schedule_rows )

      return cls._save_guardians_talk_schedules(
         schedules,
         save_schedule=GuardiansTalkScheduleProvider.save_schedule )


   @classmethod
   def replace_guardians_talk_schedule_overlaps(
         cls,
         talk: str,
         location: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str = '',
         *,
         schedule_rows: list[ dict[ str, object ] ] | None = None ) -> bool:
      schedules = cls._build_guardians_talk_schedules(
         talk,
         location,
         start_date,
         end_date,
         message,
         schedule_rows=schedule_rows )

      return cls._save_guardians_talk_schedules(
         schedules,
         save_schedule=GuardiansTalkScheduleConflictResolver.save_replacing_overlaps )


   @classmethod
   def trim_guardians_talk_schedule_overlaps(
         cls,
         talk: str,
         location: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str = '',
         *,
         schedule_rows: list[ dict[ str, object ] ] | None = None ) -> bool:
      schedules = cls._build_guardians_talk_schedules(
         talk,
         location,
         start_date,
         end_date,
         message,
         schedule_rows=schedule_rows )

      return cls._save_guardians_talk_schedules(
         schedules,
         save_schedule=GuardiansTalkScheduleConflictResolver.save_trimming_overlaps )


   @classmethod
   def get_guardians_talk_schedule_times(
         cls,
         talk: str,
         location: str ) -> list[ str ]:
      schedule_times = GuardiansTalkScheduleProvider.fetch_schedule_times(
         get_connection(),
         talk_name=talk,
         location=location,
         target_date=DateValues.today_date_key() )

      return sorted(
         schedule_times,
         key=DateValues.time_value_in_seconds )


   @classmethod
   def end_guardians_talk_schedule(
         cls,
         talk: str,
         location: str,
         schedule_end_date: DateInput,
         talk_times: list[ str ] ) -> bool:
      for talk_time in DateValues.normalize_unique_schedule_times(
            talk_times ):
         schedule_end = GuardiansTalkScheduleEndBuilder.build(
            talk=talk,
            location=location,
            schedule_end_date=schedule_end_date,
            talk_time=talk_time )

         if not GuardiansTalkScheduleProvider.save_schedule_end(
               get_connection(),
               schedule_end=schedule_end ):
            return False

      return True


   @classmethod
   def cancel_guardians_talk_occurrence(
         cls,
         talk: str,
         location: str,
         date: DateKey,
         talk_times: list[ str ] ) -> bool:
      for talk_time in DateValues.normalize_unique_schedule_times(
            talk_times ):
         cancellation = GuardiansTalkCancellationBuilder.build(
            talk=talk,
            location=location,
            date=date,
            time=talk_time )

         if not GuardiansTalkCancellationProvider.save_cancellation(
               get_connection(),
               cancellation=cancellation ):
            return False

      return True


   @classmethod
   def add_guardians_talk_occurrence(
         cls,
         talk: str,
         location: str,
         date: DateKey,
         talk_times: list[ str ] ) -> tuple[ bool, ApiOperationFailure | None ]:
      conn = get_connection()

      for talk_time in DateValues.normalize_unique_schedule_times(
            talk_times ):
         occurrence = GuardiansTalkOccurrenceBuilder.build(
            talk=talk,
            location=location,
            date=date,
            time=talk_time )

         if GuardiansTalkOccurrenceProvider.occurrence_exists(
               conn,
               occurrence.talk_name,
               occurrence.location,
               occurrence.occurrence_date,
               occurrence.talk_time ):
            return (
               False,
               ApiOperationFailure(
                  error_type=(
                     ApiErrorType.GUARDIANS_TALK_OCCURRENCE_ALREADY_EXISTS ),
                  params={
                     'talk': occurrence.talk_name,
                     'location': occurrence.location,
                     'date': occurrence.occurrence_date,
                     'talkTime': occurrence.talk_time,
                  } ) )

         if not GuardiansTalkOccurrenceProvider.save_occurrence(
               conn,
               occurrence=occurrence ):
            return (
               False,
               ApiOperationFailure(
                  error_type=ApiErrorType.COULD_NOT_ADD_GUARDIANS_TALK_OCCURRENCE,
                  params={
                     'talk': talk,
                     'location': location,
                     'date': date,
                  } ) )

      return True, None


   @classmethod
   def get_guardians_talks_for_saved_itinerary(
         cls,
         saved_guardians_talks: list[ ItineraryGuardiansTalkRecord ] ) -> list[ GuardiansTalk ]:
      if not saved_guardians_talks:
         return []

      guardians_talk_names = [
         saved_talk.talk_name
         for saved_talk in saved_guardians_talks
      ]

      guardians_talks = cls.get_guardians_talk_details(
         guardians_talk_names )
      itinerary_talks = ItineraryGuardiansTalksBuilder.build(
         guardians_talks,
         saved_guardians_talks )

      return GuardiansTalkLinkedAnimalsBuilder.attach(
         get_connection(),
         itinerary_talks )


   @classmethod
   def get_guardians_talk_schedule(
         cls,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ GuardiansTalk ]:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )

      return cls.get_guardians_talk_schedule_for_target_date( target_date )


   @classmethod
   def get_guardians_talks_matching_query(
         cls,
         query: str,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ GuardiansTalk ]:
      guardians_talks = cls.get_guardians_talk_schedule(
         month=month,
         day=day,
         year=year )

      return GuardiansTalksMatchingQueryBuilder.build(
         guardians_talks,
         query )


   @classmethod
   def get_guardians_talk_on_day_schedule(
         cls,
         month: MonthInput,
         day: VisitDay,
         talk_name: str,
         year: VisitYear,
         *,
         start_time: str,
         day_schedule: list[ GuardiansTalk ] | None = None ) -> GuardiansTalk | None:
      rows = (
         day_schedule
         if day_schedule is not None
         else cls.get_guardians_talk_schedule(
            month=month,
            day=day,
            year=year )
      )

      return GuardiansTalkDayScheduleFinder.find_on_day_schedule(
         rows,
         talk_name,
         start_time=start_time )


   @classmethod
   def get_guardians_talk_schedule_for_target_date(
         cls,
         target_date: date ) -> list[ GuardiansTalk ]:
      records = GuardiansTalkDayScheduleProvider.fetch_day_schedule_records(
         get_connection(),
         target_date.isoformat() )
      guardians_talks = GuardiansTalkDayScheduleBuilder.build_from_records(
         records )

      return GuardiansTalkLinkedAnimalsBuilder.attach(
         get_connection(),
         guardians_talks )
