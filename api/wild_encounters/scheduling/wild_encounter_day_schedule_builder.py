from __future__ import annotations

from datetime import date

from ...app_string_provider import AppStringProvider
from ..data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord
from ..domain.wild_encounter_sort_builder import WildEncounterSortBuilder
from ...models import WildEncounter
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues


class WildEncounterDayScheduleBuilder():
   @classmethod
   def build_for_target_date(
         cls,
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
               unavailable_message = AppStringProvider.format(
                  'guestStatus.visitDaySchedule.notScheduledOnVisitDay',
                  name=name,
                  month=target_date.strftime( '%B' ),
                  day=target_date.day )
            elif not weekday_ok:
               unavailable_message = AppStringProvider.format(
                  'guestStatus.visitDaySchedule.notOfferedThisWeekday',
                  name=name )
            elif record.is_cancelled:
               unavailable_message = AppStringProvider.format(
                  'guestStatus.visitDaySchedule.cancelledForThisDate',
                  name=name )

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

      WildEncounterSortBuilder.sort_by_name_and_start_time( wild_encounters )

      return wild_encounters


   @classmethod
   def filter_available(
         cls,
         wild_encounters: list[ WildEncounter ] ) -> list[ WildEncounter ]:
      return [
         wild_encounter
         for wild_encounter in wild_encounters
         if getattr( wild_encounter, 'is_available', True )
      ]
