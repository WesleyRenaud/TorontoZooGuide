from __future__ import annotations

from datetime import timedelta

from ..data_access.guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from ..data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from .guardians_talk_weekday_time import guardians_talk_time_for_weekday
from ...models import ScheduledOccurrence
from ...shared.calendar_dates import DateValues


def build_guardians_talk_occurrences(
      schedule_record: GuardiansTalkScheduleRecord | None,
      cancellation_records: list[ GuardiansTalkCancellationRecord ],
      days_ahead: int ) -> list[ ScheduledOccurrence ]:
   if schedule_record == None:
      return []

   today = DateValues.parse_date_value( DateValues.today_date_key() )
   schedule_start_date = today
   schedule_end_date = today + timedelta( days=days_ahead )

   parsed_start_date = DateValues.parse_date_value(
      value=schedule_record.schedule_start_date )

   if parsed_start_date > schedule_start_date:
      schedule_start_date = parsed_start_date

   if schedule_record.schedule_end_date != None:
      parsed_end_date = DateValues.parse_date_value(
         value=schedule_record.schedule_end_date )

      if parsed_end_date < schedule_end_date:
         schedule_end_date = parsed_end_date

   if schedule_end_date < schedule_start_date:
      return []

   occurrences: list[ ScheduledOccurrence ] = []
   current_date = schedule_start_date

   while current_date <= schedule_end_date:
      current_date_key = current_date.isoformat()
      talk_time = guardians_talk_time_for_weekday(
         schedule_record,
         current_date.weekday() )

      if (
            talk_time != None
            and not guardians_talk_occurrence_is_cancelled(
               cancellation_records,
               current_date_key,
               talk_time ) ):
         occurrences.append(
            ScheduledOccurrence(
               date=current_date_key,
               time=talk_time ) )

      current_date += timedelta( days=1 )

   return occurrences


def guardians_talk_occurrence_is_cancelled(
      cancellation_records: list[ GuardiansTalkCancellationRecord ],
      occurrence_date: str,
      talk_time: str ) -> bool:
   return any(
      cancellation.cancellation_date == occurrence_date
      and cancellation.talk_time == talk_time
      for cancellation in cancellation_records
   )
