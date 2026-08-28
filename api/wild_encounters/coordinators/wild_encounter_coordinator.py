from __future__ import annotations

from collections.abc import Callable

from ..cancellations.wild_encounter_cancellation_builder import WildEncounterCancellationBuilder
from ..data_access.wild_encounter_cancellation_provider import WildEncounterCancellationProvider
from ..data_access.wild_encounter_provider import WildEncounterProvider
from ..data_access.wild_encounter_schedule_provider import WildEncounterScheduleProvider
from ..domain.wild_encounter_builder import WildEncounterBuilder
from ...itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ..itinerary.itinerary_wild_encounters_builder import ItineraryWildEncountersBuilder
from ...models import ScheduledOccurrence
from ...models import WildEncounter
from ...request_connection import get_connection
from ..scheduling.wild_encounter_day_schedule_builder import WildEncounterDayScheduleBuilder
from ..scheduling.wild_encounter_day_schedule_finder import WildEncounterDayScheduleFinder
from ..scheduling.wild_encounter_occurrences_builder import WildEncounterOccurrencesBuilder
from ..scheduling.wild_encounter_schedule_builder import WildEncounterScheduleBuilder
from ..scheduling.wild_encounter_schedule_conflict_resolver import WildEncounterScheduleConflictResolver
from ..scheduling.wild_encounter_schedule_end_builder import WildEncounterScheduleEndBuilder
from ..scheduling.wild_encounter_schedule_input import WildEncounterScheduleInput
from ..scheduling.wild_encounter_schedule_row_input import WildEncounterScheduleRowInput
from ..search.wild_encounters_matching_query_builder import WildEncountersMatchingQueryBuilder
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...shared.constants import SCHEDULED_OCCURRENCE_DAYS_AHEAD
from ...types import Connection, DateInput, DateKey, MonthInput, VisitDay, VisitYear


