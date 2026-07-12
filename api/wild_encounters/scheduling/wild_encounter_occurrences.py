from __future__ import annotations

from ..data_access.wild_encounter_cancellation_record import WildEncounterCancellationRecord
from ..data_access.wild_encounter_schedule_record import WildEncounterScheduleRecord
from ...models import ScheduledOccurrence
from ...shared.scheduled_occurrences import build_scheduled_occurrences


def build_wild_encounter_occurrences(
      schedule_records: list[ WildEncounterScheduleRecord ],
      cancellation_records: list[ WildEncounterCancellationRecord ],
      days_ahead: int ) -> list[ ScheduledOccurrence ]:
   return build_scheduled_occurrences(
      schedule_records,
      days_ahead=days_ahead,
      get_time=lambda schedule_record: schedule_record.encounter_time,
      get_weekday_flags=lambda schedule_record: (
         schedule_record.monday,
         schedule_record.tuesday,
         schedule_record.wednesday,
         schedule_record.thursday,
         schedule_record.friday,
         schedule_record.saturday,
         schedule_record.sunday,
      ),
      is_cancelled=lambda occurrence_date, encounter_time: (
         wild_encounter_occurrence_is_cancelled(
            cancellation_records,
            occurrence_date,
            encounter_time ) ) )


def wild_encounter_occurrence_is_cancelled(
      cancellation_records: list[ WildEncounterCancellationRecord ],
      occurrence_date: str,
      encounter_time: str ) -> bool:
   return any(
      cancellation.cancellation_date == occurrence_date
      and cancellation.encounter_time == encounter_time
      for cancellation in cancellation_records
   )
