from __future__ import annotations

from ..data_access.guardians_talk_cancellation_record import GuardiansTalkCancellationRecord
from ..data_access.guardians_talk_schedule_record import GuardiansTalkScheduleRecord
from .guardians_talk_weekday_time import guardians_talk_weekday_flags
from ...models import ScheduledOccurrence
from ...shared.scheduled_occurrences import build_scheduled_occurrences


def build_guardians_talk_occurrences(
      schedule_records: list[ GuardiansTalkScheduleRecord ],
      cancellation_records: list[ GuardiansTalkCancellationRecord ],
      days_ahead: int ) -> list[ ScheduledOccurrence ]:
   return build_scheduled_occurrences(
      schedule_records,
      days_ahead=days_ahead,
      get_time=lambda schedule_record: schedule_record.talk_time,
      get_weekday_flags=guardians_talk_weekday_flags,
      is_cancelled=lambda occurrence_date, talk_time: (
         guardians_talk_occurrence_is_cancelled(
            cancellation_records,
            occurrence_date,
            talk_time ) ) )


def guardians_talk_occurrence_is_cancelled(
      cancellation_records: list[ GuardiansTalkCancellationRecord ],
      occurrence_date: str,
      talk_time: str ) -> bool:
   return any(
      cancellation.cancellation_date == occurrence_date
      and cancellation.talk_time == talk_time
      for cancellation in cancellation_records
   )
