from __future__ import annotations

from ..data_access.guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from ..data_access.guardians_talk_occurrence_record import GuardiansTalkOccurrenceRecord
from ..data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from .guardians_talk_weekday_time import guardians_talk_weekday_flags
from ...models import ScheduledOccurrence
from ...shared.scheduled_occurrences import build_scheduled_occurrences


def build_guardians_talk_occurrences(
      schedule_records: list[ GuardiansTalkScheduleRecord ],
      cancellation_records: list[ GuardiansTalkCancellationRecord ],
      days_ahead: int,
      occurrence_records: list[ GuardiansTalkOccurrenceRecord ] | None = None ) -> list[ ScheduledOccurrence ]:
   def is_cancelled(
         occurrence_date: str,
         talk_time: str ) -> bool:
      return guardians_talk_occurrence_is_cancelled(
         cancellation_records,
         occurrence_date,
         talk_time )

   extra_occurrences = [
      ScheduledOccurrence(
         date=occurrence_record.occurrence_date,
         time=occurrence_record.talk_time )
      for occurrence_record in occurrence_records or []
      if (
         occurrence_record.talk_time
         and not is_cancelled(
            occurrence_record.occurrence_date,
            occurrence_record.talk_time ) )
   ]

   return build_scheduled_occurrences(
      schedule_records,
      days_ahead=days_ahead,
      get_time=lambda schedule_record: schedule_record.talk_time,
      get_weekday_flags=guardians_talk_weekday_flags,
      is_cancelled=is_cancelled,
      extra_occurrences=extra_occurrences )


def guardians_talk_occurrence_is_cancelled(
      cancellation_records: list[ GuardiansTalkCancellationRecord ],
      occurrence_date: str,
      talk_time: str ) -> bool:
   return any(
      cancellation.cancellation_date == occurrence_date
      and cancellation.talk_time == talk_time
      for cancellation in cancellation_records
   )
