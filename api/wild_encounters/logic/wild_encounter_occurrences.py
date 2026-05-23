from __future__ import annotations

from datetime import timedelta

from ...models import ScheduledOccurrence
from ...zoo_util import ZooUtil
from ..data_access.wild_encounter_cancellation_record import WildEncounterCancellationRecord
from ..data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord


def build_wild_encounter_occurrences(
      schedule_record: WildEncounterScheduleRecord | None,
      cancellation_records: list[ WildEncounterCancellationRecord ],
      days_ahead: int ) -> list[ ScheduledOccurrence ]:
   if schedule_record == None:
      return []

   today = ZooUtil.parse_date_value( ZooUtil.today_date_key() )
   schedule_start_date = today
   schedule_end_date = today + timedelta( days=days_ahead )

   parsed_start_date = ZooUtil.parse_date_value(
      value=schedule_record.schedule_start_date )

   if parsed_start_date > schedule_start_date:
      schedule_start_date = parsed_start_date

   if schedule_record.schedule_end_date != None:
      parsed_end_date = ZooUtil.parse_date_value(
         value=schedule_record.schedule_end_date )

      if parsed_end_date < schedule_end_date:
         schedule_end_date = parsed_end_date

   if schedule_end_date < schedule_start_date:
      return []

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

   occurrences: list[ ScheduledOccurrence ] = []
   current_date = schedule_start_date

   while current_date <= schedule_end_date:
      current_date_key = current_date.isoformat()

      if (
            ZooUtil.schedule_includes_weekday(
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