class WildEncounterCoordinator():
   @classmethod
   def _build_wild_encounter_schedules(
         cls,
         wild_encounter_name: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str,
         *,
         schedule_rows: list[ dict[ str, object ] ] | None = None ) -> list[ WildEncounterScheduleInput ]:
      resolved_schedule_rows = WildEncounterScheduleRowInput.parse_rows( schedule_rows )

      return [
         WildEncounterScheduleBuilder.build(
            wild_encounter=wild_encounter_name,
            start_date=start_date,
            end_date=end_date,
            encounter_time=schedule_row.encounter_time,
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
   def _save_wild_encounter_schedules(
         cls,
         schedules: list[ WildEncounterScheduleInput ],
         *,
         save_schedule: Callable[ [ Connection, WildEncounterScheduleInput ], bool ] ) -> bool:
      if not schedules:
         return False

      conn = get_connection()

      for schedule in schedules:
         if not save_schedule( conn, schedule ):
            return False

      return True


   @classmethod
   def get_wild_encounter_names( cls ) -> list[ str ]:
      return WildEncounterProvider.fetch_wild_encounter_names( get_connection() )


   @classmethod
   def get_wild_encounter_occurrences(
         cls,
         wild_encounter_name: str,
         days_ahead: int = SCHEDULED_OCCURRENCE_DAYS_AHEAD ) -> list[ ScheduledOccurrence ]:
      conn = get_connection()
      schedule_records = WildEncounterScheduleProvider.fetch_schedule_records_for_occurrences(
         conn,
         wild_encounter=wild_encounter_name )
      cancellation_records = WildEncounterCancellationProvider.fetch_cancellation_records(
         conn,
         wild_encounter=wild_encounter_name )

      return WildEncounterOccurrencesBuilder.build(
         schedule_records=schedule_records,
         cancellation_records=cancellation_records,
         days_ahead=days_ahead )


   @classmethod
   def get_wild_encounter_details(
         cls,
         wild_encounters_to_include: list[ str ] | None = None ) -> list[ WildEncounter ]:
      wild_encounter_records = WildEncounterProvider.fetch_wild_encounter_records( get_connection() )

      return WildEncounterBuilder.build_details(
         wild_encounter_records,
         wild_encounters_to_include=wild_encounters_to_include )


   @classmethod
   def set_wild_encounter_schedule(
         cls,
         wild_encounter_name: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str = '',
         *,
         schedule_rows: list[ dict[ str, object ] ] | None = None ) -> bool:
      schedules = cls._build_wild_encounter_schedules(
         wild_encounter_name,
         start_date,
         end_date,
         message,
         schedule_rows=schedule_rows )

      return cls._save_wild_encounter_schedules(
         schedules,
         save_schedule=WildEncounterScheduleProvider.save_schedule )


   @classmethod
   def replace_wild_encounter_schedule_overlaps(
         cls,
         wild_encounter_name: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str = '',
         *,
         schedule_rows: list[ dict[ str, object ] ] | None = None ) -> bool:
      schedules = cls._build_wild_encounter_schedules(
         wild_encounter_name,
         start_date,
         end_date,
         message,
         schedule_rows=schedule_rows )

      return cls._save_wild_encounter_schedules(
         schedules,
         save_schedule=WildEncounterScheduleConflictResolver.save_replacing_overlaps )


   @classmethod
   def trim_wild_encounter_schedule_overlaps(
         cls,
         wild_encounter_name: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str = '',
         *,
         schedule_rows: list[ dict[ str, object ] ] | None = None ) -> bool:
      schedules = cls._build_wild_encounter_schedules(
         wild_encounter_name,
         start_date,
         end_date,
         message,
         schedule_rows=schedule_rows )

      return cls._save_wild_encounter_schedules(
         schedules,
         save_schedule=WildEncounterScheduleConflictResolver.save_trimming_overlaps )


   @classmethod
   def get_wild_encounter_schedule_times(
         cls,
         wild_encounter_name: str ) -> list[ str ]:
      schedule_times = WildEncounterScheduleProvider.fetch_schedule_times(
         get_connection(),
         wild_encounter=wild_encounter_name,
         target_date=DateValues.today_date_key() )

      return sorted(
         schedule_times,
         key=DateValues.time_value_in_seconds )


   @classmethod
   def end_wild_encounter_schedule(
         cls,
         wild_encounter_name: str,
         schedule_end_date: DateInput,
         encounter_times: list[ str ] ) -> bool:
      for encounter_time in DateValues.normalize_unique_schedule_times(
            encounter_times ):
         schedule_end = WildEncounterScheduleEndBuilder.build(
            wild_encounter=wild_encounter_name,
            schedule_end_date=schedule_end_date,
            encounter_time=encounter_time )

         if not WildEncounterScheduleProvider.save_schedule_end(
               get_connection(),
               schedule_end=schedule_end ):
            return False

      return True


   @classmethod
   def cancel_wild_encounter_occurrence(
         cls,
         wild_encounter_name: str,
         date: DateKey,
         encounter_times: list[ str ] ) -> bool:
      for encounter_time in DateValues.normalize_unique_schedule_times(
            encounter_times ):
         cancellation = WildEncounterCancellationBuilder.build(
            wild_encounter=wild_encounter_name,
            date=date,
            time=encounter_time )

         if not WildEncounterCancellationProvider.save_cancellation(
               get_connection(),
               cancellation=cancellation ):
            return False

      return True


   @classmethod
   def get_wild_encounters_for_saved_itinerary(
         cls,
         saved_wild_encounters: list[ ItineraryWildEncounterRecord ] ) -> list[ WildEncounter ]:
      if not saved_wild_encounters:
         return []

      wild_encounter_names = [
         saved_encounter.wild_encounter
         for saved_encounter in saved_wild_encounters
      ]

      wild_encounters = cls.get_wild_encounter_details(
         wild_encounter_names )

      return ItineraryWildEncountersBuilder.build(
         wild_encounters,
         saved_wild_encounters )


   @classmethod
   def get_wild_encounter_schedule(
         cls,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ WildEncounter ]:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )

      records = WildEncounterScheduleProvider.fetch_schedule_records(
         get_connection(),
         target_date )

      return WildEncounterDayScheduleBuilder.build_for_target_date(
         records,
         target_date )


   @classmethod
   def get_wild_encounter_on_day_schedule(
         cls,
         month: MonthInput,
         day: VisitDay,
         encounter_name: str,
         year: VisitYear,
         *,
         start_time: str,
         day_schedule: list[ WildEncounter ] | None = None ) -> WildEncounter | None:
      rows = (
         day_schedule
         if day_schedule is not None
         else cls.get_wild_encounter_schedule(
            month=month,
            day=day,
            year=year )
      )

      return WildEncounterDayScheduleFinder.find_on_day_schedule(
         rows,
         encounter_name,
         start_time=start_time )


   @classmethod
   def get_available_wild_encounters(
         cls,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ WildEncounter ]:
      return WildEncounterDayScheduleBuilder.filter_available(
         cls.get_wild_encounter_schedule(
            month=month,
            day=day,
            year=year ) )


   @classmethod
   def get_wild_encounters_matching_query(
         cls,
         query: str,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ WildEncounter ]:
      wild_encounters = cls.get_available_wild_encounters(
         month=month,
         day=day,
         year=year )

      return WildEncountersMatchingQueryBuilder.build(
         wild_encounters,
         query )
