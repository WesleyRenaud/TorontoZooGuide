from __future__ import annotations

from ..cancellations.wild_encounter_cancellation_status import build_wild_encounter_cancellation
from ..data_access.wild_encounter import fetch_wild_encounter_names
from ..data_access.wild_encounter import fetch_wild_encounter_records
from ..data_access.wild_encounter_cancellation import save_wild_encounter_cancellation
from ..data_access.wild_encounter_schedule import fetch_wild_encounter_cancellation_records
from ..data_access.wild_encounter_schedule import fetch_wild_encounter_schedule_records
from ..data_access.wild_encounter_schedule import fetch_wild_encounter_schedule_records_for_occurrences
from ..data_access.wild_encounter_schedule import fetch_wild_encounter_schedule_times
from ..data_access.wild_encounter_schedule import save_wild_encounter_schedule
from ..data_access.wild_encounter_schedule import save_wild_encounter_schedule_end
from ..domain.wild_encounter import build_wild_encounter_details
from ...itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ..itinerary.itinerary_wild_encounters import build_itinerary_wild_encounters
from ...models import ScheduledOccurrence
from ...models import WildEncounter
from ...request_connection import get_connection
from ..scheduling.wild_encounter_occurrences import build_wild_encounter_occurrences
from ..scheduling.wild_encounter_schedule import build_wild_encounter_schedule_for_target_date
from ..scheduling.wild_encounter_schedule import filter_available_wild_encounters
from ..scheduling.wild_encounter_schedule import find_wild_encounter_on_day_schedule
from ..scheduling.wild_encounter_schedule_ending import build_wild_encounter_schedule_end
from ..scheduling.wild_encounter_schedule_status import build_wild_encounter_schedule
from ..search.wild_encounters_matching_query import build_wild_encounters_matching_query
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...types import DateInput, DateKey, MonthInput, VisitDay, VisitYear


class WildEncounterCoordinator():
   @classmethod
   def get_wild_encounter_names( cls ) -> list[ str ]:
      return fetch_wild_encounter_names( get_connection() )


   @classmethod
   def get_wild_encounter_occurrences(
         cls,
         wild_encounter_name: str,
         days_ahead: int = 60 ) -> list[ ScheduledOccurrence ]:
      schedule_records = fetch_wild_encounter_schedule_records_for_occurrences(
         get_connection(),
         wild_encounter=wild_encounter_name )
      cancellation_records = fetch_wild_encounter_cancellation_records(
         get_connection(),
         wild_encounter=wild_encounter_name )

      return build_wild_encounter_occurrences(
         schedule_records=schedule_records,
         cancellation_records=cancellation_records,
         days_ahead=days_ahead )


   @classmethod
   def get_wild_encounter_details(
         cls,
         wild_encounters_to_include: list[ str ] | None = None ) -> list[ WildEncounter ]:
      wild_encounter_records = fetch_wild_encounter_records( get_connection() )

      return build_wild_encounter_details(
         wild_encounter_records,
         wild_encounters_to_include=wild_encounters_to_include )


   @classmethod
   def set_wild_encounter_schedule(
         cls,
         wild_encounter_name: str,
         start_date: DateInput,
         end_date: DateInput,
         encounter_times: list[ str ],
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         message: str ) -> bool:
      for encounter_time in DateValues.normalize_unique_schedule_times(
            encounter_times ):
         schedule = build_wild_encounter_schedule(
            wild_encounter=wild_encounter_name,
            start_date=start_date,
            end_date=end_date,
            encounter_time=encounter_time,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            message=message )

         if not save_wild_encounter_schedule(
               get_connection(),
               schedule=schedule ):
            return False

      return True


   @classmethod
   def get_wild_encounter_schedule_times(
         cls,
         wild_encounter_name: str ) -> list[ str ]:
      schedule_times = fetch_wild_encounter_schedule_times(
         get_connection(),
         wild_encounter=wild_encounter_name )

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
         schedule_end = build_wild_encounter_schedule_end(
            wild_encounter=wild_encounter_name,
            schedule_end_date=schedule_end_date,
            encounter_time=encounter_time )

         if not save_wild_encounter_schedule_end(
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
         cancellation = build_wild_encounter_cancellation(
            wild_encounter=wild_encounter_name,
            date=date,
            time=encounter_time )

         if not save_wild_encounter_cancellation(
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

      return build_itinerary_wild_encounters(
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

      records = fetch_wild_encounter_schedule_records(
         get_connection(),
         target_date )

      return build_wild_encounter_schedule_for_target_date(
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

      return find_wild_encounter_on_day_schedule(
         rows,
         encounter_name,
         start_time=start_time )


   @classmethod
   def get_available_wild_encounters(
         cls,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ WildEncounter ]:
      return filter_available_wild_encounters(
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

      return build_wild_encounters_matching_query(
         wild_encounters,
         query )
