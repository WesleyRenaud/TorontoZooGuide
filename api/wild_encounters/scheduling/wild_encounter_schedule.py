from __future__ import annotations

from datetime import date

from ..data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord
from ..domain.wild_encounter_name_filter import WildEncounterNameFilter
from ..domain.wild_encounter_sort import sort_wild_encounters_by_name_and_start_time
from ...models import WildEncounter
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ...shared.strings import SharedStrings
from ...types import ScheduleTimeKey


def find_wild_encounter_on_day_schedule(
      day_schedule: list[ WildEncounter ],
      encounter_name: str,
      *,
      start_time: ScheduleTimeKey,
   ) -> WildEncounter | None:
   encounter_filter = WildEncounterNameFilter( name=encounter_name )

   if encounter_filter.should_return_empty():
      return None

   normalized_start_time = DateValues.normalize_schedule_time(
      start_time )

   if normalized_start_time is None:
      return None

   for row in day_schedule:
      if not encounter_filter.allows_wild_encounter_name( row.name ):
         continue

      row_start_time = DateValues.normalize_schedule_time(
         row.start_time )

      if row_start_time == normalized_start_time:
         return row

   return None


def filter_available_wild_encounters(
      wild_encounters: list[ WildEncounter ] ) -> list[ WildEncounter ]:
   return [
      wild_encounter
      for wild_encounter in wild_encounters
      if getattr( wild_encounter, 'is_available', True )
   ]


def build_wild_encounter_schedule_for_target_date(
      records: list[ WildEncounterScheduleRecord ],
      target_date: date ) -> list[ WildEncounter ]:

   target_weekday = target_date.weekday()

   wild_encounters: list[ WildEncounter ] = []

   for record in records:
      name = record.name
      encounter_time = record.encounter_time

      date_range_ok = DateValues.is_date_in_range(
         target_date=target_date,
         start_date_value=record.schedule_start_date,
         end_date_value=record.schedule_end_date )
      unavailable_message: str | None = None

      weekday_ok = CalendarDates.schedule_includes_weekday(
         target_weekday,
         (
            record.monday,
            record.tuesday,
            record.wednesday,
            record.thursday,
            record.friday,
            record.saturday,
            record.sunday,
         ) )

      is_available = date_range_ok and weekday_ok and not record.is_cancelled

      if not is_available:
         if not date_range_ok:
            unavailable_message = SharedStrings.VisitDaySchedule.not_scheduled_on_visit_day(
               name,
               target_date )
         elif not weekday_ok:
            unavailable_message = SharedStrings.VisitDaySchedule.not_offered_this_weekday( name )
         elif record.is_cancelled:
            unavailable_message = SharedStrings.VisitDaySchedule.cancelled_for_this_date( name )

      encounter_end_time = DateValues.normalize_schedule_time(
         DateValues.add_minutes_to_time(
            encounter_time,
            record.maximum_duration ) )

      wild_encounters.append(
         WildEncounter(
            name=name,
            meeting_spot=record.meeting_spot,
            link=record.link,
            start_time=encounter_time,
            maximum_duration=record.maximum_duration,
            end_time=encounter_end_time,
            x_coord=record.x_coord,
            y_coord=record.y_coord,
            region=record.region,
            is_available=is_available,
            unavailable_message=unavailable_message ) )

   sort_wild_encounters_by_name_and_start_time( wild_encounters )

   return wild_encounters
