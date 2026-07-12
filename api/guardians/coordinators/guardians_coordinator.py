from __future__ import annotations

from collections.abc import Callable
from datetime import date

from ..cancellations.guardians_talk_cancellation_status import build_guardians_talk_cancellation
from ..data_access.guardians_talk import fetch_guardians_talk_locations
from ..data_access.guardians_talk import fetch_guardians_talk_names
from ..data_access.guardians_talk import fetch_guardians_talk_names_at_location
from ..data_access.guardians_talk import fetch_meet_the_guardians_talk_records
from ..data_access.guardians_talk_cancellation import save_guardians_talk_cancellation
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_cancellation_records
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_occurrence_is_cancelled
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_records
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_records_for_occurrences
from ..data_access.guardians_talk_schedule import fetch_guardians_talk_schedule_times
from ..data_access.guardians_talk_schedule import save_guardians_talk_schedule
from ..data_access.guardians_talk_schedule import save_guardians_talk_schedule_end
from ..domain.guardians_talk import build_guardians_talk_details
from ...itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from ..itinerary.itinerary_guardians_talks import build_itinerary_guardians_talks
from ...models import GuardiansTalk
from ...models import ScheduledOccurrence
from ...request_connection import get_connection
from ..scheduling.guardians_talk_occurrences import build_guardians_talk_occurrences
from ..scheduling.guardians_talk_schedule import build_guardians_talk_schedule_for_target_date
from ..scheduling.guardians_talk_schedule import find_guardians_talk_on_day_schedule
from ..scheduling.guardians_talk_schedule_conflict_resolution import save_guardians_talk_schedule_replacing_overlaps
from ..scheduling.guardians_talk_schedule_conflict_resolution import save_guardians_talk_schedule_trimming_overlaps
from ..scheduling.guardians_talk_schedule_ending import build_guardians_talk_schedule_end
from ..scheduling.guardians_talk_schedule_input import GuardiansTalkScheduleInput
from ..scheduling.guardians_talk_schedule_row_input import parse_guardians_talk_schedule_rows
from ..scheduling.guardians_talk_schedule_status import build_guardians_talk_schedule
from ..search.guardians_talks_matching_query import build_guardians_talks_matching_query
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...shared.constants import SCHEDULED_OCCURRENCE_DAYS_AHEAD
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
      resolved_schedule_rows = parse_guardians_talk_schedule_rows( schedule_rows )

      return [
         build_guardians_talk_schedule(
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
      return fetch_guardians_talk_locations( get_connection() )


   @classmethod
   def get_guardians_talk_names( cls ) -> list[ str ]:
      return fetch_guardians_talk_names( get_connection() )


   @classmethod
   def get_guardians_talk_names_at_location( cls, location: str ) -> list[ str ]:
      return fetch_guardians_talk_names_at_location(
         get_connection(),
         location=location )


   @classmethod
   def get_guardians_talk_occurrences(
         cls,
         talk: str,
         location: str,
         days_ahead: int = SCHEDULED_OCCURRENCE_DAYS_AHEAD ) -> list[ ScheduledOccurrence ]:
      schedule_records = fetch_guardians_talk_schedule_records_for_occurrences(
         get_connection(),
         talk_name=talk,
         location=location )
      cancellation_records = fetch_guardians_talk_cancellation_records(
         get_connection(),
         talk_name=talk,
         location=location )

      return build_guardians_talk_occurrences(
         schedule_records=schedule_records,
         cancellation_records=cancellation_records,
         days_ahead=days_ahead )


   @classmethod
   def get_guardians_talk_details(
         cls,
         guardians_talks_to_include: list[ str ] | None = None ) -> list[ GuardiansTalk ]:
      talk_records = fetch_meet_the_guardians_talk_records( get_connection() )

      return build_guardians_talk_details(
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
         save_schedule=save_guardians_talk_schedule )


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
         save_schedule=save_guardians_talk_schedule_replacing_overlaps )


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
         save_schedule=save_guardians_talk_schedule_trimming_overlaps )


   @classmethod
   def get_guardians_talk_schedule_times(
         cls,
         talk: str,
         location: str ) -> list[ str ]:
      schedule_times = fetch_guardians_talk_schedule_times(
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
         schedule_end = build_guardians_talk_schedule_end(
            talk=talk,
            location=location,
            schedule_end_date=schedule_end_date,
            talk_time=talk_time )

         if not save_guardians_talk_schedule_end(
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
         cancellation = build_guardians_talk_cancellation(
            talk=talk,
            location=location,
            date=date,
            time=talk_time )

         if not save_guardians_talk_cancellation(
               get_connection(),
               cancellation=cancellation ):
            return False

      return True


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

      return build_itinerary_guardians_talks(
         guardians_talks,
         saved_guardians_talks )


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

      return build_guardians_talks_matching_query(
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

      return find_guardians_talk_on_day_schedule(
         rows,
         talk_name,
         start_time=start_time )


   @classmethod
   def _guardians_talk_occurrence_is_cancelled(
         cls,
         talk_name: str,
         location: str,
         cancellation_date: DateKey,
         talk_time: str | None ) -> bool:
      return fetch_guardians_talk_occurrence_is_cancelled(
         get_connection(),
         talk_name,
         location,
         cancellation_date,
         talk_time )


   @classmethod
   def get_guardians_talk_schedule_for_target_date(
         cls,
         target_date: date ) -> list[ GuardiansTalk ]:
      records = fetch_guardians_talk_schedule_records( get_connection() )

      return build_guardians_talk_schedule_for_target_date(
         records,
         target_date,
         cls._guardians_talk_occurrence_is_cancelled )
