from __future__ import annotations

from datetime import timedelta

from ..data_access.wild_encounter_cancellation_record import WildEncounterCancellationRecord
from ..data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord
from ...models import ScheduledOccurrence
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues


def build_wild_encounter_occurrences(
      schedule_records: list[ WildEncounterScheduleRecord ],
      cancellation_records: list[ WildEncounterCancellationRecord ],
      days_ahead: int ) -> list[ ScheduledOccurrence ]:
   if not schedule_records:
      return []

   today = DateValues.parse_date_value( DateValues.today_date_key() )
   schedule_start_date = today
   schedule_end_date = today + timedelta( days=days_ahead )
   occurrences: list[ ScheduledOccurrence ] = []

   for schedule_record in schedule_records:
      parsed_start_date = DateValues.parse_date_value(
         value=schedule_record.schedule_start_date )
      slot_start_date = (
         parsed_start_date
         if parsed_start_date > schedule_start_date
         else schedule_start_date )
      slot_end_date = schedule_end_date

      if schedule_record.schedule_end_date != None:
         parsed_end_date = DateValues.parse_date_value(
            value=schedule_record.schedule_end_date )

         if parsed_end_date < slot_end_date:
            slot_end_date = parsed_end_date

      if slot_end_date < slot_start_date:
         continue

      encounter_time = schedule_record.encounter_time
      weekday_flags = (
         schedule_record.monday,
         schedule_record.tuesday,
         schedule_record.wednesday,
         schedule_record.thursday,
         schedule_record.friday,
         schedule_record.saturday,
         schedule_record.sunday,
      )
      current_date = slot_start_date

      while current_date <= slot_end_date:
         current_date_key = current_date.isoformat()

         if (
               CalendarDates.schedule_includes_weekday(
                  current_date.weekday(),
                  weekday_flags )
               and not wild_encounter_occurrence_is_cancelled(
                  cancellation_records,
                  current_date_key,
                  encounter_time ) ):
            occurrences.append(
               ScheduledOccurrence(
                  date=current_date_key,
                  time=encounter_time ) )

         current_date += timedelta( days=1 )

   occurrences.sort(
      key=lambda occurrence: (
         occurrence.date,
         occurrence.time or '',
      ) )

   return occurrences


def wild_encounter_occurrence_is_cancelled(
      cancellation_records: list[ WildEncounterCancellationRecord ],
      occurrence_date: str,
      encounter_time: str ) -> bool:
   return any(
      cancellation.cancellation_date == occurrence_date
      and cancellation.encounter_time == encounter_time
      for cancellation in cancellation_records
   )
